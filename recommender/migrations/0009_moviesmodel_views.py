# Generated by Django 5.1.7 on 2025-04-06 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0008_moviesmodel_viewed'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviesmodel',
            name='views',
            field=models.TextField(default=0),
        ),
    ]
