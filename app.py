from flask import Flask, request, url_for, session, redirect, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import time 
import requests

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

app = Flask(__name__)

app.secret_key = "aN32fgns43cdNo"
app.config["SESSION_COOKIE_NAME"] = 'My Journal'
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external=True))

@app.route('/get-tracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect("/")
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    playlists = sp.current_user_playlists()
    all_playlists = []
    
    for playlist in playlists['items']:
        playlist_id = playlist['id']
        playlist_name = playlist['name']
        
        tracks = sp.playlist_tracks(playlist_id)
        playlist_tracks = []
        
        for track in tracks['items']:
            track_name = track['track']['name']
            artist_name = track['track']['artists'][0]['name']
            track_id = track['track']['id']
            track_images = track['track']['album']['images']
            
            playlist_tracks.append({
                'name': track_name,
                'artist': artist_name,
                'id': track_id,
                'images': track_images
            })
        
        all_playlists.append({
            'name': playlist_name,
            'tracks': playlist_tracks
        })
    
    return str(all_playlists)

@app.route('/get-events', methods=['GET'])
def get_events():
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    api_key = "0w9wJgajLh6QfnKltKFyIg8A7M5nkE7D"

    # Define the allowed query parameters
    allowed_params = {
        'size', 'id', 'keyword', 'attractionId', 'venueId', 'postalCode',
        'latlong', 'radius', 'unit', 'source', 'locale', 'marketId',
        'startDateTime', 'endDateTime', 'includeTBA', 'includeTBD',
        'includeTest', 'sort', 'onsaleStartDateTime', 'onsaleEndDateTime',
        'city', 'countryCode', 'stateCode', 'classificationName',
        'classificationId', 'dmaId', 'localStartDateTime',
        'localStartEndDateTime', 'startEndDateTime',
        'publicVisibilityStartDateTime', 'preSaleDateTime',
        'onsaleOnStartDate', 'onsaleOnAfterStartDate',
        'collectionId', 'segmentId', 'segmentName', 'includeFamily',
        'promoterId', 'genreId', 'subGenreId', 'typeId', 'subTypeId',
        'geoPoint', 'preferredCountry', 'includeSpellcheck', 'domain'
    }

    # Get query parameters from the request
    params = request.args.to_dict()

    # Filter out any parameters that are not allowed
    params = {key: params[key] for key in params if key in allowed_params}

    # Add the API key to the parameters
    params['apikey'] = api_key

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Error fetching events'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recently-played')
def getRecentlyPlayed():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect("/")
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    # Fetch recently played tracks
    recently_played = sp.current_user_recently_played(limit=10)  # Limit to 10 tracks
    
    return str(recently_played)


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = "4cc452c2ffbe46529870e8eacefc0e5c",
        client_secret = "3062ad55a2464af2b1c807af68d83883",
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read user-read-recently-played"
    )

