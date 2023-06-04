from django.db import models
from django.core.validators import URLValidator
from .validators import validate_annotation_type

class Annotation(models.Model):
    # A unique identifier for each annotation. This should follow the IRI specification.
    annotation_id = models.CharField(max_length=255, unique=True)

    # The context for the annotation, typically the URL of the JSON-LD schema.
    # It's set to the W3C annotation context by default.
    context = models.URLField(default="http://www.w3.org/ns/anno.jsonld", validators=[URLValidator()])

    # The type of the annotation, which must be a valid property in the JSON-LD schema.
    annotation_type = models.CharField(max_length=255, default="Annotation", validators=[validate_annotation_type])

    # The body of the annotation, stored as JSON.
    body = models.JSONField(default=dict) 

    # The target of the annotation, stored as JSON.
    target = models.JSONField()

    # The datetime when the annotation was created. This is automatically set when the annotation is created.
    creation_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        # The default ordering for the annotations. They will be ordered by creation_datetime when retrieved.
        ordering = ["creation_datetime"]

        # The human-readable name for the Annotation model, used in the Django admin interface.
        verbose_name = "annotation"

        # The human-readable plural name for the Annotation model, used in the Django admin interface.
        verbose_name_plural = "annotations"

    @property
    def as_dict(self):
        # Converts the Annotation instance into a dictionary.
        annotation_dict = {
            "@context": self.context,
            "id": self.annotation_id,
            "type": self.annotation_type,
            "body": self.body,
            "target": self.target,
        }
        return annotation_dict
