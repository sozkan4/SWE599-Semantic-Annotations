from django.urls import path
from annotations.views import create_annotation, update_annotation, delete_annotation

urlpatterns = [
    # Other URL patterns
    path('annotations/', create_annotation, name='create_annotation'),
    path('annotations/<int:annotation_id>/', update_annotation, name='update_annotation'),
    path('annotations/<int:annotation_id>/', delete_annotation, name='delete_annotation'),
]
