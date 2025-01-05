import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_spotify_token():
    # Set your client ID and client secret here
    client_id = '85110bebacca48a6bc191414c25e5b36'
    client_secret = 'b089c708e59f4684a6b7064787ce2419'
    
    # Setup Spotify Client Credentials
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    # Get the access token
    token_info = sp.auth_manager.get_access_token()
    return token_info['access_token']
