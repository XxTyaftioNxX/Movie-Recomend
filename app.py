import streamlit as st
import pickle
import pandas as pd
import requests

st.title('Movie Recommendations')

#loading the movie dataset as dictionary and the smiliarity matrix
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

from tmdbv3api import TMDb
tmdb = TMDb()
tmdb.api_key = '0637662c8bb31d6ff455570552952b85'

from tmdbv3api import Movie
tmdb_movie = Movie() 

#getting id for the movies
def get_id(movie):
    result = tmdb_movie.search(movie)
    return result[0].id

#getting the poster path
def get_poster(movie):
    movie_id = get_id(movie)
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id,tmdb.api_key))
    print(response.json()['poster_path'])
    return 'https://image.tmdb.org/t/p/w500/' + str(response.json()['poster_path'])

#get recommended movies /  posters
def recommend(name):
    user_movie_index = movies[movies['movie_title'] == name].index[0]
    print(user_movie_index)
    recommended_movies = list(enumerate(similarity[user_movie_index]))
    sorted_recommended_movies = sorted(recommended_movies, key=lambda x: x[1], reverse=True)[1:6]
    
    recommended = []
    poster_paths = []

    for i in sorted_recommended_movies:
        title = movies.iloc[i[0]].movie_title
        poster_paths.append(get_poster(title))
        recommended.append(title)

    return recommended, poster_paths

#acquiring the movie the user has selected
user_selected_movie = st.selectbox(
    'Type the Name of the movie you like to be recommened similar movies to',
    movies.movie_title .values
)

#show recommended 
if st.button('Recommend!!'):
    recommended, poster_paths = recommend(user_selected_movie)

    col1, col2, col3, col4, col5 = st.beta_columns(5)
    
    with col1:
        st.header(recommended[0])
        st.image(poster_paths[0])
    
    with col2:
        st.header(recommended[1])
        st.image(poster_paths[1])

    with col3:
        st.header(recommended[2])
        st.image(poster_paths[2])
    
    with col4:
        st.header(recommended[3])
        st.image(poster_paths[3])

    with col5:
        st.header(recommended[4])
        st.image(poster_paths[4])