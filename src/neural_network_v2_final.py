import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler


# load up and preprocess testing and training datasets
def load_and_preprocess_data(file_paths, columns_to_drop, encode_key=False):
    data_frames = [pd.read_csv(path) for path in file_paths]
    combined_data = pd.concat(data_frames).drop(columns=columns_to_drop) # get rid of unneeded columns (clean up)
    if encode_key:
        combined_data = pd.get_dummies(combined_data, columns=['key']) # one-hot encoding onto the 'key' feature (details in docs)
    return combined_data

# dataset preping
def prepare_datasets(combined_data):
    X = combined_data.drop('emotion', axis=1)   # features
    y = LabelEncoder().fit_transform(combined_data['emotion'])  # values
    scaler = StandardScaler().fit(X)        # normalize feature variables
    X_scaled = scaler.transform(X)
    return X_scaled, y, scaler, X.columns

# Train and evaluate the neural network model based on playlists of songs with a specific mood
def train_and_evaluate_model(X_scaled, y):
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)   # Splits training data into train and test sets

    # only one hidden layer of 100 neurons, adaptive learning rate, running on logistic (sigmoid) activation, 
    # kept the number of epochs to 2k, regularization rate is kept at default (0.001)
    mlp = MLPClassifier(hidden_layer_sizes=(100), learning_rate='adaptive', activation='logistic',
                        random_state=42, max_iter=2000, alpha=0.001) 
    mlp.fit(X_train, y_train)
    train_score, test_score = mlp.score(X_train, y_train), mlp.score(X_test, y_test) # model evaluation based on the training dataset
    print(f"Training score: {train_score}\nTesting score: {test_score}")
    return mlp

# Making predictions on the testing dataset from a playlist we created
def predict_and_save_new_data(model, scaler, feature_columns, test_data_path, output_path):
    test_data = pd.read_csv(test_data_path)
    test_data_processed = load_and_preprocess_data([test_data_path], columns_to_drop, encode_key=True)
    X_new_test = test_data_processed[feature_columns]   # separate the features in the csv to prepare for the prediction
    predictions = model.predict(scaler.transform(X_new_test))   # prediction is made here
    test_data['emotion'] = LabelEncoder().fit(combined_data['emotion']).inverse_transform(predictions)  # overwrite the emotion space with the prediction

    # get rid of features we don't need, clean up for readability
    metadata_columns = ['duration_ms', 'genres', 'tempo', 'loudness', 'energy', 'danceability', 'key', 'instrumentalness', 'valence']
    test_data.drop(columns=metadata_columns, inplace=True)
    test_data.to_csv(output_path, index=False)
    print("Predictions for test data have been saved into a new CSV file.")


# Define file paths and columns to drop (pre-pre-processing data, (cleaning up uneeded stuff))
file_paths = ['lab data/training/sadData.csv', 'lab data/training/calmData.csv', 
              'lab data/training/happyData.csv', 'lab data/training/hypeData.csv']
columns_to_drop = ['Unnamed: 0', 'track_name', 'artist', 'duration_ms', 'genres']

# Load and preprocess data
combined_data = load_and_preprocess_data(file_paths, columns_to_drop, encode_key=True)

# Prepare datasets
X_scaled, y, scaler, feature_columns = prepare_datasets(combined_data)

# Train and evaluate model (Start training!)
mlp_model = train_and_evaluate_model(X_scaled, y)

# Predict on new data and save results
test_data_path = 'lab data/testing/testData.csv'
output_path = 'lab data/testing/testData_predictions.csv'
predict_and_save_new_data(mlp_model, scaler, feature_columns, test_data_path, output_path)
