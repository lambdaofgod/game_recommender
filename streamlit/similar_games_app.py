import streamlit as st
import numpy as np
import pandas as pd
from game_recommender import steam_data, content_based
from functools import partial
from sklearn import feature_extraction
import altair
import umap


steam_df_url = 'https://storage.googleapis.com/lambdastruck_bucket/datasets/steam/steam_games.csv.gz' 
steam_df = steam_data.load_steam_df(steam_df_url)
vectors_url = 'https://storage.googleapis.com/lambdastruck_bucket/datasets/steam/steam_metadata_reduced_vectors.csv.gz' 
umap_vectors_url = 'https://storage.googleapis.com/lambdastruck_bucket/datasets/steam/steam_metadata_umap_vectors.csv.gz' 
steam_metadata_vectors = pd.read_csv(vectors_url).values
searcher = content_based.SimilaritySearcher(steam_df, steam_metadata_vectors)
viz_df = pd.read_csv(umap_vectors_url)


def show_similar_games(raw_game_name_substring):
    game_name_substring = steam_data.normalize_name(raw_game_name_substring)
    chosen_games_df = steam_data.get_games_by_name(steam_df, game_name_substring)
    if len(chosen_games_df) > 0:
        results = searcher.find_similar(chosen_games_df['name'])
        similar_games_df = content_based.make_stacked_results_df(*results)
        chosen_games_df.index = chosen_games_df['name']
        st.text('Games matching title')
        st.write(chosen_games_df)
        st.text('Similar games')
        st.write(similar_games_df)
        viz_df['is_similar'] = viz_df['name'].isin(content_based.get_similar_game_names_from_results(results[0]))
        similar_points_altair_scatterplot = (
            altair.Chart(viz_df[viz_df['is_similar']])
                .mark_circle(size=100, color='red', opacity=1.0)
                .encode(x='X', y='Y', tooltip=['name'])
                .interactive()
        )

        not_similar_points_altair_scatterplot = (
            altair.Chart(viz_df[~viz_df['is_similar']])
                .mark_circle(size=10, color='blue', opacity=0.1)
                .encode(x='X', y='Y', tooltip=['name'])
                .interactive()
        )

        st.altair_chart(similar_points_altair_scatterplot + not_similar_points_altair_scatterplot)
    else:
        st.text('Nothing found for query: "{}"'.format(game_name_substring))
    
game = st.text_input('Input game name', value='s.t.a.l.k.e.r')
show_similar_games(game)
