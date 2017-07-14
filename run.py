import json
import spotipy
import spotipy.util as util
from flask import Flask, request, Response

app = Flask(__name__)

scope = 'user-library-read'
token = util.prompt_for_user_token('alinaverbenchuk', scope)
spotify = spotipy.Spotify(auth=token)


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
	print(results)
	data = json.dumps({
		'name': name
	})
	return Response(data, 200, mimetype="application/json")


if __name__ =='__main__':
	app.run(debug=True)
