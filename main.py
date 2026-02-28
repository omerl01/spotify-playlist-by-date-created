import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

date = input("what year you would like to travel to in YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"
CLIENT_ID = "YOUR_ID"
CLIENT_SECRET = "YOUR_SECRET"
REDIRECT_URL = "http://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                              client_secret=CLIENT_SECRET,
                              redirect_uri=REDIRECT_URL,
                              scope='playlist-modify-private',
                              show_dialog=True,
                              cache_path=".cache",
                              username="YOUR_USERNAME"
                              )
)

user_id = sp.current_user()["id"]

response = requests.get(URL)
webpage = response.text
soup = BeautifulSoup(webpage, "html.parser")

songs_name_spans = soup.select("li ul li h3")
songs_names = [song.getText().strip() for song in songs_name_spans]

songs_uris = []
year = date.split("-")[0]
for song in songs_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist_name = f"{date} Billboard 100"
playlist = sp.user_playlist_create(user_id, playlist_name, public=False)

sp.playlist_add_items(playlist["id"], songs_uris)
