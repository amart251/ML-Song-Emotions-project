# Song emotion prediction using Machine Learning

The goal of our project is to predict the emotion or mood a song is portraying without listening to it.
We achieved this by training a Multi-layer perceptron model on the metadata of hundreds of songs.
This training and testing data was pulled from Spotify playlists associated with four specific emotions:
  - Happy
  - Sad
  - Hype (exciting)
  - Calm
    
  Potential applications:
  - Music recommendation systems
  - Music therapy
  - Personalized playlists

![image](https://github.com/user-attachments/assets/2f03c347-9a15-4d4e-af8c-38a333afd4f3)

---

## **Data Collection**

We collected data from Spotify playlists using the Spotify API.

###  Collected features:
  - **Danceability**: A measure of how suitable a track is for dancing based on tempo, rhythm stability, beat strength, and overall regularity.
  - **Energy**: A perceptual measure of intensity and activity, which can be related to the emotional intensity of a song.
  - **Tempo**: The overall estimated tempo of a track in beats per minute (BPM).
  - **Loudness**: The overall loudness of a track in decibels (dB).
  - **Key**: The key the track is in, which can sometimes correlate with certain emotions.
  - **Instrumental-ness**: Predicts whether a track contains no vocals, which might influence the emotional perception.
  - **Duration**: The length of the track might have a minor influence on the perceived emotion.

### Features collected but not considered for input:
  - **Track Name**: Sometimes the name of a track can give hints about its emotional content.
  - **Artist Name**: Knowing the artist can provide context, as some artists are known for certain emotional themes.
  - **Album Name**: Album names can sometimes reflect the overall mood of the songs within.
  - **Genre**: The genre(s) associated with the track, which can suggest common emotional themes.
  
```
    track_info = [
        track['name'],
        track['artists'][0]['name'],
        #"album": track['album']['name'],
        track['duration_ms'],
        ', '.join(artist_genres),
        track_features['tempo'],
        track_features['loudness'],
        track_features['energy'],
        track_features['danceability'],
        track_features['key'],
        track_features['instrumentalness'],
        track_features['valence']   
    ]
```
![image](https://github.com/user-attachments/assets/943d01eb-73a0-42ac-853b-e6b1e1e4690c)


We then normalized the features using the StandardScaler from sklearn to ensure that all features contribute equally to the model’s predictions.

---

## **Training Datasets**
  
![image](https://github.com/user-attachments/assets/0df78d98-dec9-4476-b568-0154c1edbe3e)
![image](https://github.com/user-attachments/assets/10677f50-39a2-4f5d-873b-1336e2d5ad3b)

---

## **Feature Criteria and Data Preprocessing**

Typical features of a song that we immediately notice
Scale of  0.0 to 1.0 for certain features
Key was based on the typical use in popular music of the genres
Talk about the scale of loudness and tempo along with their relationship between the two
Talk about what instrumental-ness is


| Feature      | Description |
| :---        |    :---   |
| Tempo     | The speed at which a passage of music is or should be played; Beats per minute      | 
| Loudness   | Values typically range between -60 and 0 db, with -60db being no sound and 0db being extremely loud        | 
| Energy  | A value of 0.0 is least danceable and 1.0 is most energetic. For example: Death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy       | 
| Danceability   | A value of 0.0 is least danceable and 1.0 is most danceable        | 
| Instrumental-ness   | 1.0 represents high confidence the track is acoustic        | 
| Key   | o	0 = C, 1 = C♯/D♭, 2 = D, 3 = D#/Eb, 4 = E, 5 = F, 6 = F#/Gb, 7 = G, 8 = G#/Ab, 9 = A, 10 = A#/Bb, 11 = B. If no key was detected, the value is -1        | 


Why energy and dancability are the same
  -	Made things a bit easier to keep them the same ranges as it would add too much complexity if they were separate.
    Could have been better to use one over the other but didn’t think of that till much later


![image](https://github.com/user-attachments/assets/51cc6e13-82ec-4985-a4cb-d7cf34502a4e)


We preprocessed the data by performing one-hot encoding for the ‘key’ feature and label encoding for the ‘emotion’ feature.

  -	One-hot encoding to treat each key as a distinct, independent attribute rather than just an incrementing value.
  -	Important because of their relation in conveying an emotion in a song
    
The "emotion" feature was label encoded, converting the emotion categories into numerical labels

Finally we normalize the wanted features using the StandardScaler from sklearn



---

## **Model Building and Training**

We chose the Multi-Layer Perceptron (MLP) classifier as our machine learning model.
 - Single hidden layer of size 100.
 - Trained over 2000 epochs until convergence.
 - Adaptive learning rate
 - Logistic (sigmoid) activation 
 - Alpha (regularization parameter) = 0.001

```
    # Define the MLP classifier
    mlp = MLPClassifier(hidden_layer_sizes=(100), # one hidden layer of 100 neurons
                        learning_rate='adaptive', # adaptive learning rate
                        activation='logistic',    # logistic (sigmoid) activation function
                        random_state=42,          # random state for reproducibility
                        max_iter=2000,            # maxiumim of 2000 iterations for the solver
                        alpha=0.001)              # regularisation parameter

    # Train the model on the scaled featrues and labels
    mlp.fit(X_train, y_train)
```

---

## **Model Evaluation and Testing Dataset**

The model’s performance was evaluated on both the training and testing data.

The training score achieved was 0.895734
  - Able to accurately predict the emotion of a song in approximately 89.57% of cases in the training set.
The testing score was 0.823899
  - The model accurately predicted the emotion of a song in approximately 82.39% of cases in the testing set.

```
# Evaluate the model
train_score = mlp.score(X_train, y_train)
test_score = mlp.score(X_test, t_test)

print(f"Training score: {train_score}\nTesting score: {test_score}")
```
![image](https://github.com/user-attachments/assets/af5fd6a2-f68d-471b-8916-e2c658a2f87c)



![image](https://github.com/user-attachments/assets/621479c2-e6d2-4256-a928-00e46ed4f98b)

When compared to manually categorized songs, the model had a largely successful rate at correctly predicting every song's conveyed emotion.
However, there were some songs that were not categorized accurately as shown above. This could be due to how Spotify possibly collects the 
data of its music possibly from the beginning of a song rather than analyzing the entirety of the composition.

---

## **Conclusion and Future Work**

Our project was successful in reaching our goal, with the bonus of high accuracy!

Recap:
  - The model was trained on data from Spotify playlists, each associated with a specific emotion: happy, sad, hype, and calm.
  - The training score and the testing score indicated that the model was performing well and was able to generalize to unseen/unaccounted data.

For future work, we could consider expanding the range of emotions, using more diverse datasets, or experimenting with different machine learning models to further improve the model’s performance.

---

## **References**

SciKit-Learn - https://scikit-learn.org/stable/modules/neural_networks_supervised.html
Spotify API - https://developer.spotify.com/documentation/web-api



