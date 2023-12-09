import pandas as pd
import spotify_integration


# Load data collected from Spotify
'''
This File should only be used if you want to use a different playlist and/or the 'lab data' is empty
'''

#https addresses for each of the playlists being used as datasets
emotion_playlists_https = [
    ["happy","https://open.spotify.com/playlist/7INcD4lmarWTQiDVodjVt4?si=cd599224ee7a45f9"],       #happy
    ["sad","https://open.spotify.com/playlist/27D7RiyuJnhmOIj2SUkTO8?si=118e5ec499b74709"],         #sad
    ["hype","https://open.spotify.com/playlist/1ey6i22I34wPgMuOQf97J0?si=cd58b6a1ded54a55"],        #hype
    ["calm","https://open.spotify.com/playlist/37i9dQZF1DX4TnpT6vw5rE?si=05b981350aea4841"]         #calm
]
test_playlist_https = ["test","https://open.spotify.com/playlist/3xZlWIpwy8wiIGe7kRDy8s?si=2383f1625ca54485"]

#Function used to create training and test datasets (should only be used once or twice)
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
    formatted_dataframe.to_csv("lab data/training/"+csv_df_filename)

formatted_dataframe, csv_df_filename = playlists_to_DF(test_playlist_https)
formatted_dataframe['emotion'] = ""
formatted_dataframe.to_csv("lab data/test/"+csv_df_filename)