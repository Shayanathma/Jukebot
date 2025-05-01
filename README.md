# 📀 JukeBot

JukeBot is a music chatbot that helps users explore music by providing song and artist recommendations, trending tracks, and detailed information—powered by the Spotify API.

## 🚀 Features:
- 🎵 Song and artist recommendations
- 📈 Trending music insights
- 🔍 Get details about albums, tracks, or artists
- 🤖 NLP-powered intent recognition using Logistic Regression + TF-IDF
- 🌐 Integrated with Spotify API for live data

## 🧪 How It Works:
The chatbot takes user input.
It classifies the intent using TF-IDF + Logistic Regression.
If the intent needs live data (e.g., "Tell me about the artist Post Malone?"), it fetches it from the Spotify API.
Otherwise, it returns a static predefined response from music_intents.json.

## 🤖 Technologies Used:
- Python
- Streamlit
- Spotipy (Spotify Web API wrapper)
- Scikit-learn – for ML model
- TF-IDF Vectorizer + Logistic Regression – for intent classification

## 🔐 Setup:
### 1. 🚥 Clone the Repository: 
    git clone https://github.com/your-username/jukebot.git
    cd jukebot

### 2. 📦 Install Required Packages:
    Make sure you're using a virtual environment (optional but recommended)
    python -m venv venv
    source venv/bin/activate   //For macOS/Linux
    venv\Scripts\activate      //For Windows

    Then install the dependencies:
    pip install -r requirements.txt

### 3. 🔐 Set Up Spotify Credentials:
    - To access Spotify data, you'll need API credentials from the Spotify Developer Dashboard.
    - Create a file named secrets.toml inside a .streamlit folder in the project root.
    - Add your credentials in this format:
        SPOTIPY_CLIENT_ID = "your_spotify_client_id"
        SPOTIPY_CLIENT_SECRET = "your_spotify_client_secret"

### 4. 🚀 Run the App
    Start the chatbot using Streamlit:
    streamlit run Jukebot.py

    Or to deploy from streamlit:
    https://jukebot.streamlit.app/

### 📝 NOTE:
This is a learning project and may not be fully refined.
For example, some user queries may not return ideal results if intent matching fails or Spotify returns incomplete metadata. Improvements are planned to make intent recognition and error handling more robust.

## Preview:
![Home page](<images/Home_page.png>)
![Conversation history page](<images/Conv_history.png>)


