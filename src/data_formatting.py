import pandas as pd
from sklearn.model_selection import train_test_split

# Load data collected from Spotify
data = pd.read_csv('spotify_data.csv')

# Handling missing values
data.dropna(inplace=True)

# Reset index after dropping rows
data.reset_index(drop=True, inplace=True)

# Feature selection
selected_features = data[['tempo', 'loudness', 'energy', 'danceability', 'valence', 'key', 'mode']]

from sklearn.preprocessing import MinMaxScaler

# Normalize features
scaler = MinMaxScaler()
normalized_features = pd.DataFrame(scaler.fit_transform(selected_features), columns=selected_features.columns)

# Encoding categorical features if necessary
encoded_data = pd.get_dummies(normalized_features, columns=['key', 'mode'])

# Encoding labels
emotion_labels = pd.factorize(data['emotion'])[0]  # This maps each unique label to an integer


X_train, X_test, Y_train, Y_test = train_test_split(encoded_data, emotion_labels, test_size=0.2, random_state=42)

# Save preprocessed data to new CSV file for use in SciLab
preprocessed_data = pd.concat([X_train, Y_train], axis=1)  # Concatenate features and labels
preprocessed_data.to_csv('preprocessed_spotify_data.csv', index=False)