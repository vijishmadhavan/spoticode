import streamlit as st
from code.main import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image,ImageOps
from urllib.request import urlopen
from io import BytesIO
import base64
import aspose.words as aw
from colorthief import ColorThief
from pyparsing import Opt
import spotipy
from spotipy.exceptions import SpotifyException
import tqdm
from PIL import ImageDraw
from PIL import ImageFont
import textwrap
import os
import re
from urllib.request import urlopen
from zipfile import ZipFile
import tempfile
import shutil






# function to convert RGB tuple to hex string.
def _rgb_to_hex(r,g,b):
    return '#%02x%02x%02x' % (r,g,b)

def readxl(path):
  import pandas as pd
  df = pd.read_excel(path)
  Upload_img	 = df["Upload Image crop"].tolist()
  Upload_img = [x for x in Upload_img if x == x]
  song_nm = df["Song Name"].tolist()
  song_nm = [x for x in song_nm if x == x]
  artist = df["Artist Name"].tolist()
  artist = [x for x in artist if x == x]
  return Upload_img,song_nm,artist

def get_dominant_color(pil_img):
    img = pil_img.copy()
    img = img.convert("RGBA")
    img = img.resize((1, 1), resample=0)
    dominant_color = img.getpixel((0, 0))
    return dominant_color



def get_art_with_code(uri, sp,text):
    try:
        if re.match(r"spotify:track:[A-Za-z0-9]{22}", uri):
            test = sp.track(uri)
            cover_uri = test["album"]["uri"]
            results = sp.album(cover_uri)

        elif re.match(r"spotify:artist:[A-Za-z0-9]{22}", uri):
            results = sp.artist(uri)

        elif re.match(r"spotify:album:[A-Za-z0-9]{22}", uri):
            results = sp.album(uri)
        else:
            return None
    except SpotifyException:
        return None

    cover_size = results["images"][0]["height"]
    link_to_cover = results["images"][0]["url"]

    cover_image = Image.open(urlopen(link_to_cover))

    # get dominant color from cover
    # this doesnt write to disc and still allows colorthief to grab most dominant color
    
    
    #with io.BytesIO() as file_object:
       #cover_image.save(file_object, "PNG")
        #cf = ColorThief(file_object)
        #dominant_color_rgb = cf.get_color(quality=1)

    dominant_color_hex = _rgb_to_hex(255,255,255)


    uri_call = uri.replace(":", "%3A")

    url = f"https://www.spotifycodes.com/downloadCode.php?uri=png%2F2B2A29%2Fwhite%2F640%2F{uri_call}"


    album_code = Image.open(urlopen(url))
    music = Image.open("12.png")
    # merge images
    final_height = album_code.size[1] + cover_size
    im = Image.new(mode="RGB", size=(cover_size, final_height))

    im.paste(cover_image, (0, 0))
    im.paste(album_code, (0, cover_size))

    im = im.resize((1352, 1576))

    
    #im = music.paste(im,(225,116,1577,1692),mask = im)
    Image.Image.paste(music, im, (225,116))

    I1 = ImageDraw.Draw(music)

    myFont = ImageFont.truetype('arial.ttf', 65)
    #texto = "Dil chahta hai koi mil gaya kolaveri in the world"
    novo = textwrap.wrap(text, width=30)
    I1.text((227, 1728), novo[0],font=myFont, fill=(255, 255, 255))
    I1.text((227, 1852), novo[1],font=myFont, fill=(255, 255, 255))

    return music


def uri_from_xls(path,sp):
  URI=[]
  Upload_img,song_nm,artist=readxl(path)
  for i in song_nm:
    uri = uri_from_query(i,sp)
    URI.append(uri)
  return URI


def get_art_with_xls(path,sp):
  Upload_img,song_nm,artist=readxl(path)
  uri = uri_from_xls(path,sp)
  cover_size = 640
  myFont = ImageFont.truetype('arial.ttf', 65)
  music = Image.open("12.png")
  try:
    shutil.rmtree("spotify", ignore_errors=False, onerror=None)
    os.remove("spotify.zip")
  except:
    pass
  os.makedirs("spotify")
  for i in Upload_img:
    for k in uri:
      cover_image = Image.open(urlopen(i))
      with cover_image as im:
         cover_image = ImageOps.pad(cover_image, (640, 640), color=(43,42,41))
      uri_call = k.replace(":", "%3A")
      url = f"https://www.spotifycodes.com/downloadCode.php?uri=png%2F2B2A29%2Fwhite%2F640%2F{uri_call}"
      album_code = Image.open(urlopen(url))
      final_height = album_code.size[1] + cover_size
      im = Image.new(mode="RGB", size=(cover_size, final_height))
      im.paste(cover_image, (0, 0))
      im.paste(album_code, (0, cover_size))
      im = im.resize((1352, 1576))
      m = music.copy()
      Image.Image.paste(m, im, (225,116))
      I1 = ImageDraw.Draw(m)
      I1.text((227, 1728), song_nm[Upload_img.index(i)],font=myFont, fill=(255, 255, 255))
      I1.text((233, 1864), artist[Upload_img.index(i)],font=myFont, fill=(255, 255, 255))
      m.save(f"spotify/{song_nm[Upload_img.index(i)]}.png")
      doc = aw.Document()
      builder = aw.DocumentBuilder(doc)
      builder.insert_image(f"spotify/{song_nm[Upload_img.index(i)]}.png")
      saveOptions = aw.saving.ImageSaveOptions(aw.SaveFormat.SVG)
      doc.save(f"spotify/{song_nm[Upload_img.index(i)]}.svg", saveOptions)
      #delete png
      os.remove(f"spotify/{song_nm[Upload_img.index(i)]}.png")
  zipObj = ZipFile('spotify.zip', 'w')
  for folderName, subfolders, filenames in os.walk('spotify'):
    for filename in filenames:
      filePath = os.path.join(folderName, filename)
      zipObj.write(filePath, os.path.basename(filePath))
    return "spotify.zip"


def save_art_with_code(uri, sp, filename):
    im = get_art_with_code(uri, sp)
    if im:
        im.save(filename)
        return True
    else:
        return False

def uri_from_query(search_term, sp):
    results = sp.search(search_term)
    if results["tracks"]["total"] > 0:
        return results["tracks"]["items"][0]["uri"]
    else:
        return None

def uri_from_url(search_url, sp):
    if re.match(r"spotify:track:[A-Za-z0-9]{22}", search_url):
        return search_url
    elif re.match(r"https://open.spotify.com/track/[A-Za-z0-9]{22}", search_url):
        return search_url.replace("https://open.spotify.com/track/", "spotify:track:")
    else:
        return None





sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(client_id="e6de42c45f314f1da04a9e63b0cdce5c", client_secret="f957f7dbd7db49de9d9af758941d4d85"))    


uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    ZipfileDotZip = get_art_with_xls(uploaded_file,sp)

    with open(ZipfileDotZip, "rb") as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f"<a href=\"data:file/zip;base64,{b64}\" download='{ZipfileDotZip}'>\
            Click last model weights\
        </a>"
    st.sidebar.markdown(href, unsafe_allow_html=True)
