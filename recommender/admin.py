from django.contrib import admin
from .models import MoviesModel, UserPreference, userReviews

class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'preference')  # Show id, user, and preference columns
class MovieAdmin(admin.ModelAdmin):
    list_display = ('movies_name', 'id', 'movies_id', 'release_year')  # Show id, user, and preference columns
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie_id')  # Show id, user, and preference columns

# Register your models here.
admin.site.register(MoviesModel, MovieAdmin)
admin.site.register(UserPreference, UserPreferenceAdmin)
admin.site.register(userReviews, ReviewAdmin)
