import pandas as pd
from requests import post, get
import json
import csv

from get_token import getToken

# Extract Data  
playlistId = '0IN7IWKmIfwlEysGyWUuRg'

dataset = []
dataset2 = []
dataset3 = []

def getAuthHeader(token):
    return {"Authorization" : "Bearer " + token}

def getAudioFeatures(token, trackId):
    
    url = f'https://api.spotify.com/v1/audio-features/{trackId}'
    
    headers = getAuthHeader(token)
    result = get(url, headers=headers)  
    json_result = json.loads(result.content)  


    audio_features_temp = [
        json_result['danceability'],
        json_result['energy'],
        json_result['key'],
        json_result['loudness'],
        json_result['mode'],
        json_result['speechiness'],
        json_result['acousticness'],
        json_result['instrumentalness'],
        json_result['liveness'],
        json_result['valence'],
        json_result['tempo'],
    ]
    dataset2.append(audio_features_temp)


def getPlaylistItems(token, playlistId):
    
    url = f'https://api.spotify.com/v1/playlists/{playlistId}/tracks'
    limit = '&limit=100'  
    market = '?market=ID'  
    
    fields = '&fields=items%28track%28id%2Cname%2Cartists%2Cpopularity%2C+duration_ms%2C+album%28release_date%29%29%29'
    url = url+market+fields+limit  
    
    headers = getAuthHeader(token)
    result = get(url, headers=headers)  
    json_result = json.loads(result.content)  
    # print(json_result)


    for i in range(len(json_result['items'])):
        playlist_items_temp = []
        playlist_items_temp.append(json_result['items'][i]['track']['id'])
        playlist_items_temp.append(
            json_result['items'][i]['track']['name'].encode('utf-8'))
        playlist_items_temp.append(
            json_result['items'][i]['track']['artists'][0]['name'].encode('utf-8'))
        playlist_items_temp.append(
            json_result['items'][i]['track']['popularity'])
        playlist_items_temp.append(
            json_result['items'][i]['track']['duration_ms'])
        playlist_items_temp.append(
            int(json_result['items'][i]['track']['album']['release_date'][0:4]))
        dataset.append(playlist_items_temp)

    
    for i in range(len(dataset)):
        getAudioFeatures(token, dataset[i][0])

   
    for i in range(len(dataset)):
        dataset3.append(dataset[i]+dataset2[i])

    print(dataset3)
    
    with open('dataset.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "artist", "popularity", "duration_ms", "year", "danceability", "energy", "key", "loudness", "mode",
                         "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"])
        writer.writerows(dataset3)




if __name__ == "__main__":
    token = getToken()
    print('access token : '+token)
    getPlaylistItems(token, playlistId)


