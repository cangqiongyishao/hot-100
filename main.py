from bs4 import BeautifulSoup
import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
id=os.getenv('CLIENT_ID')
cc=os.getenv('CLIENT_SECRET')

sp=spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope='playlist-modify-private',
        redirect_uri='http://example.com',
        client_id=id,
        client_secret=cc,
        show_dialog=True,
        cache_path='token.txt',
        username='xiao'
    )
)
user_id=sp.current_user()['id']



date=input('Which year do you want to travel to? Type the date in this format YYYY-MM-DD')

URL=f'https://www.billboard.com/charts/hot-100/{date}/'

response=requests.get(URL)
web=response.text
soup=BeautifulSoup(web,'html.parser')

song_uris=[]
year=date.split('-')[0]

names=[]
for tag in soup.select('li ul li h3'):
    names.append(tag.getText().strip())
print(names)

for song in names:
    result=sp.search(q=f'track:{song} year:{year}',type='track')
    try:
        uri=result['tracks']['items'][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
playlist=sp.user_playlist_create(user=user_id,name=f'{date} Billboard 100',public=False)
sp.playlist_add_items(playlist_id=playlist['id'],items=song_uris)
print(playlist)