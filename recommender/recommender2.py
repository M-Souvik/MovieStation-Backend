import numpy as np
import pandas as pd

movies = pd.read_csv('movieDataset2.csv', usecols=lambda column: not column.startswith('Unnamed'))

movies.head()

movies['description']=movies['description'].apply(lambda x:x.split())

movies['genre'] = movies['genre'].apply(lambda x: x.split(","))

movies.head()

movies.head()

movies['tags']=movies['description']+movies['genre']

movies.head()

newData=movies[['ID','movie_id','movie_name','genre','tags']]

newData.head()

newData['tags']=newData['tags'].apply(lambda x:" ".join(x))

newData.head()

import nltk

from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

def stem(text):
    textArray=[]
    for i in text.split():
        textArray.append(ps.stem(i))
    return " ".join(textArray)

newData['tags']=newData['tags'].apply(stem)

from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=80, stop_words='english')

vectors=cv.fit_transform(newData['tags']).toarray()

vectors

cv.get_feature_names_out()

from sklearn.metrics.pairwise import  cosine_similarity

similarity=cosine_similarity(vectors)

similarity[1]

def recommend(movie=None, preferred_genres=None):
    recommended_movies = []

    # If the user provides a movie name
    if movie:
        matched_movies = newData[newData['movie_name'].str.contains(movie, case=False, na=False)]
        
        if matched_movies.empty:
            print("No matching movies found.")
            return []

        # Select the first matched movie (or modify logic to handle multiple)
        movies_index = matched_movies.index[0]
        
        # Compute distances and get similar movies
        distances = similarity[movies_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:10]  # Get top 10 recommendations
        
        recommended_movies = [newData.iloc[i[0]] for i in movies_list]

    # If user provides genres only
    if preferred_genres:
        preferred_genres = [g.lower() for g in preferred_genres]

        # Ensure `movies['genre']` is a list before applying filtering
        genre_filtered_movies = movies[movies['genre'].apply(
            lambda g: isinstance(g, list) and any(genre in [x.lower() for x in g] for genre in preferred_genres)
        )]
        
        if not recommended_movies:
            # If no movie name was provided, return top movies from this genre
            recommended_movies = genre_filtered_movies.sample(n=min(5, len(genre_filtered_movies))).to_dict(orient="records")
        else:
            # Filter recommended movies based on genres
            recommended_movies = [
                movie for movie in recommended_movies
                if isinstance(movies.loc[movie.name, 'genre'], list) and 
                   any(g.lower() in preferred_genres for g in movies.loc[movie.name, 'genre'])
            ]

    # If no recommendations found, return top movies from dataset
    if not recommended_movies:
        recommended_movies = newData.sample(n=5).to_dict(orient="records")

    # Return the list of movie names
    return [movie['movie_id'] for movie in recommended_movies]


recommend(movie='')

recommend(preferred_genres=["thriller","action"])







