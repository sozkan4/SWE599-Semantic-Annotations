from django.contrib import admin

from .models import Annotation


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ("annotation_id", "type_display")
    search_fields = ("annotation_id", "annotation_type")
    readonly_fields = ("annotation_id", "annotation_type", "body", "target", "context", "creation_datetime")

    def type_display(self, obj):
        return obj.annotation_type
    type_display.short_description = 'Type'