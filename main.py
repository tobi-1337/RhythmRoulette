from flask import Flask, render_template, url_for, session, redirect, request
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth 
from spotipy.cache_handler import FlaskSessionCacheHandler
from config import client_id, client_secret, redirect_uri


app = Flask(__name__) #This variable is used to run the program
app.config['SECRET_KEY'] = "hello" #Secret key is needed when you use sessions in Flask
scope = 'user-top-read' #The scope defines which information from the Spotify account we get access to
cache_handler = FlaskSessionCacheHandler(session) #cache_handler allows us to store the Spotify Token in Flask session

'''
sp_oauth is used to authorize the Spotify user. They get prompted to accept or decline
the terms of service defined in our scope. 
'''
sp_oauth = SpotifyOAuth (
    client_id=client_id, 
    client_secret=client_secret, 
    redirect_uri=redirect_uri, 
    cache_handler=cache_handler,
    scope=scope,
    show_dialog = True
)
sp = Spotify(auth_manager=sp_oauth) #This variable lets us connect to the authorized Spotify user


'''Home page for the website'''
@app.route('/')
def home():
    return render_template('index.html')


'''
If the user is not already authorized, they will be redirected to the 
Spotify authorization URL. If they are already authorized they will be redirected
to 'top-artists'.
'''
@app.route('/login')
def login():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('get_top_artists'))


'''
The callback page is where the user gets redirected to 
from the Spotify authorization page.
'''
@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_top_artists'))


'''
If the user is authorized they will see their top artists written out on the page.
If not, they will be redirected to the Spotify authorization page.
'''
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
    

'''The logout page is used to clear the Flask session.'''
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


'''Makes sure that the program is run from this file and not from anywhere else.'''
if __name__ == '__main__':
    app.run(debug=True)
