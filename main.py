import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = '8414b46ee2e74788a0119e21144de7e2'
CLIENT_SEC = '3eb88afccdc94806885d15814294e8bf'
OAUTH_TOKEN_URL= 'https://accounts.spotify.com/api/token'
URI = 'http://example.com'
SCOPE = 'playlist-modify-private'

auth_response = requests.post(OAUTH_TOKEN_URL, {
            "grant_type": "client_credentials",
            "client_id":CLIENT_ID,
            "client_secret":CLIENT_SEC,
    }
)

auth_response_data = auth_response.json()
access_token = auth_response_data["access_token"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=SCOPE,
    redirect_uri=URI,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SEC,
    show_dialog=True,
    cache_path=access_token
    )
)
user_id = sp.current_user()['id']

date = input('Where I should you take? Type date in YYY-MM-DD format ')
URL = f'https://www.billboard.com/charts/hot-100/{date}'

response = requests.get(URL)
website_list = response.text
soup = BeautifulSoup(website_list, 'html.parser')
titles = soup.findAll(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-"\
                                        "size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-"\
                                        "normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet"\
                                        "-only", id="title-of-a-story")
first_title = soup.find(name='a', class_="c-title__link lrv-a-unstyle-link").getText().strip()
titles_list = [title.getText().strip() for title in titles]
titles_list.append(first_title)
print(titles_list)

songs_uri = []
year = date.split('-')[0]
for title in titles_list:
    result = sp.search(q=f"track:{title} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uri.append(uri)
    except IndexError:
        continue