import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
from game_recommender import steam_data
from functools import partial
from sklearn import feature_extraction


steam_df_url = 'https://storage.googleapis.com/lambdastruck_bucket/datasets/steam/steam_games.csv.gz' 
steam_df = steam_data.load_steam_df(steam_df_url)
vectors_url = 'https://storage.googleapis.com/lambdastruck_bucket/datasets/steam/steam_metadata_reduced_vectors.csv.gz' 
steam_metadata_vectors = pd.read_csv(vectors_url).values


def show_similar_games(game_name_substring):
    chosen_games_df = steam_data.get_games_by_name(steam_df, game_name_substring)
    if len(chosen_games_df) > 0:
        similar_games_df = steam_data.similar_games(chosen_games_df, steam_df, steam_metadata_vectors)
        chosen_games_df.index = chosen_games_df['name']
        st.text('Games matching title')
        st.write(chosen_games_df)
        st.text('Similar games')
        st.write(similar_games_df)
    else:
        st.text('Nothing found for query: "{}"'.format(game_name_substring))
    
game = st.text_input('Input game name', value='S.T.A.L.K.E.R')
show_similar_games(game)
