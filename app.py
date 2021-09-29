import streamlit as st
import pickle
import pandas as pd

st.title('Movie Recommendations')

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(name):
    user_movie_index = movies[movies['movie_title'] == name].index[0]
    print(user_movie_index)
    recommended_movies = list(enumerate(similarity[user_movie_index]))
    sorted_recommended_movies = sorted(recommended_movies, key=lambda x: x[1], reverse=True)[1:6]
    
    recommended = []
    for i in sorted_recommended_movies:
        recommended.append(movies.iloc[i[0]].movie_title)

    return recommended

user_selected_movie = st.selectbox(
    'Type the Name of the movie you like to be recommened similar movies to',
    movies.movie_title .values
)

if st.button('Recommend!!'):
    recommended = recommend(user_selected_movie)
    for movie in recommended:
        st.write(movie)
