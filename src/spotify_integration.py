import base64
import csv
import json
import os

from dotenv import load_dotenv
from requests import get, post

load_dotenv()

client_id = os.getenv("Client_ID")
client_secret = os.getenv("Client_secret")

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
    response = get(url, headers=headers)
    return response.json()
 
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
 
def print_track_info(token, tracks):
    for item in tracks['items']:
        track = item['track']
        print(f"Track Name: {track['name']}")
        print(f"Artist: {track['artists'][0]['name']}")
        print(f"Album: {track['album']['name']}")
        print(f"Duration: {track['duration_ms']} ms")
        
       
        print("\nTrack features:")
        track_features = get_track_features(token, track['id'])
        artist_genres = get_artist_genres(token, track['artists'][0]['id'])
        print(f"Genres: {', '.join(artist_genres)}")
        print(f"BPM/Tempo: {track_features['tempo']}")
        print(f"Loudness: {track_features['loudness']}")
        print(f"Energy: {track_features['energy']}")
        print(f"danceability: {track_features['danceability']}")
        print(f"key: {track_features['key']}")
        print(f"instrumentalness: {track_features['instrumentalness']}")
        print("\n------------------------")
 
token = get_token()
tracks = get_playlist_tracks(token, "3xZlWIpwy8wiIGe7kRDy8s")
print_track_info(token, tracks)

def format_track_data_for_csv(token, tracks):
    formatted_data = []
    for item in tracks['items']:
        track = item['track']
        track_features = get_track_features(token, track['id'])
        artist_genres = get_artist_genres(token, track['artists'][0]['id'])

        formatted_data.append({
            "track_name": track['name'],
            "artist": track['artists'][0]['name'],
            "album": track['album']['name'],
            "duration_ms": track['duration_ms'],
            "genres": ', '.join(artist_genres),
            "tempo": track_features['tempo'],
            "loudness": track_features['loudness'],
            "energy": track_features['energy'],
            "danceability": track_features['danceability'],
            "key": track_features['key'],
            "instrumentalness": track_features['instrumentalness']
        })
    return formatted_data

def write_to_csv(track_info, filename='filtered_outputs.csv'):
    fieldnames = [
        "track_name", "artist", "album", "duration_ms", "genres",
        "tempo", "loudness", "energy", "danceability", "key", "instrumentalness"
    ]

    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(track_info)

# Fetch and print track information
# token = get_token()
# tracks = get_playlist_tracks(token, "3xZlWIpwy8wiIGe7kRDy8s")
# print_track_info(token, tracks)

# Format track data and write it to the CSV file
formatted_data = format_track_data_for_csv(token, tracks)
#formatted_data.sort(key=lambda x: x['track_name'])  # Sort by track_name alphabetically

for track_info in formatted_data:
    write_to_csv(track_info)