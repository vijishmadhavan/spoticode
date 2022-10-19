from colorthief import ColorThief
from PIL import Image
from pyparsing import Opt
import spotipy
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from PIL import ImageDraw
from PIL import ImageFont
import argparse
import textwrap



import os
import re
from urllib.request import urlopen



# function to convert RGB tuple to hex string.
def _rgb_to_hex(r,g,b):
    return '#%02x%02x%02x' % (r,g,b)




def get_art_with_code(uri, sp, text):
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
    music = Image.open("code/12.png")
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
    
    novo = textwrap.wrap(text, width=30)
    I1.text((227, 1728), novo[0],font=myFont, fill=(255, 255, 255))
    I1.text((227, 1852), novo[1],font=myFont, fill=(255, 255, 255))

    return music


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


def main():
    parser = argparse.ArgumentParser(description="Get Spotify album art with code")
    parser.add_argument(
        "-q",
        "--query",
        type=str,
        help="Search term to find album art",
    )
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        help="URL of album art to get",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output filename",
    )
    args = parser.parse_args()

    if not args.query and not args.url:
        parser.print_help()
        return

    if not args.output:
        if args.query:
            args.output = args.query + ".png"
        elif args.url:
            args.output = args.url.replace(":", "_") + ".png"

    if args.query:
        uri = uri_from_query(args.query, sp)
    elif args.url:
        uri = uri_from_url(args.url, sp)

    if uri:
        save_art_with_code(uri, sp, args.output)
    else:
        print("No results found")

if __name__ == "__main__":
    main()
