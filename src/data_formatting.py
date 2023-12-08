import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

import spotify_integration

# Load data collected from Spotify

emotion_playlists_https = [
    ["happy","https://open.spotify.com/playlist/7INcD4lmarWTQiDVodjVt4?si=cd599224ee7a45f9"],     #happy
    ["sad","https://open.spotify.com/playlist/27D7RiyuJnhmOIj2SUkTO8?si=118e5ec499b74709"],     #sad
    ["hype","https://open.spotify.com/playlist/1ey6i22I34wPgMuOQf97J0?si=cd58b6a1ded54a55"],     #hype
    ["calm","https://open.spotify.com/playlist/37i9dQZF1DX4TnpT6vw5rE?si=05b981350aea4841"]      #calm
]
test_playlist_https = ["test","https://open.spotify.com/playlist/3xZlWIpwy8wiIGe7kRDy8s?si=2383f1625ca54485"]

def playlists_to_csv(playlist, str):
    token = spotify_integration.get_token()
    pl_uri = spotify_integration.get_uri(playlist[1])
    tracks = spotify_integration.get_playlist_tracks(token, pl_uri)
    formatted_dataframe = spotify_integration.format_track_data_for_csv(token, tracks)
    formatted_dataframe['emotion'] = playlist[0]
    csv_df_filename = playlist[0] + "Data.csv"

    print(csv_df_filename)
    formatted_dataframe.to_csv("lab data/"+ str+"/"+csv_df_filename)


# Use this portion if training data is not included

for playlist in emotion_playlists_https:
   playlists_to_csv(playlist, "training")

playlists_to_csv(test_playlist_https,"test")




        

'''
def preprocess_spotify_data(fileName):

    data = pd.read_csv(fileName)

    # Handling missing values
    data.dropna(inplace=True)

    # Reset index after dropping rows
    data.reset_index(drop=True, inplace=True)

    # Feature selection
    selected_features = data[['tempo', 'loudness', 'energy', 'danceability', 'key','valence']]
    numerical_features = data[['tempo', 'loudness', 'energy', 'danceability', 'key','instrumentalness']]
    categorical_features = data[['genres']]


    # Normalize numerical features
    scaler = MinMaxScaler()
    normalized_features = pd.DataFrame(scaler.fit_transform(numerical_features), columns=numerical_features.columns)

    # Combine normalized numerical features and categorical features
    combined_features = pd.concat([normalized_features, categorical_features], axis=1)

    # Encoding categorical features if necessary
    encoded_data = pd.get_dummies(normalized_features)

    # Encoding labels
    print(data.columns)

    emotion_labels = data[['track_name','artist','album','genres']].apply(lambda x: pd.factorize(x)[0])  # This maps each unique label to an integer



    X_train, X_test, Y_train, Y_test = train_test_split(encoded_data, emotion_labels, test_size=0.2, random_state=42)




# Save preprocessed data to new CSV file for use in SciLab
preprocessed_data = pd.concat([X_train, Y_train], axis=1)  # Concatenate features and labels
preprocessed_data.to_csv('preprocessed_spotify_data.csv', index=False)

'''
import pandas as pd
import spotify_integration
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


# Load data collected from Spotify

emotion_playlists_https = [
    ["happy","https://open.spotify.com/playlist/37i9dQZF1EIerWLYY5lG2u?si=4cfeb4299fff4bfd"],     #happy
    ["sad","https://open.spotify.com/playlist/37i9dQZF1EIdChYeHNDfK5?si=f8435148b32b457b"],     #sad
    ["hype","https://open.spotify.com/playlist/37i9dQZF1EIgzSCNweQzPQ?si=57e1261b474847bd"],     #hype
    ["calm","https://open.spotify.com/playlist/37i9dQZF1EIfS9ikr4OHrn?si=af38606beb9641e7"]      #calm
]
test_playlist_https = ["test","https://open.spotify.com/playlist/3xZlWIpwy8wiIGe7kRDy8s?si=50ef75bcef81498b"]

def playlists_to_DF(playlist):
    token = spotify_integration.get_token()
    pl_uri = spotify_integration.get_uri(playlist[1])
    tracks = spotify_integration.get_playlist_tracks(token, pl_uri)
    formatted_dataframe = spotify_integration.format_track_data_for_csv(token, tracks)
    csv_df_filename = playlist[0] + "Data.csv"

    print(csv_df_filename)

    return formatted_dataframe, csv_df_filename


# Use this portion if training data is not included
formatted_dataframe, csv_df_filename = pd.DataFrame(), ""

for playlist in emotion_playlists_https:
    formatted_dataframe, csv_df_filename = playlists_to_DF(playlist)
    formatted_dataframe['emotion'] = playlist[0]
    formatted_dataframe.to_csv(csv_df_filename)

formatted_dataframe, csv_df_filename = playlists_to_DF(test_playlist_https)
formatted_dataframe.to_csv(csv_df_filename)





        

'''
def preprocess_spotify_data(fileName):

    data = pd.read_csv(fileName)

    # Handling missing values
    data.dropna(inplace=True)

    # Reset index after dropping rows
    data.reset_index(drop=True, inplace=True)

    # Feature selection
    selected_features = data[['tempo', 'loudness', 'energy', 'danceability', 'key','valence']]
    numerical_features = data[['tempo', 'loudness', 'energy', 'danceability', 'key','instrumentalness']]
    categorical_features = data[['genres']]


    # Normalize numerical features
    scaler = MinMaxScaler()
    normalized_features = pd.DataFrame(scaler.fit_transform(numerical_features), columns=numerical_features.columns)

    # Combine normalized numerical features and categorical features
    combined_features = pd.concat([normalized_features, categorical_features], axis=1)

    # Encoding categorical features if necessary
    encoded_data = pd.get_dummies(normalized_features)

    # Encoding labels
    print(data.columns)

    emotion_labels = data[['track_name','artist','album','genres']].apply(lambda x: pd.factorize(x)[0])  # This maps each unique label to an integer



    X_train, X_test, Y_train, Y_test = train_test_split(encoded_data, emotion_labels, test_size=0.2, random_state=42)




# Save preprocessed data to new CSV file for use in SciLab
preprocessed_data = pd.concat([X_train, Y_train], axis=1)  # Concatenate features and labels
preprocessed_data.to_csv('preprocessed_spotify_data.csv', index=False)

'''