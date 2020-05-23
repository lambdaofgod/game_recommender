import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
from game_recommender import steam_data
from functools import partial
from sklearn import feature_extraction


steam_df = steam_data.load_steam_df()
vectorizer = steam_data.make_df_column_vectorizer([
        ['popular_tags'],
        ['game_description', 'desc_snippet'],
    ],
    vectorizer_classes=partial(
            feature_extraction.text.CountVectorizer,
            binary=True
    ),
    tokenizers=[steam_data.split_by_comma_tokenizer, None]
)
steam_metadata_vectors = vectorizer.fit_transform(steam_df)

game = st.text_input('Input game name')
if st.checkbox('Find similar games'):
    st.text('Games matching title')
    chosen_games_df = steam_data.get_games_by_name(steam_df, game)
    st.text('Similar games')
    similar_games_df = steam_data.similar_games(chosen_games_df, steam_df, steam_metadata_vectors)
    st.write(similar_games_df)
