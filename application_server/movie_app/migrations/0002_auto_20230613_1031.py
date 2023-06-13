# Generated by Django 3.2.18 on 2023-06-13 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='wikidata_explanations',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='wikidata_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
