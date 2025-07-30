from bs4 import BeautifulSoup
import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = os.environ.get("SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
redirect_uri = "https://open.spotify.com/"


date = input("Which year you would like to travel to? Type the date in YYYY-MM-DD format ")


header ={
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64;rv:131.0) Gecko/20100101 Firefox/131.0"
}


URL = f"https://www.billboard.com/charts/hot-100/{date}"


response = requests.get(url=URL, headers=header)
content = response.text
soup = BeautifulSoup(content, "html.parser")
songs_list = soup.select("li ul li h3")
songs = [song.get_text().strip() for song in songs_list]
print(songs)


scope = "playlist-modify-private"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        redirect_uri=redirect_uri,
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt",
        username="asadullah"
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]

for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

# Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
