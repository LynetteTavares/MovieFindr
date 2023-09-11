# Import Libraries
import pandas as pd
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def cleanData(file):

     # Load file
    movies = pd.read_excel(file)

    # Replace null value by ''
    movies = movies.fillna('')

    return movies


# Function takes dataframe and output the Cosine Similarity matrix
def selectFeatures(df):

    df['features'] =  (df['movie_genres'] + df['movie_keywords']).str.replace('[', '').str.replace(']', '').str.strip()
    count = CountVectorizer(stop_words='english', min_df=0.1, max_df=0.9)
    count_matrix = count.fit_transform(df['features'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    return cosine_sim


# Function that takes in movie title as input and outputs most similar movies
def get_recommendations(title, df):

    # Load data
    movies = df
    # Get the index of the movie that matches the title
    idx = movies[movies['movie_title'] == title].index[0]

    # Get the pairwsie similarity scores of all movies with that movie
    cosine_sim = selectFeatures(movies)
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 5 most similar movies
    sim_scores = sim_scores[1:6]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 5 most similar movies
    return movies.iloc[movie_indices]


# fetch API 
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path