import streamlit as st
from code.main import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image
from urllib.request import urlopen
from io import BytesIO


sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(client_id="e6de42c45f314f1da04a9e63b0cdce5c", client_secret="f957f7dbd7db49de9d9af758941d4d85"))    


uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    ZipfileDotZip = get_art_with_xls(uploaded_file,sp)

    with open(ZipfileDotZip, "rb") as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f"<a href=\"data:file/zip;base64,{b64}\" download='{ZipfileDotZip}.zip'>\
            Click last model weights\
        </a>"
    st.sidebar.markdown(href, unsafe_allow_html=True)
