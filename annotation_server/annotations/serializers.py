from rest_framework import serializers
from .models import Annotation

class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ["annotation_id", "context", "annotation_type", "body", "target", "creation_datetime"]

    def create(self, validated_data):
        return Annotation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.annotation_id = validated_data.get("annotation_id", instance.annotation_id)
        instance.context = validated_data.get("context", instance.context)
        instance.annotation_type = validated_data.get("annotation_type", instance.annotation_type)
        instance.body = validated_data.get("body", instance.body)
        instance.target = validated_data.get("target", instance.target)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
