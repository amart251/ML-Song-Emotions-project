import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load data from CSV files
sad_data_path = 'lab data/training/calmData.csv'
calm_data_path = 'lab data/training/calmData.csv'
happy_data_path = 'lab data/training/happyData.csv'
hype_data_path = 'lab data/training/hypeData.csv'

sad_data = pd.read_csv(sad_data_path)
calm_data = pd.read_csv(calm_data_path)
happy_data = pd.read_csv(happy_data_path)
hype_data = pd.read_csv(hype_data_path)

# Dropping unnecessary columns
columns_to_drop = ['Unnamed: 0', 'track_name', 'artist', 'duration_ms', 'genres']
sad_data = sad_data.drop(columns=columns_to_drop)
calm_data = calm_data.drop(columns=columns_to_drop)
happy_data = happy_data.drop(columns=columns_to_drop)
hype_data = hype_data.drop(columns=columns_to_drop)

# Combining datasets
combined_data = pd.concat([sad_data, calm_data, happy_data, hype_data])

# One-hot encoding for the 'Key' column
combined_data = pd.get_dummies(combined_data, columns=['key'])

# Encoding the 'emotion' column
label_encoder = LabelEncoder()
combined_data['emotion'] = label_encoder.fit_transform(combined_data['emotion'])

# Separating features and target variable
X = combined_data.drop('emotion', axis=1)
y = combined_data['emotion']

# Normalizing the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Defining the neural network architecture
    # increasd number of iterations from 1k to 2k, added a third hidden layer of 200, adjusted final hidden layer to 60
mlp = MLPClassifier(hidden_layer_sizes=(200, 50, 60), activation='relu', random_state=42, max_iter=2000, alpha = 0.001)

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


print("training score: ", train_score)
print("testing score: ",test_score)
