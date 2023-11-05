import math

import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from spotify_integration import (get_artist_genres, get_playlist_tracks,
                                 get_token, get_track_features)


## just keep in mind this is a template or starter code, needs more refinement
def fetch_and_prepare_data(playlist_id):
    # Authenticate with Spotify
    token = get_token()
    
    # Fetch tracks from the playlist
    tracks = get_playlist_tracks(token, playlist_id)
    
    # Initialize lists to store features and labels
    features = []
    labels = []
    
    # Loop over tracks and fetch data
    for item in tracks['items']:
        track_data = {}
        track = item['track']
        
        # Fetch track metadata
        track_data['track_name'] = track['name']
        track_data['artist_name'] = track['artists'][0]['name']
        track_data['album_name'] = track['album']['name']
        
        # Fetch audio features
        audio_features = get_track_features(token, track['id'])
        track_data['danceability'] = audio_features['danceability']
        track_data['energy'] = audio_features['energy']
        # add all other audio features
        
        # Fetch artist genres
        artist_genres = get_artist_genres(token, track['artists'][0]['id'])
        track_data['genres'] = artist_genres
        
        # Add the track data to the features list
        features.append(track_data)
        
        # For the labels, we would need to define how we obtaining them
        # if we have a mood label for each track, append it here
        # labels.append(mood_label)

    # Convert features and labels to a suitable format for the neural network
    # This might include one-hot encoding for categorical data and scaling for numerical data
    
    # Return the prepared dataset
    return features, labels

# Example usage:
# playlist_id = 'your_playlist_id_here'
# X, y = fetch_and_prepare_data(playlist_id)
