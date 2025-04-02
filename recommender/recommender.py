import numpy as np
import pandas as pd

movies = pd.read_csv('dataset1.csv', usecols=lambda column: not column.startswith('Unnamed'))

movies.head()

movies.isnull().sum()

movies.duplicated().sum()

movies.dropna(inplace=True)

movies.isnull().sum()

import ast
def convert(obj):
    tags=[]
    for i in ast.literal_eval(obj):
        tags.append(i['name'])
    return tags

movies['genres']=movies['genres'].apply(convert)


movies['keywords']=movies['keywords'].apply(convert)

movies.head()

import ast
def convertCast(obj):
    tags=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter != 3:
            tags.append(i['name'])
            counter+=1
        else:
            break
    return tags

movies['cast']=movies['cast'].apply(convertCast)

movies.head()

import ast
def findDirector(obj):
    tags=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            tags.append(i['name'])
            break
    return tags

movies['crew']=movies['crew'].apply(findDirector)

movies.head()

movies['overview']=movies['overview'].apply(lambda x:x.split())

movies.head()

movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

movies.head()

movies['tags']=movies['overview']+movies['genres']+movies['cast']+movies['keywords']+movies['crew']

movies.head()

newMoviesData=movies[['id','movie_id','movie_name','tags','genres']]

newMoviesData.head()

newMoviesData['tags']=newMoviesData['tags'].apply(lambda x:" ".join(x))

newMoviesData.head()

newMoviesData['tags'][0]

import nltk

from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

def stem(text):
    textArray=[]
    for i in text.split():
        textArray.append(ps.stem(i))
    return " ".join(textArray)

newMoviesData['tags']=newMoviesData['tags'].apply(stem)

from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=80, stop_words='english')

vectors=cv.fit_transform(newMoviesData['tags']).toarray()

vectors

vectors[0]

cv.get_feature_names_out()

from sklearn.metrics.pairwise import  cosine_similarity

similarity=cosine_similarity(vectors)

similarity[1]

def recommend(movie=None, preferred_genres=None):
    recommended_movies = []

    # If the user provides a movie name
    if movie:
        matched_movies = newMoviesData[newMoviesData['movie_name'].str.contains(movie, case=False, na=False)]
        
        if matched_movies.empty:
            print("No matching movies found.")
            return []

        # Select the first matched movie (or modify logic to handle multiple)
        movies_index = matched_movies.index[0]
        
        # Compute distances and get similar movies
        distances = similarity[movies_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:10]  # Get top 10 recommendations
        
        recommended_movies = [newMoviesData.iloc[i[0]] for i in movies_list]

    # If user provides genres only
    if preferred_genres:
        preferred_genres = [g.lower() for g in preferred_genres]

        # Filter movies that match user genres
        genre_filtered_movies = movies[movies['genres'].apply(lambda g: any(genre in preferred_genres for genre in g))]
        
        if not recommended_movies:
            # If no movie name was provided, return top movies from this genre
            recommended_movies = genre_filtered_movies.sample(n=min(5, len(genre_filtered_movies))).to_dict(orient="records")
        else:
            # Filter recommended movies based on genres
            recommended_movies = [movie for movie in recommended_movies if any(g in preferred_genres for g in movies['genres'][movie.name])]

    # If no recommendations found, return top movies from dataset
    if not recommended_movies:
        recommended_movies = newMoviesData.sample(n=5).to_dict(orient="records")

    # Return the list of movie IDs
    return [movie['id'] for movie in recommended_movies]




