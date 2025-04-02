from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField

# Create your models here.
class MoviesModel(models.Model):
    movies_name=models.CharField(max_length=500)
    movies_link=models.URLField(max_length=512)
    date_added = models.DateTimeField(default=timezone.now)
    genres=models.JSONField(default=list, blank=True)
    summary=models.TextField(default='')
    movies_id=models.CharField(max_length=1000)
    movie_poster=CloudinaryField('Poster')
    movie_banner_desktop=CloudinaryField('Banner Poster')

    def __str__(self):
        return f'{self.movies_name}'
