import json
import flask
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, request, Response
from decorators import crossdomain
import httplib2

from apiclient import discovery
from oauth2client import client

app = Flask(__name__)
client_credentials_manager = SpotifyClientCredentials()
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# @app.route("/")
# @crossdomain(origin='*')
# def index():
# 	data = json.dumps({
# 		'message': 'successful'
# 		})
# 	return Response(data, 200, mimetype="application/json")

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
	data = json.dumps(tracks)
	return Response(data, 200, mimetype="application/json")


@app.route('/')
@crossdomain(origin='*')
def index():
  if 'credentials' not in flask.session:
    return flask.redirect(flask.url_for('oauth2callback'))
  credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
  if credentials.access_token_expired:
    return flask.redirect(flask.url_for('oauth2callback'))
  else:
    http_auth = credentials.authorize(httplib2.Http())
    youtube = discovery.build('youtube', 'v3', http_auth)
    channel = youtube.channels().list(mine=True, part='snippet').execute()
    return json.dumps(channel)

@app.route('/oauth2callback')
def oauth2callback():
  flow = client.flow_from_clientsecrets(
      'client_secrets.json',
      scope='https://www.googleapis.com/auth/youtube.force-ssl',
      redirect_uri=flask.url_for('oauth2callback', _external=True),
      include_granted_scopes=True)
  if 'code' not in flask.request.args:
    auth_uri = flow.step1_get_authorize_url()
    return flask.redirect(auth_uri)
  else:
    auth_code = flask.request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    flask.session['credentials'] = credentials.to_json()
    return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
  import uuid
  app.secret_key = str(uuid.uuid4())
  app.debug = False
  app.run()
