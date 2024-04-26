from flask import Flask, render_template, url_for, session, redirect, request, flash, jsonify
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth 
from spotipy.cache_handler import FlaskSessionCacheHandler
from config import client_id, client_secret, redirect_uri
import db

# This variable is used to run the program
app = Flask(__name__) 
# Secret key is needed when you use sessions in Flask
app.config['SECRET_KEY'] = "hello" 
# The scope defines which information from the Spotify account we get access to
scope = 'user-top-read playlist-modify-public playlist-modify-private'
# cache_handler allows us to store the Spotify Token in Flask session
cache_handler = FlaskSessionCacheHandler(session) 
# This variable is used for connection to the database.
db = db 
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
# This variable lets us connect to the authorized Spotify user
sp = Spotify(auth_manager=sp_oauth) 


def user_info(user):
    ''' 
    Gets basic profile information about a Spotify User

    Parameters:
        - user: the id of the usr
    '''
    return sp._get('users/' + user)


def get_user_info(info):
    ''' 
    Retrieve user information from Spotify based on the requested info.

    Parameters:
        - info (str): The type of information to retrieve. 

    Returns:
        - Various types: Depending on the 'info' parameter, returns different types of user information.
    '''
    if sp_oauth.validate_token(cache_handler.get_cached_token()):
        current_user = sp.me()
        if info == 'me':
            return current_user
        elif info == 'username':
            return current_user['id']
        elif info == 'img':
            return current_user['images'][0]['url'] if current_user['images'] else None
        elif info == 'display_name':
            return current_user['display_name']


def register_user():
    '''
    The function checks if the user is already registered in our database. 
    If it is not, registers them.
    '''
    if sp_oauth.validate_token(cache_handler.get_cached_token()):
        user_id = get_user_info('username')
        display_name = get_user_info('display_name')
        registered_user = db.check_user_in_db(user_id)
        if not registered_user:
            db.register_user(user_id)
        session['logged_in'] = True
        flash(f"Välkommen {display_name}, \n Du är inloggad!")
        return redirect(url_for('home'))
    else:
        flash(f"Du måste godkänna Spotifys villkor för att logga in!")
        return redirect(url_for('home'))
        
    
@app.route('/')
def home():
    ''' Home page for the website. '''
    return render_template('index.html')


@app.route('/login')
def login():
    '''
    If the user is not already authorized, they will be redirected to the 
    Spotify authorization URL. If they are already authorized they will be redirected
    to 'top-artists'.
    '''
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    flash(f"Du är redan inloggad!")
    return redirect(url_for('get_top_artists'))


@app.route('/callback')
def callback():
    ''' The callback page is where the user gets redirected to from the Spotify authorization page. '''
    try:
        sp_oauth.get_access_token(request.args['code'])
        return register_user()
    except:
        flash(f"Du måste godkänna villkoren!")
        return redirect(url_for('home'))


@app.route('/profile-page')
def profile_page():
    ''' Redirects the user to their profile page. '''
    username = get_user_info('username')
    return redirect(url_for('user_profile', username=username))


@app.route('/users', methods=['GET', 'POST'])
def users():
    '''
    Handle requests to the '/users' route. 
    GET method: renders the 'search_for_users.html' template
    POST method: 
        - Retrieves the username from the form data.
        - Searches the database for users matching the provided username.
        - Renders the 'users.html' template with search results if found, 
        or with an indication of no results if not found.
    '''
    if request.method == 'POST':
        username = request.form['search_user']
        search_name = db.search_users(username)
        if len(search_name) > 0:
            return render_template('users.html', username=username, search_name=search_name)
        else: 
            return render_template('users.html', username=username, search_name=False)
    else:
        return render_template('search_for_users.html')


@app.route('/profile-page/<username>')
def user_profile(username):
    '''
    Render the profile page for a specific user.
    Retrieves information about the specified user and renders their profile page.

    Parameters:
        - username (str): The username of the user whose profile page is to be rendered.
    
    Returns:
        - The profile page template with the user's information.
    '''
    search_name = db.check_user_in_db(username)
    if not search_name:
        return render_template('index.html')
    user = user_info(username)
    print(user['id'])
    username = user['id']
    current_user = get_user_info('username')
    display_name = user['display_name']
    user_image_url = user['images'][0]['url'] if user['images'] else None
    return render_template('profile_page.html', username=username, display_name=display_name, user_image_url=user_image_url,current_user=current_user)
    

@app.route('/profile-settings')
def profile_settings():
    ''' Retrieves the current user's display name, username, and profile image URL. '''
    if sp_oauth.validate_token(cache_handler.get_cached_token()):
        display_name = get_user_info('display_name')
        username = get_user_info('username')
        user_image_url = get_user_info('img')
        return render_template('profile_settings.html', display_name=display_name, username=username, user_image_url=user_image_url)


@app.route('/delete-profile', methods=['POST'])
def delete_profile():
    '''
    Deletes the user's profile if they are authenticated.

    If the user's token is validated, their profile is deleted from the database
    and their session is cleared. Then, the user is redirected to the home page.
    '''
    if sp_oauth.validate_token(cache_handler.get_cached_token()):
        user_id = get_user_info('username')
        registered_user = db.check_user_in_db(user_id)

        if registered_user:
            db.delete_user(user_id)
            session.clear()
            return redirect(url_for('home'))

        
@app.route('/top-artists')
def get_top_artists():
    '''
    If the user is authorized they will see their top artists written out on the page.
    If not, they will be redirected to the Spotify authorization page.
    '''
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    top_artists = sp.current_user_top_artists()
    username = get_user_info('username')
    display_name = get_user_info('display_name')
    artists = top_artists['items']
    nr = 0
    user_image_url = get_user_info('img')
    return render_template('top-artists.html', artists=artists, nr=nr, user_image_url=user_image_url, username=username, display_name=display_name)
    

@app.route('/generate-playlist', methods=['GET', 'POST'])
def generate_playlist():
    '''
    If the user reaches this page with the use of GET method the
    function will create and empty Spotify playlist using the name and
    description provided by the user through the HTML form. If POST method was
    used, which it will be granted the form was filled, it will return the url for 
    recommendations.
    '''
    if sp_oauth.validate_token(cache_handler.get_cached_token()):
        if request.method == 'POST':
            user_id = get_user_info('username')
            playlist_name = request.form['playlist_name']
            playlist_description = request.form['playlist_description']
            if len(playlist_name) > 0:
                playlist = sp.user_playlist_create(user_id, playlist_name, public=True, collaborative=False, description=playlist_description)
            else:
                flash(f'Du måste ange ett namn på spellistan!')
                return render_template('generate_playlist.html')
            playlist_id = playlist['id']
            playlist_uri = playlist['uri']
            playlist_named = playlist['name']
            db.add_playlist(playlist_id, playlist_uri, user_id)
            session['playlist_uri'] = playlist_uri  
            session['playlist_id'] = playlist_id
            session['playlist_named'] = playlist_named  
            return redirect(url_for('recommendations'))
        else:
            return render_template('generate_playlist.html')


@app.route('/playlist', methods=['GET', 'POST'])
def get_playlist():
    '''
    Retrieves the user's information and playlist details,
    and renders the playlist page template with this information.
    '''
    username = get_user_info('username')
    display_name = get_user_info('display_name')
    user_image_url = get_user_info('img')
    user_playlists = db.check_playlist(username)
    playlists = {"name":[], 'id':[]}
    for playlist in user_playlists:
        for pl in playlist:
            playlist_info = sp.playlist(pl)
            playlist_name = playlist_info['name']
            playlist_uri = playlist_info['uri']
            playlists['name'].append(playlist_name)
            playlists['id'].append(pl)
    for name in playlists['id']:
        print(name)
    zipped_playlists = zip(playlists['name'], playlists['id'])
    if sp_oauth.validate_token(cache_handler.get_cached_token()):
        if len(user_playlists) > 0:
            return render_template('playlist.html', playlist = True, playlists=zipped_playlists, username=username, display_name=display_name, user_image_url=user_image_url)
        else:
            return render_template('playlist.html', username=username, display_name=display_name, user_image_url=user_image_url)

@app.route('/playlist/<pl_id>')
def playlist_page(pl_id):
    username = get_user_info('username')
    display_name = get_user_info('display_name')
    user_image_url = get_user_info('img')
    playlist_tracks = sp.playlist_tracks(pl_id)
    print(pl_id)
    playlist_info = sp.playlist(pl_id)
    playlist_uri = playlist_info['uri']
    playlist_name = playlist_info['name']
    playlist_items = playlist_tracks['items']
    for track in playlist_tracks['items']:
        track_name = track['track']['name']
        artist_name = track['track']['artists'][0]['name']
        album_name = track['track']['album']['name']
        album_img = track['track']['album']['images'][0]['url']
        
        

        print(f" Img: {album_img} Track: {track_name} Artist: {artist_name} Album: {album_name}")
    try:
        return render_template('playlist_page.html', playlist_uri=playlist_uri, album_img=album_img, playlist_name=playlist_name, playlist_items=playlist_items, pl_id=pl_id, username=username, display_name=display_name, user_image_url=user_image_url)
    except:
        flash(f"Spellistan du försöker öppna är tom!")
        return render_template('index.html')
@app.route('/delete-playlist/<pl_id>')
def delete_playlist(pl_id):
    sp.current_user_unfollow_playlist(pl_id)
    db.delete_playlist(pl_id)
    return redirect(url_for('get_playlist'))



@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    '''
    If the user reaches this page using the GET method they will be
    presented with a list of genres to choose from, as well as a slider. When clicking
    the button at the bottom of the form they will generate as many songs they wanted
    generated from the genres they chose. If the POST method was used, they will be presented with
    a pop up notifying them that their playlist was made, then redirected to the home page.
    For the POST method the function is using JavaScript for storing the genres chosen and handling the redirection.
    '''
    if sp_oauth.validate_token(cache_handler.get_cached_token()):
            recco_list = sp.recommendation_genre_seeds()
            if request.method == 'POST':
                if request.is_json:
                    data = request.json
                    genre_seeds = data.get('genres')
                    recco_limit = data.get('recco_limit')
                else:
                    genre_seeds = request.form['genres']
                    recco_limit = request.form['recco_limit']

                reccos = sp.recommendations(seed_genres=genre_seeds, 
                                            limit=recco_limit, market='SE')

                if 'playlist_id' in session:
                    playlist_id = session['playlist_id']
                    track_list = []
                    
                    for track in reccos['tracks']:
                        song_uri = track['uri']
                        track_list.append(song_uri)
                    sp.playlist_add_items(playlist_id, track_list, position=None)
                return jsonify({"message": "Spellista skapad!"}), 200
            else:
                return render_template('recommendations.html', recco_list=recco_list)


@app.route('/generate-playlist-year', methods=['GET', 'POST'])
def generate_playlist_year():
    '''
    If the user reaches this page with the use of GET method the
    function will create and empty Spotify playlist using the name and
    description provided by the user through the HTML form. If POST method was
    used, which it will be granted the form was filled, it will return the url for 
    recommendations.
    '''
    if sp_oauth.validate_token(cache_handler.get_cached_token()):
        if request.method == 'POST':
            current_user = sp.me()
            user_id = current_user['id']
            playlist_name = request.form['playlist_name']
            playlist_description = request.form['playlist_description']
            playlist = sp.user_playlist_create(user_id, playlist_name, public=True, collaborative=False, description=playlist_description)
            playlist_id = playlist['id']
            session['playlist_id'] = playlist_id
            return redirect(url_for('search'))
        else:
            return render_template('generate-playlist-year.html') 
            
        
@app.route('/search', methods=['GET', 'POST'])
def search():
    '''
    If the user reaches this page using the GET method they will be
    presented with a list of decade to choose from, as well as a slider. When clicking
    the button at the bottom of the form they will generate as many songs they wanted
    generated from the decades they chose. If the POST method was used, they will be presented with
    a pop up notifying them that their playlist was made, then redirected to the home page.
    For the POST method the function is using JavaScript for storing the decades chosen and handling the redirection.
    '''
    print("Search route accessed")
    if sp_oauth.validate_token(cache_handler.get_cached_token()):
        decades = ['50s', '60s', '70s', '80s', '90s', '00s']   

        if request.method == 'POST':
            print("Received a POST request")
            if request.is_json:
                data = request.json
                years = data.get('decades')
                search_limit = data.get('search_limit')
                print(f"Years: {years}")
                print(f" Search limit: {search_limit}")
            else:
                years = request.form.get('decades')
                search_limit = request.form.get('search_limit')
                    
                        
            if 'playlist_id' in session:
                playlist_id = session['playlist_id']
                print(f"Playlist id: {playlist_id}")
                track_list = []  

                search_terms = [f"{decade}" for decade in years]
                combined_search = ' '.join(search_terms)
                print("Search query:", combined_search)
                searches = sp.search(q= combined_search, type='track', market='SE')
                for decade in years:
                    searches = sp.search(q=f'year:{combined_search}', type='track', limit=search_limit, market='SE')
                print("Search results:", searches)
                

                for track in searches['tracks']['items']:
                    print(f"Print datatype i felsökningssyfte: ", type(track))
                    track_list.append(track['uri'])

                sp.playlist_add_items(playlist_id, track_list, position=None)

            return jsonify({"message": "Spellista skapad!"}), 200
        
        else:
            return render_template('search.html', decades=decades)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    ''' Renders the signup page. '''
    return render_template('signup.html')


@app.route('/logout')
def logout():
    ''' The logout page is used to clear the Flask session. '''
    if 'is_logged_in' in session:
        flash(f"Du är utloggad!")
    else:
        flash(f"Du är inte inloggad!")
    session.clear()   
    return redirect(url_for('home'))


''' Makes sure that the program is run from this file and not from anywhere else. '''
if __name__ == '__main__':
    app.run(debug=True)