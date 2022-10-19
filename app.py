import streamlit as st

from code.main import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image
from urllib.request import urlopen

option = st.selectbox('Select your choice of search',
('Song Name', 'Song URL'))

st.write('You selected:', option)

title = st.text_input('Search input based on option', '')
SongName = st.text_input('Song name/Name you would like to display', '')

sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(client_id="e6de42c45f314f1da04a9e63b0cdce5c", client_secret="f957f7dbd7db49de9d9af758941d4d85"))

if option == 'Song Name':
  uri = uri_from_query(title,sp)
elif option == 'Song URL':
  uri = uri_from_url(title, sp)

img = get_art_with_code(uri, sp, SongName)

im1 = img.save("geeks.png")

image = Image.open('geeks.png')

st.image(image, caption='Great!!')

