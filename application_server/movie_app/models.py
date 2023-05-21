from django.db import models
from django.core.validators import URLValidator
from .validators import validate_annotation_type
from ckeditor.fields import RichTextField
from datetime import datetime

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    bio = models.TextField(default="none")
    profile_pic = models.ImageField(upload_to='pictures', default='default.jpg')

    def __str__(self):
        return self.first_name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = RichTextField(blank=True, null=True)
    creation_date = models.DateField(default=datetime.now)
    likes = models.ManyToManyField(User, related_name='likes')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(default='no name', max_length=50)
    comment = models.CharField(max_length=400)

    def __str__(self):
        return self.name + "=>" + self.comment


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(default=None)
    message = models.TextField()

    def __str__(self):
        return self.name


class Annotation(models.Model):
    annotation_id = models.CharField(max_length=255, unique=True)
    context = models.URLField(default="http://www.w3.org/ns/anno.jsonld", validators=[URLValidator()])
    annotation_type = models.CharField(max_length=255, default="Annotation", validators=[validate_annotation_type])
    body = models.JSONField()
    target = models.JSONField()
    creation_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["creation_datetime"]
        verbose_name = "annotation"
        verbose_name_plural = "annotations"

    @property
    def as_dict(self):
        annotation_dict = {
            "@context": self.context,
            "id": self.annotation_id,
            "type": self.annotation_type,
            "body": self.body,
            "target": self.target,
        }
        return annotation_dict
