from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

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
    runtime=models.CharField(max_length=50, default='')
    ratings=models.CharField(max_length=10, default=0)
    release_year=models.CharField(max_length=10, default='')
    director=models.CharField(max_length=100, default='None')
    review=models.TextField(max_length=1000, default='None')
    viewed=models.BooleanField(default=False)
    views=models.TextField(default=0)

    def __str__(self):
        return f'{self.movies_name}-{self.movies_id}'
    
class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    preference = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f'{self.user}-{self.preference}'
