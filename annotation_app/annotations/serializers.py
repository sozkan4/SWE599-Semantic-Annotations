from rest_framework import serializers
from .models import Annotation

class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        # The model the serializer should serialize.
        model = Annotation

        # The fields to include in the serialized representation.
        fields = ["annotation_id", "context", "annotation_type", "body", "target", "creation_datetime"]
