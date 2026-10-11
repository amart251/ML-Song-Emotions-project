import base64
import json
import os
import re
from pathlib import Path

import pandas as pd
import spotipy
from dotenv import load_dotenv
from requests import get, post
from spotipy import SpotifyClientCredentials

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

client_id = os.getenv("Client_ID")
client_secret = os.getenv("Client_secret")

if client_id and client_secret:
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
else:
    session = None


def get_uri(playlist_url):
    if not playlist_url:
        raise ValueError("Playlist URL is required.")

    match = re.search(r"https://open.spotify.com/playlist/([A-Za-z0-9]+)", playlist_url)
    if not match:
        raise ValueError("Expected format: https://open.spotify.com/playlist/...")
    return match.group(1)


def get_token():
    if not client_id or not client_secret:
        raise ValueError("Spotify credentials are missing. Set Client_ID and Client_secret in src/.env")

    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("UTF-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)

    if result.status_code != 200:
        raise RuntimeError(f"Spotify authentication failed: {result.status_code} {result.text}")

    json_result = result.json()
    if "access_token" not in json_result:
        raise KeyError("Spotify response did not include an access token.")

    return json_result["access_token"]


def get_playlist_tracks(token, playlist_id):
    headers = {"Authorization": "Bearer " + token}
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    tracks = []
    offset = 0

    while True:
        response = get(url, headers=headers, params={"offset": offset})
        if response.status_code != 200:
            raise RuntimeError(f"Spotify playlist request failed: {response.status_code} {response.text}")

        json_response = response.json()
        items = json_response.get("items", [])
        tracks.extend(items)

        if json_response.get("next"):
            offset += len(items)
        else:
            break

    return tracks


def get_track_features(token, track_id):
    headers = {"Authorization": "Bearer " + token}
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    response = get(url, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(f"Spotify audio-features request failed: {response.status_code} {response.text}")

    data = response.json()
    if not data:
        raise ValueError(f"No audio features returned for track {track_id}.")
    return data


def get_artist_genres(token, artist_id):
    headers = {"Authorization": "Bearer " + token}
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    response = get(url, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(f"Spotify artist request failed: {response.status_code} {response.text}")

    data = response.json()
    return data.get("genres", [])


def get_track_info(item, token):
    if not item:
        raise ValueError("Track item is missing.")

    track = item.get("track")
    if not track:
        raise ValueError("Track data is missing.")

    artist = track.get("artists", [{}])[0] if track.get("artists") else {}
    if not artist:
        raise ValueError(f"Artist data is missing for track {track.get('name', 'unknown')}.")

    track_features = get_track_features(token, track["id"])
    artist_genres = get_artist_genres(token, artist["id"])

    track_info = [
        track.get("name", ""),
        artist.get("name", ""),
        track.get("duration_ms", 0),
        ", ".join(artist_genres),
        track_features.get("tempo", 0),
        track_features.get("loudness", 0),
        track_features.get("energy", 0),
        track_features.get("danceability", 0),
        track_features.get("key", 0),
        track_features.get("instrumentalness", 0),
        track_features.get("valence", 0),
        track_features.get("acousticness", 0),
    ]
    return track_info


def format_track_data_for_csv(token, tracks):
    columns = [
        "track_name",
        "artist",
        "duration_ms",
        "genres",
        "tempo",
        "loudness",
        "energy",
        "danceability",
        "key",
        "instrumentalness",
        "valence",
        "acousticness",
    ]
    formatted_data = pd.DataFrame(columns=columns)

    for index, item in enumerate(tracks):
        formatted_data.loc[index] = get_track_info(item, token)

    return formatted_data
