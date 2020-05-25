mkdir -p data
kaggle datasets download trolukovich/steam-games-complete-dataset
kaggle datasets download tamber/steam-video-games
mv steam-games-complete-dataset.zip data
mv steam-video-games.zip data
