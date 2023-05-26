import streamlit as st
import pickle
import pandas as pd
import requests
import time
import bz2
import _pickle as cPickle

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlORaNOCBB-FbhJ8St5kALNLZerCJvpL57BA&usqp=CAU");
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]

    with st.spinner('Wait for it...'):
        time.sleep(2)
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        #fetch poster from Api
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


movie_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movie_dict)

#similarity=pickle.load(open('similarity.pkl','rb'))


similarity = cPickle.load(bz2.BZ2File('similarity.pbz2', 'rb'))

st.markdown("<h1 style='text-align: center;color: skyblue;font-size:110px;'>Cinema Guide</h1>", unsafe_allow_html=True)
page_bg_img = """
<style>
.header {
    margin-bottom: 50em;
    color: #CCCCFF;
    # color: #6495ED;
    font-weight: bold;
    font-size: 25px;
    text-align: center;
    margin-bottom: -15em;
}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown('<p class="header">Find your perfect film! </p>', unsafe_allow_html=True)
selected_movie_name = st.selectbox('',movies['title'].values)

button_style = '''
    <style>
    .stButton button {
        background-color: #87ceeb;
        color: #F5F5DC;
        text-align: center;
        display: block;
        margin: 0 auto;
        padding: 10px 25px;
        border-radius: 5px;
        cursor: default;
        font-weight: bold;
        font-style: italic;
    }
    </style>
'''

st.markdown(button_style, unsafe_allow_html=True)

if st.button('Discover Movies'):

    if st.markdown(
            """
            <style>

            .movie-container {
                display: flex;
                overflow-x: auto;
                gap: 2em;
                margin-top: 1em;
            }

            .movie-card {
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
            }

            .movie-title {
                margin-top: 0.3em;
                margin-bottom: 2.5em;
                font-weight: bold;
            }
            </style>

            """,
            unsafe_allow_html=True
    ):
        names, posters = recommend(selected_movie_name)

        st.markdown('<div class="movie-container">', unsafe_allow_html=True)
        for name, poster in zip(names, posters):
            st.markdown(
                """
                <div class="movie-card">
                    <img src="{}" width="150">
                    <p class="movie-title">{}</p>
                </div>
                """.format(poster, name),
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
