from flask import Flask, render_template, url_for, session, redirect
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth 
from spotipy.cache_handler import FlaskSessionCacheHandler
from config import client_id, client_secret, redirect_uri, scope


app = Flask(__name__)
app.config['SECRET_KEY'] = "hello"

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id, 
    client_secret=client_secret, 
    redirect_uri=redirect_uri, 
    cache_handler=cache_handler,
    scope=scope,
    show_dialog = True
)

sp = Spotify(auth_manager=sp_oauth)


@app.route('/')
def home():
    return render_template('index.html')





if __name__ == '__main__':
    app.run(debug=True)
