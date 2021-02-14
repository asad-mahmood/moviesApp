import numpy as np
import pandas as pd
import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import plotly.express as px


# Web App Title
st.set_page_config(page_title='Movie Explorer',
                   layout='wide')

st.title("Movie Explorer")
st.subheader("The data used in this webapp is accquired from [The Open Movie Database.](http://www.omdbapi.com/)")
st.write("The OMDb API is a RESTful web service to obtain movie information, all content and images on the site are contributed and maintained by our users.")
st.write("**Made By: Asad Mahmood**")

# Load data
@st.cache
def load_data():

    a = pd.read_csv('https://raw.githubusercontent.com/asad-mahmood/moviesApp/main/all_movies.csv')

    # Copy of orginal dataframe
    oa = a
    missingData = []
    for col in a.columns:
        missingData.append((col, round(100 * a[col].isnull().sum() / len(a), 2)))

    mDf = pd.DataFrame(data=missingData, columns=['Column Names', 'Missing Data %'])
    mDf = mDf.sort_values(by='Missing Data %', ascending=False)
    mfig = px.bar(mDf, x='Column Names', y='Missing Data %', width = 1600, height = 500)
    mfig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    a = a.dropna()
    a = a.reset_index(drop=True)
    a = a.assign(Genre=a['Genre'].str.split(', ')).explode('Genre')

    return a, oa, mfig


df, odf, mfig = load_data()

########
######## Sidebar
########

st.sidebar.header('Navigation')
tabs = ('Overview of Project', 'EDA', 'Visual Exploration', 'Ratings10', 'Rotten')
tab = st.sidebar.selectbox("",tabs)


# Header of Specify Input Parameters
st.sidebar.header('Specify Filter Parameters')

######## Year

st.sidebar.subheader('1) Select by Year')
Year = st.sidebar.slider('Select a Range of Years', 1927, 2014, (1927, 2014), 1)
df = df[(df['Year'] >= Year[0]) & (df['Year'] <= Year[1])]

######### Genre

st.sidebar.subheader('2) Select Genre')
genre_list = list(df.Genre.unique())
genre_list = ['All'] + genre_list
genre_list = tuple(genre_list)
value = st.sidebar.selectbox("Select ('All') if you want to view all Genres", genre_list, 0)

if value == "All":
    df = df
else:
    df = df[df['Genre'] == value]

######### Rating

st.sidebar.subheader('3) Select Rated')
rated_list = list(df.Rated.unique())
rated_list = ['All'] + rated_list
rated_list = tuple(rated_list)
rated = st.sidebar.selectbox("Select ('All') if you want to view all Ratings", rated_list, 0)

if rated == "All":
    df = df
else:
    df = df[df['Rated'] == rated]

######### IMDB
st.sidebar.subheader('4) Select by IMDB Rating')
imdb = st.sidebar.slider('Select a Range of IMDB Rating', float(df.imdbRating.min()), float(df.imdbRating.max()), (float(df.imdbRating.min()), float(df.imdbRating.max())), 0.1)
df = df[(df['imdbRating'] >= imdb[0]) & (df['imdbRating'] <= imdb[1])]

######### Metacritic
st.sidebar.subheader('5) Select by Metacritic Rating')
mtcrtic = st.sidebar.slider('Select a Range of Metacritic Rating', float(df.Metacritic.min()), float(df.Metacritic.max()), (float(df.Metacritic.min()), float(df.Metacritic.max())), 0.1)
df = df[(df['Metacritic'] >= mtcrtic[0]) & (df['Metacritic'] <= mtcrtic[1])]


#########
######### Navigation Panel
#########

if tab == 'Overview of Project':
    st.header('**Overview of Project**')
    st.subheader('Input DataFrame')
    st.write(df.head())
    st.subheader("Data Cleaning and Preprocessing Steps")
    st.write("**1)** Loaded data from my [Github Repo]('https://raw.githubusercontent.com/asad-mahmood/moviesApp/main/all_movies.csv')\n")
    st.write("**2)** Dropped all rows that had missing values so as to create more accurate plots. The missing value data percentages can be viewed below")
    st.plotly_chart(mfig)
    st.write("**3)** The 'Genre' column string patterns are converted to single genre categories so as to have a more efficetive data visualizations.")
    st.write("**4)** A copy of orginal dataframe was kept for visual exploration of columns that don't have any missing data.")

elif tab == 'EDA':
    st.header("**Exploratory Data Analysis**")
    pr = ProfileReport(df, explorative=True)
    st.subheader('Input DataFrame')
    st.write(df.head())
    st.write('---')
    st.header('**Pandas Profiling Report**')
    st_profile_report(pr)

elif tab == 'Visual Exploration':
    st.header("**Visual Exploration of Movies winning Oscar Awards**")
    col1, col2 = st.beta_columns(2)

    with col1:
        st.subheader("1) Different Genre movies that won Oscars")
        fig1 = px.pie(df, values='Oscars', names='Genre', title='Genres with a history of winning Oscar Awards')
        st.plotly_chart(fig1)

    with col2:
        st.subheader("3) Top 10 Movies which won most Oscars")
        oscarsDf = odf.nlargest(10, 'Oscars')
        fig2 = px.bar(oscarsDf, x='Title', y='Oscars',
                     title='Most Oscar Winning Movies')
        fig2.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
        st.plotly_chart(fig2)

    st.subheader("2) Different Genre movies having different Runtime")
    fig = px.bar(df, y='Oscars', x='Rated', color='Genre',
                     title='Genres with a history of winning Oscar Awards',
                     animation_frame="Year", hover_name = "Title",
                     width = 1400, height = 500,
                     range_y=[-1, 12])
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
    st.plotly_chart(fig)


elif tab == 'Ratings10':
    st.header("**Rating 10 Tab**")
    fig = px.scatter(df, x="Rating10", y="BoxOffice",
                     title ='A plot based on Ratings10 Ratings vs amount made on Box Office',
                     width = 1400,
                     height = 800)
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig)
else:
    st.header("**Rotten Tab**")
    fig = px.scatter(df, x="Rotten", y="BoxOffice",
                     title='A plot based on Ratten Ratings vs amount made on Box Office',
                     width=1400,
                     height=800)
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig)


#st.sidebar.subheader('3) Select by Rating')
#Rating = st.sidebar.slider('Select Rating', df.Rating10.min(), df.Rating10.max(), (df.Rating10.min(), df.Rating10.max()), 0.1)
#'Selected Year', Rating
