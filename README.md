# Movies App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/asad-mahmood/moviesapp/main/app.py)

A small demo of the App:

![Alt Text](https://github.com/asad-mahmood/moviesApp/blob/main/ezgif.com-gif-maker%20(1).gif)

## App Functionality

This is a multi page app which visually explores movies data from 'The Open Movie Dataset'. I am also using pandas profiling for EDA. It has five filters on its sidebar as follows:
+ Year
+ Genre
+ Rated
+ IMDB Rating
+ Metacritic Rating

## Reproducing this web app

To recreate this web app on your own computer, do the following.

### Install prerequisite libraries

Download requirements.txt file

```
wget https://github.com/asad-mahmood/moviesApp/edit/main/requirements.txt
```

Pip install libraries

```
pip install -r requirements.txt
```

###  Download and unzip contents from GitHub repo

Download and unzip contents from this repo and open up the command prompt and traverse to the location where you unzipped the repo contents

###  Launch the app

Use this command to run it on your local machine

```
streamlit run app.py
```
