cat streamlit/config.toml | sed s/\$PORT/$PORT/ - > .streamlit/config.toml
nbdev_build_lib; pip install -e .
