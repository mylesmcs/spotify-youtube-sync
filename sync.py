from googleapiclient.discovery import build
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
from dotenv import load_dotenv
import json
import time
import os


load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
PLAYLIST = os.getenv("USER_PLAYLIST")

service = build('youtube', 'v3', developerKey=API_KEY)


# query a specific playlist for all videos
def playlist_query(page=''):
    request = service.playlistItems().list(
        part='contentDetails',
        maxResults=5,
        pageToken=f'{page}',
        playlistId=f'{PLAYLIST}'
    )
    return request.execute()


# query a video using it's id
def video_query(id):
    request = service.videos().list(
        part='snippet',
        id=f'{id}'
    )
    return request.execute()

def write_video_list(video_list):
    with open('video-list.txt', 'w') as f:
        for title in video_list:
            f.write(f"{title}\n")


if os.path.exists('video-list.txt'):
    pass
else:
    response = playlist_query()

    video_titles = []

    while "nextPageToken" in response:
        for video in response['items']:
            video_id = json.dumps(video['contentDetails']['videoId']).replace("\"","")
            try:
                video_titles.append(video_query(video_id)['items'][0]['snippet']['title'])
            except:
                pass
        response = playlist_query(page=response['nextPageToken'])
    write_video_list(video_titles)



scope = 'user-library-read playlist-modify-private'

token = util.prompt_for_user_token('milo', scope)

sp = spotipy.Spotify(auth=token)
sp.trace = False

# list of tracks to add
track_ids = []

def load_videos():
    with open('video-list.txt', 'r') as f:
        titles = []
        line = f.readline()
        while line:
            titles.append(line)
            line = f.readline()
        f.close()
        return titles


for title in load_videos():
    track_seach_result = sp.search(f"{title}", limit=1, type='track')
    try:
        track_id = track_seach_result['tracks']['items'][0]['uri']
        print(f"{track_id} ---- {title}")
        track_ids.append(track_id)
    except:
        pass

# add track to playlist
if track_ids:
    user_id = sp.me()['id']
    if len(track_ids) >= 100:
        final = [track_ids[i * 100:(i + 1) * 100] for i in range((len(track_ids) + 100 - 1) // 100 )]
        for x in final:
            sp.user_playlist_add_tracks(user_id, '0RlQqSn3cpR0TnXriLnmtK', x)
    else:
        sp.user_playlist_add_tracks(user_id, '0RlQqSn3cpR0TnXriLnmtK',  track_ids)
    
    




#playlists = sp.user_playlists('milo')
#print(playlists)