from django.db import models
from django.core.validators import URLValidator
from .validators import validate_annotation_type
from ckeditor.fields import RichTextField
from datetime import datetime
from django.db import models
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    bio = models.TextField(default="none")
    profile_pic = models.ImageField(upload_to='pictures', default='default.jpg')

    def __str__(self):
        return self.first_name
        
class Tag(models.Model):
    name = models.CharField(max_length=255)
    wikidata_id = models.CharField(max_length=50)  # stores Wikidata Q-ID
    wikidata_explanations = models.TextField(blank=True)  # stores explanations related to the tag

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    creation_date = models.DateField(default=datetime.now)
    likes = models.ManyToManyField(User, related_name='likes')
    web_link = models.URLField(max_length=200, blank=True, null=True)  # field for web link
    slug = models.SlugField(unique=True, max_length=100, blank=True)
    tags = TaggableManager()

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


