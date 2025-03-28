from django.shortcuts import render
from .recommender import recommend
import requests
from django.http import JsonResponse
from .models import MoviesModel
from environ import Env

env = Env()

# Create your views here.

def get_movie_recommendations(request, movie_name):
    recommended_movie = recommend(movie_name)
    print(recommended_movie)

    if recommended_movie is None:
        return JsonResponse({"error": "No recommendations found."}, status=404)  # Handle None case

    movie_ids = [int(x) for x in recommended_movie]  # Ensure movie_ids is created correctly
    movies = []

    print(movie_ids)

    for movie_id in movie_ids:  # Changed variable name for clarity
        print(movie_id)
        try:
            movie = MoviesModel.objects.get(pk=movie_id)  # Use movie_id instead of movie
            # Serialize the movie object to a dictionary
            # print('movie' + str(movie_id))

            movie_data={
                "id": movie.id,
                "title": movie.movies_name,
                "description": movie.summary,
                "movie_link":movie.movies_link,
                "genres":movie.genres,
                "poster": 'https://res.cloudinary.com/'+env("CLOUDINARY_CLOUD_NAME")+'/image/upload/v1743015824/'+str(movie.movie_banner_desktop)+'.jpg'
                
                # Add other fields as necessary
            }
            print(movie_data)
             
            movies.append(movie_data)
        except MoviesModel.DoesNotExist:
            continue  # Skip this ID if it does not exist

    return JsonResponse({"movies": movies})
