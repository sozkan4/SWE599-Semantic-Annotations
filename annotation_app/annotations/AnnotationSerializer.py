from rest_framework import serializers
from .models import Annotation

class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ["annotation_id", "context", "annotation_type", "body", "target", "creation_datetime"]
