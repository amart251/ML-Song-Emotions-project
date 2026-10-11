# ML Song Emotions Project

A machine learning project that predicts song emotion from Spotify audio features such as tempo, energy, danceability, valence, loudness, and key.

This project combines music data collection, preprocessing, and neural network training to classify songs into mood categories such as happy, sad, calm, and hype.

## Why This Project

Music emotion recognition is a practical machine learning problem that sits at the intersection of audio analysis and recommendation systems. This project explores how musical attributes can be used to categorize songs by emotional tone and how those predictions can be generated in a repeatable, data-driven workflow.

## Features

- Spotify playlist-based dataset generation
- Track audio feature extraction from the Spotify API
- Data cleaning and preprocessing for machine learning
- Multilayer perceptron training for mood classification
- Prediction output saved as CSV files for evaluation
- Supporting project documentation and visual assets

## Emotional Categories

The project currently focuses on four classes:

- Happy
- Sad
- Calm
- Hype

## Project Structure

```text
ML-Song-Emotions-project/
├── docs/                               # Reports, diagrams, and presentation materials
├── lab data/
│   ├── training/                       # Labeled training datasets
│   └── testing/                       # Testing data and prediction outputs
├── src/
│   ├── spotify_integration.py         # Spotify API access and feature extraction
│   ├── data_formatting.py              # Playlist-to-dataset conversion
│   ├── neural_network_v2_final.py      # Model training and prediction workflow
│   ├── .env                            # Local Spotify credentials (keep private)
│   └── __pycache__/
├── README.md
├── .gitignore
└── .DS_Store
```

## Tech Stack

- Python
- pandas
- scikit-learn
- Spotipy
- python-dotenv
- Spotify Web API

## How the Pipeline Works

1. Spotify playlists are used as labeled mood datasets.
2. Track metadata and audio features are fetched from the Spotify API.
3. Data is cleaned and transformed into a structured machine-learning format.
4. The model is trained on labeled examples using a neural network.
5. Predictions are generated for test data and saved to a CSV file.

## Repository Highlights

- [src/spotify_integration.py](src/spotify_integration.py) handles authentication and Spotify track data extraction.
- [src/data_formatting.py](src/data_formatting.py) rebuilds training and testing datasets from Spotify playlists.
- [src/neural_network_v2_final.py](src/neural_network_v2_final.py) trains the classifier and saves predictions.
- [docs/](docs/) contains the project report, presentation materials, and visual examples.
- [lab data/](lab%20data/) stores the curated datasets used for model development.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/amart251/ML-Song-Emotions-project.git
cd ML-Song-Emotions-project
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

On Windows:

```powershell
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install pandas scikit-learn spotipy python-dotenv
```

### 4. Configure Spotify credentials

Create a local file at `src/.env`:

```env
Client_ID=your_spotify_client_id
Client_secret=your_spotify_client_secret
```

### 5. Run the training pipeline

```bash
python src/neural_network_v2_final.py
```

This will train the model and generate predictions using the dataset in `lab data/testing/`.

### 6. Regenerate datasets from Spotify playlists

```bash
python src/data_formatting.py
```

This fetches fresh track data from Spotify and writes new CSV files under the training/testing folders.

## Outputs

The model writes predictions to:

```text
lab data/testing/testData_predictions.csv
```

## Notes

- The project is designed for local experimentation and academic use.
- Keep Spotify credentials private and do not commit them to a public repository.
- The repository was improved to use safer path handling and more robust data/model processing logic.

## Documentation

Project documents and related artifacts are available in the [docs/](docs/) directory, including the report, presentation files, and sample visualizations.

