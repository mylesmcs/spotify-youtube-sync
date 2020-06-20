import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import os
import json

os.environ["SPOTIPY_CLIENT_ID"]='0c8aca217f814a7590d37dadbe9a93c6'
os.environ["SPOTIPY_CLIENT_SECRET"]='473c8ffa7aa246c8b4ccf24a666cfc84'
os.environ["SPOTIPY_REDIRECT_URI"]='http://mylesmcsweeney.com'

scope = 'user-library-read playlist-modify-private'

token = util.prompt_for_user_token('milo', scope)

sp = spotipy.Spotify(auth=token)
sp.trace = False

# list of tracks to add
track_ids = []

# search track
track_seach_result = sp.search("dsdsdsadsfsdfsafdsfsa", limit=1, type='track')

try:
    track_ids.append(track_seach_result['tracks']['items'][0]['uri'])
except:
    pass

# add track to playlist
if track_ids:
    user_id = sp.me()['id']
    print(user_id)
    sp.user_playlist_add_tracks(user_id, '0RlQqSn3cpR0TnXriLnmtK',  track_ids)




#playlists = sp.user_playlists('milo')
#print(playlists)