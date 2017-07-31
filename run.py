import json
import flask
import spotipy
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, request, Response
from decorators import crossdomain
import httplib2

from apiclient import discovery
from oauth2client import client

app = Flask(__name__)
client_credentials_manager = SpotifyClientCredentials()
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


@app.route("/")
@crossdomain(origin='*')
def index():
	data = json.dumps({
		'message': 'successful'
		})
	return Response(data, 200, mimetype="application/json")

@app.route("/api/search", methods = ["GET"])
@crossdomain(origin='*')
def artists_get():
	
	name = request.args.get('name')
	results = spotify.search(q='artist:' + name, type = 'artist')
	# extract the URI
	one_artist = results['artists']['items'][0]['uri']
	
	albums = spotify.artist_albums(one_artist)
	print(albums);
	data = json.dumps(albums)
	return Response(data, 200, mimetype="application/json")


@app.route("/api/album_tracks", methods = ["GET"])
@crossdomain(origin='*')
def album_tracks_get():
	album_id = request.args.get('album_id')
	tracks = spotify.album_tracks(album_id)

	new_response = {'items': []}

	for track in tracks['items']:
	    name_of_song = track['name']
	    name_of_artist = track['artists'][0]['name']
	    spotify_preview_url = track['preview_url']
	    spotify_external_urls = track['external_urls']['spotify']
	    uri = track['uri']


	    track_query = name_of_song + ' ' + name_of_artist
	    r = requests.get("https://www.googleapis.com/youtube/v3/search?key=AIzaSyDtVCBq96FsRaLCDibG_hNVMvJg_hwEMf4&part=snippet&type=video&q=" + track_query)
	    youtube_response = r.json()

	    video_id = youtube_response['items'][0]['id']['videoId']


	    new_response['items'].append({
	    	'name_of_song': name_of_song,
	    	'name_of_artist': name_of_artist, 
	    	'spotify_preview_url': spotify_preview_url,
	    	'spotify_external_urls': spotify_external_urls,
	    	'uri': uri,
	    	'video_id': video_id
	    	})
	# Fetch Youtube track
	# looping through the tracks!
	# get the artist name
	# get the song name
	# seach by combinatin of artist name + song name
	data = json.dumps(new_response)
	return Response(data, 200, mimetype="application/json")




if __name__ == '__main__':
  import uuid
  app.secret_key = str(uuid.uuid4())
  app.debug = False
  app.run()
