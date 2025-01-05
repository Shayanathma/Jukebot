import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotify_auth import get_spotify_token  # Import the function to get the token
from datetime import datetime  # Import datetime module for date formatting

# Load intents
with open('music_intents.json', 'r') as file:
    data = json.load(file)
    intents = data['intents']  # Access the 'intents' list

nltk.download('punkt')
nltk.download('stopwords')

# Preprocessing function
def preprocess_text(text):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words and word not in string.punctuation]
    return words

# Prepare data
all_words = []
class_labels = []

for intent in intents:
    for pattern in intent['patterns']:
        words = preprocess_text(pattern)
        all_words.extend(words)
        class_labels.append(intent['tag'])

all_words = sorted(list(set(all_words)))

vectorizer = TfidfVectorizer(vocabulary=all_words)
X = [" ".join(preprocess_text(pattern)) for intent in intents for pattern in intent['patterns']]
y = [intent['tag'] for intent in intents for _ in intent['patterns']]
X_tfidf = vectorizer.fit_transform(X)

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)

# Get Spotify token from spotify_auth.py
access_token = get_spotify_token()  # Fetch the token from spotify_auth.py

# Use the token to authenticate Spotify API requests
sp = spotipy.Spotify(auth=access_token)

# Predict intent
def predict_intent(user_input):
    user_input_tfidf = vectorizer.transform([user_input])
    prediction = model.predict(user_input_tfidf)
    return prediction[0]

# Date formatting function
def format_date(date_string):
    try:
        # Convert date string (yyyy-mm-dd) to dd-mm-yyyy
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        return date_obj.strftime('%d-%m-%Y')
    except Exception as e:
        print(f"Error formatting date: {e}")
        return date_string

# Spotify helpers
def get_audio_features(track_id):
    try:
        audio_features = sp.audio_features(track_id)[0]
        return {
            'danceability': audio_features['danceability'],
            'energy': audio_features['energy'],
            'key': audio_features['key'],
            'loudness': audio_features['loudness'],
            'mode': audio_features['mode'],
            'speechiness': audio_features['speechiness'],
            'acousticness': audio_features['acousticness'],
            'instrumentalness': audio_features['instrumentalness'],
            'liveness': audio_features['liveness'],
            'valence': audio_features['valence'],
            'tempo': audio_features['tempo'],
            'duration_ms': audio_features['duration_ms']
        }
    except Exception as e:
        print(f"Error fetching audio features: {e}")
        return None

def get_album_info(album_name):
    try:
        results = sp.search(q=album_name, type="album", limit=1)
        if results['albums']['items']:
            album = results['albums']['items'][0]
            album_info = {
                'name': album['name'],
                'artist': album['artists'][0]['name'],
                'release_date': format_date(album['release_date']),  # Format date
                'url': album['external_urls']['spotify']
            }
            return album_info
        else:
            return None
    except Exception as e:
        print(f"Error fetching album info: {e}")
        return None

def get_artist_info(artist_name):
    try:
        results = sp.search(q=artist_name, type="artist", limit=1)
        if results['artists']['items']:
            artist = results['artists']['items'][0]
            artist_info = {
                'name': artist['name'],
                'genres': ", ".join(artist['genres']),
                'followers': artist['followers']['total'],
                'url': artist['external_urls']['spotify']
            }
            return artist_info
        else:
            return None
    except Exception as e:
        print(f"Error fetching artist info: {e}")
        return None

def get_trending_tracks():
    try:
        results = sp.new_releases(limit=5)
        tracks = []
        for album in results['albums']['items']:
            tracks.append({
                'name': album['name'],
                'artist': album['artists'][0]['name'],
                'url': album['external_urls']['spotify']
            })
        return tracks
    except Exception as e:
        print(f"Error fetching trending tracks: {e}")
        return []

def get_recommendations(seed_genre):
    try:
        results = sp.recommendations(seed_genres=[seed_genre], limit=5)
        recommendations = []
        for track in results['tracks']:
            recommendations.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'url': track['external_urls']['spotify']
            })
        return recommendations
    except Exception as e:
        print(f"Error fetching recommendations: {e}")
        return []

def get_song_info(song_name):
    try:
        results = sp.search(q=song_name, type="track", limit=1)
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            song_info = {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'release_date': format_date(track['album']['release_date']),  # Format date
                'url': track['external_urls']['spotify']
            }
            return song_info
        else:
            return None
    except Exception as e:
        print(f"Error fetching song info: {e}")
        return None

# Chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        confirm = input("Jukebox: Are you sure you want to quit? (yes/no): ")
        if confirm.lower() == 'yes':
            print("Jukebox: Goodbye!")
            break
        else:
            continue

    intent = predict_intent(user_input)
    for intent_data in intents:
        if intent_data['tag'] == intent:
            response = intent_data['responses'][0]

            if 'album' in intent_data['tag'].lower():
                album_name = user_input.split('album')[-1].strip()
                album_info = get_album_info(album_name)
                if album_info:
                    print(f"Jukebox: Here's the info about '{album_info['name']}':")
                    print(f"Artist: {album_info['artist']}, Release Date: {album_info['release_date']}")
                    print(f"Listen here: {album_info['url']}")
                else:
                    print(f"Jukebox: Sorry, I couldn't find any information about the album '{album_name}'.")

            elif 'artist' in intent_data['tag'].lower():
                artist_name = user_input.split('artist')[-1].strip()
                artist_info = get_artist_info(artist_name)
                if artist_info:
                    print(f"Jukebox: Here's the info about '{artist_info['name']}':")
                    print(f"Genres: {artist_info['genres']}, Followers: {artist_info['followers']}")
                    print(f"Explore more: {artist_info['url']}")
                else:
                    print(f"Jukebox: Sorry, I couldn't find any information about the artist '{artist_name}'.")

            elif 'song' in user_input.lower():
                song_name = user_input.split('song')[-1].strip()
                song_info = get_song_info(song_name)
                if song_info:
                    print(f"Jukebox: Here's the info about the song '{song_info['name']}':")
                    print(f"Artist: {song_info['artist']}, Album: {song_info['album']}")
                    print(f"Release Date: {song_info['release_date']}")
                    print(f"Listen here: {song_info['url']}")
                else:
                    print(f"Jukebox: Sorry, I couldn't find any information about the song '{song_name}'.")

            elif 'audio features' in intent_data['tag'].lower():
                song_name = user_input.split('audio features')[-1].strip()
                song_info = get_song_info(song_name)
                if song_info:
                    track_id = song_info['url'].split('/')[-1]
                    audio_features = get_audio_features(track_id)
                    if audio_features:
                        print(f"Jukebox: Audio features for '{song_info['name']}':")
                        for feature, value in audio_features.items():
                            print(f"{feature.capitalize()}: {value}")
                    else:
                        print(f"Jukebox: Sorry, I couldn't fetch audio features for '{song_name}'.")
                else:
                    print(f"Jukebox: Sorry, I couldn't find any information about the song '{song_name}'.")

            elif 'trending' in intent_data['tag'].lower():
                trending_tracks = get_trending_tracks()
                if trending_tracks:
                    print("Jukebox: Here are the trending tracks:")
                    for track in trending_tracks:
                        print(f"- {track['name']} by {track['artist']} (Listen: {track['url']})")
                else:
                    print("Jukebox: Sorry, I couldn't fetch trending tracks right now.")

            elif 'recommend' in intent_data['tag'].lower():
                genre = user_input.split('recommend')[-1].strip()
                recommendations = get_recommendations(genre)
                if recommendations:
                    print(f"Jukebox: Here are some recommended tracks for '{genre}':")
                    for rec in recommendations:
                        print(f"- {rec['name']} by {rec['artist']} (Listen: {rec['url']})")
                else:
                    print(f"Jukebox: Sorry, I couldn't fetch recommendations for '{genre}'.")

            else:
                print(f"Jukebox: {response}")
            break