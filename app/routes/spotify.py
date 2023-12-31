from flask import Blueprint, request, url_for, session, redirect, jsonify, current_app
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time 
import requests

spotify = Blueprint('spotify', __name__)
TOKEN_INFO = current_app.config['TOKEN_INFO']
TICKET_MASTER_API_KEY = current_app.config['TICKET_MASTER_API_KEY']
CLIENT_ID = current_app.config['CLIENT_ID']
CLIENT_SECRET = current_app.config['CLIENT_SECRET']

@spotify.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@spotify.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external=True))

@spotify.route('/get-tracks')
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

@spotify.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external=True))

@spotify.route('/get-top-artists')
def getTopArtists():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect("/")
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    top_artists = sp.current_user_top_artists()
    
    return top_artists

#to do: get-attraction and get-attraction details
@spotify.route('/get-artists', methods=['GET'])
def get_artists():
    url = "https://app.ticketmaster.com/discovery/v2/attractions.json"
    api_key = TICKET_MASTER_API_KEY

    # Define the allowed query parameters
    allowed_params = {
        'id': str,  # Filter entities by its id
        'keyword': str,  # Keyword to search on
        'source': str,  # Filter entities by its primary source name OR publishing source name
        'locale': str,  # The locale in ISO code format
        'includeTest': str,  # Entities flagged as test in the response
        'size': str,  # Page size of the response
        'page': str,  # Page number
        'sort': str,  # Sorting order of the search result
        'classificationName': list,  # Filter attractions by classification name (array)
        'classificationId': list,  # Filter attractions by classification id (array)
        'includeFamily': str,  # Filter by classification that are family-friendly
        'segmentId': list,  # Filter attractions by segmentId (array)
        'genreId': list,  # Filter attractions by genreId (array)
        'subGenreId': list,  # Filter attractions by subGenreId (array)
        'typeId': list,  # Filter attractions by typeId (array)
        'subTypeId': list,  # Filter attractions by subTypeId (array)
        'preferredCountry': str,  # Popularity boost by country
        'includeSpellcheck': str,  # Include spell check suggestions in the response
        'domain': list  # Filter entities based on domains they are available on (array)
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
            return jsonify({'error': 'Error fetching artists'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@spotify.route('/get-events', methods=['GET'])
def get_events():
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    api_key = TICKET_MASTER_API_KEY

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

@spotify.route('/get-event-details/<event_id>', methods=['GET'])
def get_events(event_id):
    url = f"https://app.ticketmaster.com/discovery/v2/events/{event_id}.json"
    api_key = TICKET_MASTER_API_KEY

    # Add the API key to the parameters
    params = {'apikey': api_key}

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Error fetching event details'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@spotify.route('/recently-played')
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
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read user-read-recently-played"
    )



