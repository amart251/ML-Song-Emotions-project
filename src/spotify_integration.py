import base64
import json
import os
import re

import pandas as pd
import spotipy
from dotenv import load_dotenv
from requests import get, post
from spotipy import SpotifyClientCredentials

load_dotenv()

client_id = os.getenv("Client_ID")
client_secret = os.getenv("Client_secret")


# authenticate
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)

# create spotify session object
session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#Strips the uri from the spotify https address
def get_uri(playlist):
    if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", playlist):
            playlist_uri = match.groups()[0]
    else:
        raise ValueError("Expected format: https://open.spotify.com/playlist/...")
    return playlist_uri

#creates a token to access the specific spotify client and retrieve data
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("UTF-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_playlist_tracks(token, playlist_id):
    headers = {
        "Authorization": "Bearer " + token
    }
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    tracks = []
    offset = 0
    while True:
        response = get(url, headers=headers, params={'offset': offset})
        json_response = response.json()
        tracks.extend(json_response['items'])
        
        if 'next' in json_response and json_response['next']:
            offset += len(json_response['items'])
        else:
            break
    return tracks


def get_track_features(token, track_id):
    headers = {
        "Authorization": "Bearer " + token
    }
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    response = get(url, headers=headers)
    return response.json()

def get_artist_genres(token, artist_id):
    headers = {
        "Authorization": "Bearer " + token
    }
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    response = get(url, headers=headers)
    return response.json()["genres"]

'''
This Function was used only to see if we were able to access the API and load the data we want.
#
#def print_track_info(token, tracks):
#    for item in tracks['items']:
#        track = item['track']
#        print(f"Track Name: {track['name']}")
#        print(f"Artist: {track['artists'][0]['name']}")
#        print(f"Album: {track['album']['name']}")
#        print(f"Duration: {track['duration_ms']} ms")
#        
#       
#        print("\nTrack features:")
#        track_features = get_track_features(token, track['id'])
#        artist_genres = get_artist_genres(token, track['artists'][0]['id'])
#        print(f"Genres: {', '.join(artist_genres)}")
#        print(f"BPM/Tempo: {track_features['tempo']}")
#        print(f"Loudness: {track_features['loudness']}")
#        print(f"Energy: {track_features['energy']}")
#        print(f"danceability: {track_features['danceability']}")
#        print(f"key: {track_features['key']}")
#        print(f"instrumentalness: {track_features['instrumentalness']}")
#        print("\n------------------------")
'''

#Retrieves features of song from Spotify API and returns data as list that is then added to dataframe
def get_track_info(item, token):
    track = item['track']
    track_features = get_track_features(token, track['id'])
    artist_genres = get_artist_genres(token, track['artists'][0]['id'])

    track_info = [
        track['name'],
        track['artists'][0]['name'],
        #"album": track['album']['name'],
        track['duration_ms'],
        ', '.join(artist_genres),
        track_features['tempo'],
        track_features['loudness'],
        track_features['energy'],
        track_features['danceability'],
        track_features['key'],
        track_features['instrumentalness'],
        track_features['valence']
        #track_features['acousticnesss']  
    ]
    return track_info

#returns a dataframe containing all specified data in get_track_info() to caller function
def format_track_data_for_csv(token, tracks):
    formatted_data = pd.DataFrame(columns=["track_name", "artist","duration_ms","genres","tempo", "loudness","energy","danceability","key", "instrumentalness","valence","acousticnesss"])
    for i,item in enumerate(tracks):
        formatted_data.loc[i] = get_track_info(item, token)
        
    return formatted_data