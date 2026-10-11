from pathlib import Path

import pandas as pd

import spotify_integration

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRAINING_DIR = PROJECT_ROOT / "lab data" / "training"
TESTING_DIR = PROJECT_ROOT / "lab data" / "testing"

EMOTION_PLAYLISTS = [
    ["happy", "https://open.spotify.com/playlist/7INcD4lmarWTQiDVodjVt4?si=cd599224ee7a45f9"],
    ["sad", "https://open.spotify.com/playlist/27D7RiyuJnhmOIj2SUkTO8?si=118e5ec499b74709"],
    ["hype", "https://open.spotify.com/playlist/1ey6i22I34wPgMuOQf97J0?si=cd58b6a1ded54a55"],
    ["calm", "https://open.spotify.com/playlist/37i9dQZF1DX4TnpT6vw5rE?si=05b981350aea4841"],
]
TEST_PLAYLIST = ["test", "https://open.spotify.com/playlist/3xZlWIpwy8wiIGe7kRDy8s?si=2383f1625ca54485"]


def playlists_to_df(playlist):
    token = spotify_integration.get_token()
    playlist_uri = spotify_integration.get_uri(playlist[1])
    tracks = spotify_integration.get_playlist_tracks(token, playlist_uri)
    formatted_dataframe = spotify_integration.format_track_data_for_csv(token, tracks)
    csv_df_filename = f"{playlist[0]}Data.csv"
    return formatted_dataframe, csv_df_filename


def main():
    TRAINING_DIR.mkdir(parents=True, exist_ok=True)
    TESTING_DIR.mkdir(parents=True, exist_ok=True)

    for playlist in EMOTION_PLAYLISTS:
        formatted_dataframe, csv_df_filename = playlists_to_df(playlist)
        formatted_dataframe["emotion"] = playlist[0]
        formatted_dataframe.to_csv(TRAINING_DIR / csv_df_filename, index=False)

    formatted_dataframe, csv_df_filename = playlists_to_df(TEST_PLAYLIST)
    formatted_dataframe["emotion"] = ""
    formatted_dataframe.to_csv(TESTING_DIR / csv_df_filename, index=False)


if __name__ == "__main__":
    main()