import requests
import json
import base64
from pprint import pprint
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path="venv/.env")
def find_result(TRACK_NAME, ARTIST_NAME):
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")

    base64_auth_string = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode("utf-8")).decode("utf-8")

    response = requests.post("https://accounts.spotify.com/api/token", data={"grant_type": "client_credentials"}, headers={"Authorization": f"Basic {base64_auth_string}"})
    response_json = response.json()
    access_token = response_json["access_token"]
    AUTH_TOKEN = access_token

    if ARTIST_NAME and TRACK_NAME:

        response = requests.get(f"https://api.spotify.com/v1/search?q={TRACK_NAME}+artist:{ARTIST_NAME}&type=track&limit=10",
                                headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
        if response.status_code == 200:
            TRACK_ID = response.json()["tracks"]["items"][0]["id"]
            response = requests.get(f"https://api.spotify.com/v1/tracks/{TRACK_ID}", headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
            response_json = response.json()

            song_name = response_json['name']
            artist = response_json['artists'][0]['name']
            album = response_json['album']['name']
            release_date = response_json['album']['release_date']
            URL = response_json['external_urls']['spotify']
            result = [song_name, artist, album, release_date, URL]
            return result
        else:
            print("Failed to retrieve tracks:", response.status_code)

    elif TRACK_NAME:
        # Search for artists with the given track name
        response = requests.get(f"https://api.spotify.com/v1/search?q={TRACK_NAME}&type=track&limit=20",
                                headers={"Authorization": f"Bearer {AUTH_TOKEN}"})

        if response.status_code == 200:
            response_json = response.json()

            result = []
            for item in response_json["tracks"]["items"]:
                track = item["name"]
                artist = item["artists"][0]["name"]
                album = item["album"]["name"]
                release_date = item["album"]["release_date"]
                URL = item["external_urls"]["spotify"]

                if track.lower() == TRACK_NAME.lower():
                    result.append((track, artist, album, release_date, URL))

            return result
        else:
            print("Failed to retrieve tracks:", response.status_code)

    elif ARTIST_NAME:
        # Search for albums by the artist
        response = requests.get(f"https://api.spotify.com/v1/search?q=artist:{ARTIST_NAME}&type=album&limit=10",
                                headers={"Authorization": f"Bearer {AUTH_TOKEN}"})

        response_json = response.json()

        artist_ids = []
        for album in response_json["albums"]["items"]:
            for artist in album["artists"]:
                artist_id = artist["id"]
                artist_ids.append(artist_id)

        artist_ids = list(set(artist_ids))


        # Use the artist's ID to search for albums by the artist
        album_tuples = []
        for item in artist_ids:
            response = requests.get(f"https://api.spotify.com/v1/artists/{item}/albums?include_groups=album&limit=50",
                                    headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
            response_json = response.json()

            for item in response_json["items"]:
                if item["artists"][0]["name"].lower() == ARTIST_NAME.lower():

                    # Extract the list of album names from the response
                    albums = response_json["items"]
                    album_names = [album["name"] for album in albums]

                    if len(album_names) == 0:
                        album_tuples.append(("No Album",))
                    else:
                        album_tuples.append(tuple(album_names))

                    artist = item["artists"][0]["name"]
                    URL = item["artists"][0]["external_urls"]["spotify"]
                    album_tuples = list(set(album_tuples))
                    result = [(artist, URL, album_tuples)]
                    return result



