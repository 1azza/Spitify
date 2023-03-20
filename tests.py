import spotify_dl

# Set the required environment variables
import os
os.environ["SPOTIPY_CLIENT_ID"] = "2eff2f0720d741649dd8e6f831af5412"
os.environ["SPOTIPY_CLIENT_SECRET"] = "f74c496921504da6a4f03a46e9fe0a70"

# Define the playlist link and download directory
playlist_link = "https://open.spotify.com/playlist/4IRfV6mMRCInZf956BPLaY?si=e007fef4e08b434e"
download_dir = "/path/to/download/directory"

os.system(f'spotify_dl -l {playlist_link} -o {download_dir}')
