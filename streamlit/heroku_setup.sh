mkdir -p .streamlit
cat streamlit/config.toml | sed s/PORT/$PORT/ - > .streamlit/config.toml
cp streamlit/credentials.toml .streamlit/credentials.toml
nbdev_build_lib; pip install -e .
streamlit run streamlit/similar_games_app.py
