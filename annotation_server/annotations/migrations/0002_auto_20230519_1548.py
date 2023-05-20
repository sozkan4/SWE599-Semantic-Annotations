from django.db import migrations
from django.utils.crypto import get_random_string

def generate_unique_annotation_ids(apps, schema_editor):
    Annotation = apps.get_model('annotations', 'Annotation')

    for annotation in Annotation.objects.all():
        if not annotation.annotation_id:
            annotation.annotation_id = get_random_string(length=10, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            annotation.save()

class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(generate_unique_annotation_ids),
    ]
