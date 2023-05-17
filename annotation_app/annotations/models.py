from django.db import models
from django.core.validators import URLValidator
from .validators import validate_annotation_type

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
