import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, request, Response

app = Flask(__name__)
client_credentials_manager = SpotifyClientCredentials()
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


@app.route("/")
def index():
	data = json.dumps({
		'message': 'successful'
		})
	return Response(data, 200, mimetype="application/json")

@app.route("/api/search", methods = ["GET"])
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
def album_tracks_get():
	album_id = request.args.get('album_id')
	tracks = spotify.album_tracks(album_id)
	data = json.dumps(tracks)
	return Response(data, 200, mimetype="application/json")


if __name__ =='__main__':
	app.run(debug=True)
