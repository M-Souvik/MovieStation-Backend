# from django.shortcuts import render
from .recommender2 import recommend
import requests
from django.http import JsonResponse
from .models import MoviesModel, UserPreference
from environ import Env
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import json

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
            "runtime":movie.runtime,
            "poster": f"https://res.cloudinary.com/{env('CLOUDINARY_CLOUD_NAME')}/image/upload/v1743015824/{movie.movie_banner_desktop}.jpg"
        }
        movies.append(movie_data)

    return JsonResponse({"movies": movies})


@csrf_exempt
def movies_by_genres(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        user_genres = data.get("genres")
        recommended_movie_ids = recommend(preferred_genres=user_genres)
        
        if not recommended_movie_ids:  # If no recommendations found
            return JsonResponse({"error": "No recommendations found."}, status=404)
        
        movie_ids = [int(x) for x in recommended_movie_ids]

        # Fetch movie details based on the recommended IDs
        movies_queryset = MoviesModel.objects.filter(movies_id__in=movie_ids)
        movies_list = []
        for movie in movies_queryset:
            movie_data = {
                "id": movie.id,
                "title": movie.movies_name,
                "description": movie.summary,
                "movie_id": movie.movies_id,
                "movie_link": movie.movies_link,
                "genres": movie.genres,
                "runtime":movie.runtime,
                "poster": f"https://res.cloudinary.com/{env('CLOUDINARY_CLOUD_NAME')}/image/upload/v1743015824/{movie.movie_poster}.jpg",
                # "poster": str(movie.movie_poster),
                "banner_poster": f"https://res.cloudinary.com/{env('CLOUDINARY_CLOUD_NAME')}/image/upload/v1743015824/{movie.movie_banner_desktop}.jpg",
            }
            movies_list.append(movie_data)

        return JsonResponse({"movies": movies_list})  # Now movies_list is a list of dictionaries


# @login_required
def get_movies_by_id(request, movie_id):
    if not request.user.is_authenticated:  # Check if the user is not logged in
        return JsonResponse({"error": "Unauthorized"}, status=401)

    movie = get_object_or_404(MoviesModel, movies_id=movie_id)
    
    # Serialize the movie instance to a dictionary
    movie_data = {
        "id": movie.id,
        "title": movie.movies_name,
        "description": movie.summary,
        "movie_link": movie.movies_link,
        "movie_id": movie.movies_id,
        "genres": movie.genres,
        "poster": str(movie.movie_poster),
        "banner_poster": str(movie.movie_banner_desktop),  # Convert CloudinaryResource to string if necessary
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
            "runtime": movie.runtime,
            "movie_id": movie.movies_id,
            "poster": f"https://res.cloudinary.com/{env('CLOUDINARY_CLOUD_NAME')}/image/upload/v1743015824/{movie.movie_poster}.jpg",
            # "banner_poster": str(movie.movie_banner_desktop),  # Convert CloudinaryResource to string
            "banner_poster": f"https://res.cloudinary.com/{env('CLOUDINARY_CLOUD_NAME')}/image/upload/v1743015824/{movie.movie_banner_desktop}.jpg",

        }
        movies_list.append(movie_data)

    return JsonResponse({"movies": movies_list})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        if not username or not password or not email:
            return JsonResponse({"error": "All fields are required."}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists."}, status=400)

        user = User(
            username=username,
            email=email,
            password=make_password(password)  # Hash the password before saving
        )
        user.save()

        savedUser = {
            "id": user.id,
            "username": user.username,
            # "email"
        }

        return JsonResponse({"message": "User registered successfully.", "user": savedUser}, status=201)

    return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")


        if not email or not password:
            return JsonResponse({"error": "Email and password are required."}, status=400)

        try:
            user = User.objects.get(email=email)  # Get user by email
            if user.check_password(password):  # Check the password
                refresh = RefreshToken.for_user(user)
                if user:
                    preferences=UserPreference.objects.get(user_id=user.id)
                    print(preferences)
                    # preferences_data = {
                    #     "id": preferences.id,
                    #     "preference": preferences.preference,  # Assuming preference is already serializable
                    # }

                return JsonResponse({
                    "message": "Login successful.",
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': {
                        "id":user.id,
                        "username":user.username,
                        "email":user.email,
                        "preferences":preferences.preference
                    }
                }, status=200)
            else:
                return JsonResponse({"error": "Invalid email or password."}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"error": "Invalid email or password."}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def add_user_preference(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        
        # Assuming you have the user ID in the request data
        user_id = data.get('user_id')  # Get user ID from the request data
        preference=data.get('preference')
        
        try:
            user = User.objects.get(id=user_id)  # Fetch the user instance
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        # Create a new UserPreference instance
        user_preference = UserPreference(user=user, preference=preference)  # Pass the user instance
        # Set other fields as necessary
        # user_preference.some_field = data.get('some_field')

        user_preference_data = {
                'user_id': user.id,  # Serialize the user ID
                'preference': preference,  # Assuming preference is already serializable
            }

        user_preference.save()  # Save the instance to the database
        return JsonResponse({"message": "Preference added successfully", 'user_preference':user_preference_data}, status=201)

    return JsonResponse({"error": "Invalid request"}, status=400)