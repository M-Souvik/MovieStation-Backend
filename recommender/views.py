# from django.shortcuts import render
from .recommender2 import recommend
import requests
from django.http import JsonResponse
from .models import MoviesModel
from environ import Env
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


env = Env()

# Create your views here.

def get_movie_recommendations(request, movie_name=None):
    recommended_movie = recommend(movie=movie_name)  # Modified call to include genres

    if not recommended_movie:  # If no recommendations found
        return JsonResponse({"error": "No recommendations found."}, status=404)

    movie_ids = [int(x) for x in recommended_movie]  # Convert to integers for querying
    print(recommended_movie)

    # Fetch movies in a single query instead of looping (Better Performance)
    movies_queryset = MoviesModel.objects.filter(movies_id__in=movie_ids)

    

    movies = []
    for movie in movies_queryset:
        movie_data = {
            "id": movie.id,
            "title": movie.movies_name,
            "description": movie.summary,
            "movie_link": movie.movies_link,
            "movie_id": movie.movies_id,
            "genres": movie.genres,
            "poster": f"https://res.cloudinary.com/{env('CLOUDINARY_CLOUD_NAME')}/image/upload/v1743015824/{movie.movie_banner_desktop}.jpg"
        }
        movies.append(movie_data)

    return JsonResponse({"movies": movies})


@csrf_exempt
def movies_by_genres(request):
    if request.method == 'POST':
        user_genres = request.POST.get("genres")
        recommended_movie_ids = recommend(preferred_genres=user_genres)
        
        if not recommended_movie_ids:  # If no recommendations found
            return JsonResponse({"error": "No recommendations found."}, status=404)
        
        movie_ids = [int(x) for x in recommended_movie_ids]

        # Fetch movie details based on the recommended IDs
        movies_queryset = MoviesModel.objects.filter(id__in=movie_ids)
        movies_list = []
        for movie in movies_queryset:
            movie_data = {
                "id": movie.id,
                "title": movie.movies_name,
                "description": movie.summary,
                "movie_link": movie.movies_link,
                "genres": movie.genres,
                "poster":str(movie.movie_poster),
                "banner_poster": str(movie.movie_banner_desktop),
            }
            movies_list.append(movie_data)

        return JsonResponse({"movies": movies_list})  # Now movies_list is a list of dictionaries


# @login_required
def get_movies_by_id(request, movie_id):
    movie = get_object_or_404(MoviesModel, movies_id=movie_id)
    
    # Serialize the movie instance to a dictionary
    movie_data = {
        "id": movie.id,
        "title": movie.movies_name,
        "description": movie.summary,
        "movie_link": movie.movies_link,
        "movie_id":movie.movies_id,
        "genres": movie.genres,
        "poster":str(movie.movie_poster),
        "banner_poster": str(movie.movie_banner_desktop), # Convert CloudinaryResource to string if necessary
    }
    
    return JsonResponse({"movie": movie_data}, safe=False)

def get_all_movies(request):
    movies = MoviesModel.objects.all()  # This returns a QuerySet
    movies_list = []

    for movie in movies:
        movie_data = {
            "id": movie.id,
            "title": movie.movies_name,
            "description": movie.summary,
            "movie_link": movie.movies_link,
            "genres": movie.genres,
            "movie_id":movie.movies_id,
            "poster":str(movie.movie_poster),
            "banner_poster": str(movie.movie_banner_desktop),  # Convert CloudinaryResource to string
        }
        movies_list.append(movie_data)

    return JsonResponse({"movies": movies_list})

# def register(request):




