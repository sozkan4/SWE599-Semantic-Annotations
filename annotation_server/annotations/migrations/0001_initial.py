from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.crypto import get_random_string


def generate_unique_annotation_ids(apps, schema_editor):
    Annotation = apps.get_model('annotations', 'Annotation')

    for annotation in Annotation.objects.all():
        if not annotation.annotation_id:
            annotation.annotation_id = get_random_string(length=10, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            annotation.save()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        # Add the correct dependency for the previous migration
        ('annotations', '000W_previous_migration'),

        # Add the dependency for the AUTH_USER_MODEL setting
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(generate_unique_annotation_ids),

        migrations.CreateModel(
            name="Movie",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("release_year", models.IntegerField()),
                ("genre", models.CharField(max_length=255)),
                ("director", models.CharField(max_length=255)),
                ("description", models.TextField()),
            ],
        ),

        migrations.CreateModel(
            name="Annotation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("annotation_id", models.CharField(max_length=10, unique=True)),
                ("content", models.TextField()),
                ("annotation_type", models.CharField(max_length=255)),
                ("target", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("movie", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="annotations.Movie")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
