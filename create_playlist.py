import sys
import spotipy
import discogs_client
import yaml
import spotipy.util as util
from pprint import pprint




def load_config():
    global user_config
    stream = open('config.yaml')
    user_config = yaml.load(stream)
    # pprint(user_config)

def get_song_by_artist_title_search(artistName, trackName):
    song_id = []
    q = format("artist:%s track:%s" % (artistName, trackName))
    song_results = sp.search(q=q, type='track', limit=1)
    try:
        return song_results['tracks']['items'][0]['id']
    except:
        return False

def get_top_songs_for_artist(artist, song_count=1):
    song_ids = []
    artist_results = sp.search(q='artist:' + artist, type='artist', limit=1)
    # pprint(artist_results)

    if artist_results['artists']['total']:
        artist_id = artist_results['artists']['items'][0]['id']
        # pprint(artist_id)
        artist_top_tracks = sp.artist_top_tracks(artist_id)
        artist_top_tracks_length = len(artist_top_tracks['tracks'])
        for x in range(0, artist_top_tracks_length if song_count > artist_top_tracks_length else song_count ):
            song_ids.append(artist_top_tracks['tracks'][x]['id'])
            # pprint(artist_top_tracks['tracks'][x])
            print(str(len(song_ids)) + ' songs found - ' + artist)
    else:
        print('Artist not found - ' + artist)
        # pprint(song_ids)
    return song_ids

def create_new_playlist(username, playlist_name, playlist_description):
    playlists = sp.user_playlist_create(username, playlist_name, public=False, description=playlist_description)

def get_wacken_tracks():
    artists = [
        'Can',
        'Shadow Band'
    ]

    all_track_ids = []
    for i, current_artist in enumerate(artists):
        api_track_add_limit = 100
        top_song_limit_per_artist = 2
        top_artist_songs = get_top_songs_for_artist(current_artist, top_song_limit_per_artist)
        if len(top_artist_songs):
            all_track_ids.extend(top_artist_songs)
        if len(all_track_ids)+ top_song_limit_per_artist > api_track_add_limit or (i == len(artists)-1 and len(all_track_ids)):
            sp.user_playlist_add_tracks(user=user_config['spotify_username'], playlist_id=user_config['spotify_playlist_id'], tracks=all_track_ids)
            all_track_ids = []

def add_track_to_playlist(track_id):
    track_list = []
    track_list.append(track_id)
    sp.user_playlist_add_tracks(user=user_config['spotify_username'], playlist_id=user_config['spotify_playlist_id'],tracks=track_list)

if __name__ == '__main__':
    global sp
    global user_config
    load_config()


TRACKLIST = [["O.V. Wright", "Thats How Strong"],["Wendy Rene","After Laughter"],["asfasdf","asdfsadf"],["Don Covay","Come See About Me"]]
token = util.prompt_for_user_token(user_config['spotify_username'], scope='playlist-modify-private,playlist-modify-public', client_id=user_config['spotify_client_id'], client_secret=user_config['spotify_client_secret'], redirect_uri=user_config['spotify_redirect_uri'])

if token:
    sp = spotipy.Spotify(auth=token)
    for t in TRACKLIST:
        track_id = get_song_by_artist_title_search(t[0], t[1])
        if track_id:
            add_track_to_playlist(track_id)
    # get_wacken_tracks()
else:
    print ("Can't get token for", user_config['spotify_username'])