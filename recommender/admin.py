from django.contrib import admin
from .models import MoviesModel, UserPreference

class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'preference')  # Show id, user, and preference columns

# Register your models here.
admin.site.register(MoviesModel)
admin.site.register(UserPreference, UserPreferenceAdmin)
