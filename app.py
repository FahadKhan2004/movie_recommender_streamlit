import streamlit as st
import pickle
import pandas as pd
import requests
movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load((open('similarity.pkl','rb')))

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=08490cea234f10816e114c329d2fa900&language=en-US'.format(movie_id))
    data=response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:9]

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movie_list:
        movied_id=movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movied_id))
    return recommended_movies,recommended_movies_posters



st.title('Movie Recommender System')

#select box
selected_movie_name=st.selectbox(
    'How ',
movies['title'].values)

'''if st.button('Recommend'):
    names, posters=recommend(selected_movie_name)

    col1, col2, col3, col4, col5 =st.columns(5)
    with col1:
        st.header(names[0])
        st.image(posters[0])
    with col2:
        st.header(names[1])
        st.image(posters[1])
    with col3:
        st.header(names[2])
        st.image(posters[2])
    with col4:
        st.header(names[3])
        st.image(posters[3])
    with col5:
        st.header(names[4])
        st.image(posters[4])'''
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Custom CSS for scrollable text with spacing
    text_style = """
        <style>
        .scrollable-text {
            width: 100%;                /* Full width within the column */
            white-space: nowrap;         /* Prevent text from wrapping */
            overflow-x: auto;            /* Horizontal scroll if text overflows */
            text-align: center;          /* Center the text */
            font-size: 16px;             /* Adjust font size as needed */
            margin-bottom: 5px;          /* Space between text and image */
        }
        img {
            margin-bottom: 20px;         /* Space between movies */
        }
        </style>
    """
    st.markdown(text_style, unsafe_allow_html=True)

    # First row of 4 columns
    row1_cols = st.columns(4)
    for i, col in enumerate(row1_cols):
        with col:
            st.markdown(f"<div class='scrollable-text'>{names[i]}</div>", unsafe_allow_html=True)
            st.image(posters[i], use_column_width=True)

    # Second row of 4 columns
    row2_cols = st.columns(4)
    for i, col in enumerate(row2_cols):
        with col:
            st.markdown(f"<div class='scrollable-text'>{names[i+4]}</div>", unsafe_allow_html=True)
            st.image(posters[i+4], use_column_width=True)
