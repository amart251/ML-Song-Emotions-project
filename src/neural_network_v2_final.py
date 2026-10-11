from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRAINING_DIR = PROJECT_ROOT / "lab data" / "training"
TESTING_DIR = PROJECT_ROOT / "lab data" / "testing"


def load_and_preprocess_data(file_paths, columns_to_drop=None, encode_key=False):
    columns_to_drop = columns_to_drop or []
    data_frames = [pd.read_csv(path) for path in file_paths]
    combined_data = pd.concat(data_frames, ignore_index=True)

    existing_columns = [column for column in columns_to_drop if column in combined_data.columns]
    combined_data = combined_data.drop(columns=existing_columns)

    if encode_key and "key" in combined_data.columns:
        combined_data = pd.get_dummies(combined_data, columns=["key"])

    return combined_data


def prepare_datasets(combined_data):
    if "emotion" not in combined_data.columns:
        raise ValueError("The dataset must include an 'emotion' column.")

    X = combined_data.drop(columns=["emotion"])
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(combined_data["emotion"])

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, y, scaler, list(X.columns), label_encoder


def train_and_evaluate_model(X_scaled, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    mlp = MLPClassifier(
        hidden_layer_sizes=(100,),
        learning_rate="adaptive",
        activation="logistic",
        random_state=42,
        max_iter=2000,
        alpha=0.001,
    )
    mlp.fit(X_train, y_train)

    train_score = mlp.score(X_train, y_train)
    test_score = mlp.score(X_test, y_test)
    print(f"Training score: {train_score}\nTesting score: {test_score}")
    return mlp


def predict_and_save_new_data(model, scaler, label_encoder, feature_columns, columns_to_drop, test_data_path, output_path):
    test_data = pd.read_csv(test_data_path)
    test_data_processed = load_and_preprocess_data([test_data_path], columns_to_drop, encode_key=True)

    aligned_features = test_data_processed.reindex(columns=feature_columns, fill_value=0.0)
    predictions = model.predict(scaler.transform(aligned_features))
    test_data["emotion"] = label_encoder.inverse_transform(predictions)

    metadata_columns = [
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
    for column in metadata_columns:
        if column in test_data.columns:
            test_data.drop(columns=[column], inplace=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    test_data.to_csv(output_path, index=False)
    print("Predictions for test data have been saved into a new CSV file.")


def main():
    file_paths = [
        TRAINING_DIR / "sadData.csv",
        TRAINING_DIR / "calmData.csv",
        TRAINING_DIR / "happyData.csv",
        TRAINING_DIR / "hypeData.csv",
    ]
    columns_to_drop = ["Unnamed: 0", "track_name", "artist", "duration_ms", "genres"]

    combined_data = load_and_preprocess_data(file_paths, columns_to_drop, encode_key=True)
    X_scaled, y, scaler, feature_columns, label_encoder = prepare_datasets(combined_data)
    mlp_model = train_and_evaluate_model(X_scaled, y)

    test_data_path = TESTING_DIR / "testData.csv"
    output_path = TESTING_DIR / "testData_predictions.csv"
    predict_and_save_new_data(
        mlp_model,
        scaler,
        label_encoder,
        feature_columns,
        columns_to_drop,
        test_data_path,
        output_path,
    )


if __name__ == "__main__":
    main()
