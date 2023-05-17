from django.db import models
from django.contrib.auth.models import User

        
class Annotation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assumes you're using Django's built-in User model for authentication
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    annotation_type = models.CharField(max_length=255)  # E.g., 'text', 'image', etc.
    target = models.TextField()  # Reference to the annotated text or image
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["creation_datetime"]
        verbose_name = "annotation"
        verbose_name_plural = "annotations"

    @property
    def as_dict(self):
        annotation_dict = {
            "@context": "http://www.w3.org/ns/anno.jsonld",
            "id": self.id,
            "type": self.type,
            "body": self.body,
            "target": self.target,
        }

        return annotation_dict