import pandas as pd
import streamlit_app as st
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

import plotly.express as px 

from get_token import getToken
from get_data import getAudioFeatures, getAuthHeader, getPlaylistItems

def dataProcessing():
    data = pd.read_csv('dataset.csv')
    data
    st.write("## Preprocessing Result")  # streamlit widget

    data = data[['artist', 'name', 'year', 'popularity', 'key', 'mode', 'duration_ms', 'acousticness',
                'danceability', 'energy', 'instrumentalness', 'loudness', 'liveness', 'speechiness', 'tempo', 'valence']]
    data = data.drop(['mode'], axis=1)
    data['artist'] = data['artist'].map(lambda x: str(x)[2:-1])
    data['name'] = data['name'].map(lambda x: str(x)[2:-1])
    st.write("### Data to be deleted:")
    data[data['name'] == '']
    data = data[data['name'] != '']

    st.write("## Normalization Result")  # streamlit widget
    data2 = data.copy()
    data2 = data2.drop(
        ['artist', 'name', 'year', 'popularity', 'key', 'duration_ms'], axis=1)
    x = data2.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    data2 = pd.DataFrame(x_scaled)
    data2.columns = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                     'loudness', 'liveness', 'speechiness', 'tempo', 'valence']
    data2

    st.write("## Dimensionality Reduction with PCA")  # streamlit widget
    pca = PCA(n_components=2)
    pca.fit(data2)
    pca_data = pca.transform(data2)
    pca_df = pd.DataFrame(data=pca_data, columns=['x', 'y'])
    fig = px.scatter(pca_df, x='x', y='y', title='PCA')
    st.plotly_chart(fig)  # output plotly chart using streamlit

    st.write("## Clustering with K-Means")  # streamlit widget
    data2 = list(zip(pca_df['x'], pca_df['y']))
    kmeans = KMeans(n_init=10, max_iter=1000).fit(data2)
    fig = px.scatter(pca_df, x='x', y='y', color=kmeans.labels_,
                     color_continuous_scale='rainbow', hover_data=[data.artist, data.name])
    st.plotly_chart(fig)  # output plotly chart using streamlit

    st.write("Enjoy!")


# streamlit widgets
st.write("# Spotify Playlist Clustering")
client_id = st.text_input("Enter Client ID")
client_secret = st.text_input("Enter Client Secret")
playlistId = st.text_input("Enter Playlist ID")

# streamlit widgets
if st.button('Create Dataset!'):
    token = getToken()
    getPlaylistItems(token, playlistId)