"""
URL configuration for movieRecommender project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from .views import get_movie_recommendations, get_all_movies, get_movies_by_id, movies_by_genres


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('recommend/<str:movie_name>/', get_movie_recommendations, name='get_movie_recommendations'),
    path('recommend/genres', movies_by_genres, name='movies_by_genres'),
    path('movie/<str:movie_id>/', get_movies_by_id , name='get_movie_by_id'),
    path('movies/', get_all_movies , name='get_all_movies'),
]
