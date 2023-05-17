from django.contrib import admin

from .models import Annotation


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ("id", "type")
    search_fields = ("id", "type")
    readonly_fields = ("id", "type", "body", "target")