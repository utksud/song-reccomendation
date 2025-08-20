import streamlit as st
import pickle
import joblib
import numpy as np
import time
import pandas as pd

st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: #FFFFFF;
    }
    .stApp {
        background-color: #121212;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎧 Similar Song Recommender")

song_data = pd.read_csv('song_names.csv')
similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))

def recommend_songs(song_name, similarity_matrix, top_n=5):
    # Find the index of the song in song_data
    try:
        song_index = song_data[song_data['song'].str.lower() == song_name.lower()].index[0]
    except IndexError:
        return f"Song '{song_name}' not found in the dataset."
    
    # Get similarity scores for that song
    similarities = list(enumerate(similarity_matrix[song_index]))
    
    # Sort by similarity score (excluding the song itself)
    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    top_matches = similarities[1:top_n+1]
    
    # Get song names from song_data
    recommendations = [song_data.iloc[i[0]]['song'] for i in top_matches]
    
    return recommendations

option = st.selectbox("🎵 Select a song:", song_data)

# When button is clicked
if st.button("🔍 Analyze"):
    start = time.time()

    results = recommend_songs(option, similarity_matrix)

   

    st.success(f"Found similar songs in {round(time.time() - start, 2)} seconds!")

    # Display results in card-style layout with YouTube logo link
    for song in results:
        song_name = song.capitalize()
        youtube_search_url = f"https://www.youtube.com/results?search_query={song_name.replace(' ', '+')}"

        st.markdown(
            f'''
            <div style="background-color:#1f1f1f; padding:15px; margin-bottom:10px; border-radius:10px;">
                <div style="display:flex; align-items:center; justify-content:space-between;">
                    <span style="font-size:18px;">🎶 {song_name}</span>
                    <a href="{youtube_search_url}" target="_blank">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/0/09/YouTube_full-color_icon_(2017).svg"
                             width="28" height="28" title="Search on YouTube" />
                    </a>
                </div>
            </div>
            ''',
            unsafe_allow_html=True
        )
