import spotipy
import streamlit as st
from spotipy.oauth2 import SpotifyClientCredentials

# Load credentials from Streamlit secrets
CLIENT_ID = st.secrets["SPOTIPY_CLIENT_ID"]
CLIENT_SECRET = st.secrets["SPOTIPY_CLIENT_SECRET"]

def get_spotify_token():
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    token_info = sp.auth_manager.get_access_token()
    return token_info['access_token']
