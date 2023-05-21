# Generated by Django 3.2.18 on 2023-05-21 23:15

import datetime
import django.core.validators
from django.db import migrations, models
import movie_app.validators


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annotation_id', models.CharField(max_length=255, unique=True)),
                ('context', models.URLField(default='http://www.w3.org/ns/anno.jsonld', validators=[django.core.validators.URLValidator()])),
                ('annotation_type', models.CharField(default='Annotation', max_length=255, validators=[movie_app.validators.validate_annotation_type])),
                ('body', models.JSONField()),
                ('target', models.JSONField()),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'annotation',
                'verbose_name_plural': 'annotations',
                'ordering': ['creation_datetime'],
            },
        ),
        migrations.AlterField(
            model_name='post',
            name='creation_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
