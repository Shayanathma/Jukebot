import streamlit as st

# Import functions and model from your main Jukebox code
from Jukebot import predict_intent, get_album_info, get_artist_info, get_song_info, get_trending_tracks, get_recommendations

# Streamlit app UI
st.title('Jukebox Music Bot')
st.write('Ask me about songs, albums, artists, trending tracks, or get recommendations!')

# User input field
user_input = st.text_input('You:', placeholder='Type your question here...')

# Submit button to process the input
if st.button('Submit'):
    if user_input:
        # Predict the intent of the user query
        intent = predict_intent(user_input)
        response = "I'm sorry, I didn't understand that."

        # Process the intent and generate a response
        if 'album' in intent.lower():
            album_name = user_input.split('album')[-1].strip()
            album_info = get_album_info(album_name)
            if album_info:
                response = f"Album: {album_info['name']}\nArtist: {album_info['artist']}\nRelease Date: {album_info['release_date']}\n[Listen here]({album_info['url']})"
        
        elif 'artist' in intent.lower():
            artist_name = user_input.split('artist')[-1].strip()
            artist_info = get_artist_info(artist_name)
            if artist_info:
                response = f"Artist: {artist_info['name']}\nGenres: {artist_info['genres']}\nFollowers: {artist_info['followers']}\n[Explore more]({artist_info['url']})"
        
        elif 'song' in user_input.lower():
            song_name = user_input.split('song')[-1].strip()
            song_info = get_song_info(song_name)
            if song_info:
                response = f"Song: {song_info['name']}\nArtist: {song_info['artist']}\nAlbum: {song_info['album']}\nRelease Date: {song_info['release_date']}\n[Listen here]({song_info['url']})"
        
        elif 'trending' in intent.lower():
            trending_tracks = get_trending_tracks()
            if trending_tracks:
                response = "Trending Tracks:\n"
                for track in trending_tracks:
                    response += f"- {track['name']} by {track['artist']} ([Listen]({track['url']}))\n"
        
        elif 'recommend' in intent.lower():
            genre = user_input.split('recommend')[-1].strip()
            recommendations = get_recommendations(genre)
            if recommendations:
                response = "Recommended Tracks:\n"
                for track in recommendations:
                    response += f"- {track['name']} by {track['artist']} ([Listen]({track['url']}))\n"

        # Display the chatbot response
        st.text_area("Jukebox Bot:", value=response, height=300)
