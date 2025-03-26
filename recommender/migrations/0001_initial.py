# Generated by Django 5.1.7 on 2025-03-26 18:59

import cloudinary.models
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MoviesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movies_name', models.CharField(max_length=500)),
                ('movies_link', models.URLField(max_length=512)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('genres', models.JSONField(blank=True, default=list)),
                ('summary', models.TextField(default='')),
                ('movies_id', models.CharField(max_length=1000)),
                ('movie_banner_desktop', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
            ],
        ),
    ]
