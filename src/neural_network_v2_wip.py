import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load data from CSV files
sad_data_path = 'lab data/training/sadData.csv'
calm_data_path = 'lab data/training/calmData.csv'
happy_data_path = 'lab data/training/happyData.csv'
hype_data_path = 'lab data/training/hypeData.csv'
test_data_path = 'lab data/testing/testData.csv'

sad_data = pd.read_csv(sad_data_path)
calm_data = pd.read_csv(calm_data_path)
happy_data = pd.read_csv(happy_data_path)
hype_data = pd.read_csv(hype_data_path)
test_data = pd.read_csv(test_data_path)

# Dropping unnecessary columns
columns_to_drop = ['Unnamed: 0', 'track_name', 'artist', 'duration_ms', 'genres']
sad_data = sad_data.drop(columns=columns_to_drop)
calm_data = calm_data.drop(columns=columns_to_drop)
happy_data = happy_data.drop(columns=columns_to_drop)
hype_data = hype_data.drop(columns=columns_to_drop)

test_data = test_data.drop(columns=columns_to_drop)

# Combining datasets
combined_data = pd.concat([sad_data, calm_data, happy_data, hype_data])

# One-hot encoding for the 'Key' column
combined_data = pd.get_dummies(combined_data, columns=['key'])
test_data = pd.get_dummies(test_data, columns=['key'])


# Encoding the 'emotion' column
label_encoder = LabelEncoder()
combined_data['emotion'] = label_encoder.fit_transform(combined_data['emotion'])
#test_data['emotion'] = label_encoder.transform(test_data['emotion'])  # Encoding 'emotion' column


# Separating features and target variable
X = combined_data.drop('emotion', axis=1)
y = combined_data['emotion']

X_new_testing = test_data
#y_new_testing = test_data['emotion']

# List of column names
cols = X.columns

# Ensure that X_new_testing only contains the same columns as X
X_new_testing = X_new_testing[cols]


# Normalizing the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_new_test_scaled = scaler.transform(X_new_testing)  # Use the same scaler fit on training data


# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)


# Defining the neural network architecture
    # increasd number of iterations from 1k to 2k, added a third hidden layer of 200, adjusted final hidden layer to 60
    # decreased hidden layer to 100, added learning rate to be adaptive, changed activation to be logistic (sigmoid), changed normalization rate to 0.001
mlp = MLPClassifier(hidden_layer_sizes=(100), learning_rate='adaptive', activation='logistic', random_state=42, max_iter=2000, alpha = 0.001)

"""
# Implementing cross-validation on the adjusted model with the new data
cv_scores_adjusted = cross_val_score(mlp, X_scaled, y, cv=5)

# Calculating the mean cross-validation score for the adjusted model
mean_cv_score_adjusted = cv_scores_adjusted.mean()
"""

# Training the model on the training data
mlp.fit(X_train, y_train)



# Evaluating the model on the test data
train_score = mlp.score(X_train, y_train)
test_score = mlp.score(X_test, y_test)
# new_test_score = mlp.score(X_new_test_scaled)


print("training score: ", train_score)
print("testing score: ",test_score)
# print("testing score from playlist: ", new_test_score)

# Making predictions on the new test data
predictions = mlp.predict(X_new_test_scaled)

# Transform predictions back to original labels
predictions_labels = label_encoder.inverse_transform(predictions)

# Load the original testing data CSV into a DataFrame
test_data_original = pd.read_csv(test_data_path)

# Create a copy of the original DataFrame
test_data_copy = test_data_original.copy()

# Write over the 'Emotion' column with the predictions in the copied DataFrame
test_data_copy['emotion'] = predictions_labels

# Save the modified DataFrame back to a new CSV file
test_data_copy.to_csv('lab data/testing/testData_copy.csv', index=False)

# Write over the 'Emotion' column with the predictions
test_data_original['emotion'] = predictions_labels

# Save the modified DataFrame back to the CSV file
test_data_original.to_csv(test_data_path, index=False)

print("Predictions for new test data have been saved to the CSV file.")
