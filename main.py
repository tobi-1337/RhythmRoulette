from flask import Flask, render_template, url_for, session, redirect, request
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth 
from spotipy.cache_handler import FlaskSessionCacheHandler
from config import client_id, client_secret, redirect_uri


app = Flask(__name__)
app.config['SECRET_KEY'] = "hello"
scope = 'user-top-read'
cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth (
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

@app.route('/login')
def login():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('get_top_artists'))

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_top_artists'))

@app.route('/top-artists')
def get_top_artists():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    top_artists = sp.current_user_top_artists()
    artists = top_artists['items']
    for artist in artists:
        print(artist['name'])

    return render_template('top-artists.html', artists=artists)
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
