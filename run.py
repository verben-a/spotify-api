import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/")
def index():
	data = json.dumps({
		'message': 'successful'
		})
	return Response(data, 200, mimetype="application/json")

@app.route("/api/search", methods = ["GET"])
def artists_get():
	# scope = 'user-library-read'
	# token = util.prompt_for_user_token('alinaverbenchuk', scope)
	# spotify = spotipy.Spotify(auth=token)

	client_credentials_manager = SpotifyClientCredentials()
	spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	name = request.args.get('name')
	results = spotify.search(q='artist:' + name, type = 'artist')
	print(results)
	data = json.dumps({
		'name': name
	})
	return Response(data, 200, mimetype="application/json")


if __name__ =='__main__':
	app.run(debug=True)
