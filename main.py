from flask import Flask, render_template, url_for, session, redirect, request, flash, jsonify
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth 
from spotipy.cache_handler import FlaskSessionCacheHandler
from config import client_id, client_secret, redirect_uri
import db


app = Flask(__name__) #This variable is used to run the program
app.config['SECRET_KEY'] = "hello" #Secret key is needed when you use sessions in Flask
scope = 'user-top-read playlist-modify-public playlist-modify-private' #The scope defines which information from the Spotify account we get access to
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



@app.route('/')
def home():
    '''Home page for the website'''
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
    '''
    The callback page is where the user gets redirected to 
    from the Spotify authorization page.
    '''
    sp_oauth.get_access_token(request.args['code'])
    session['logged_in'] = True
    flash(f"Du är inloggad!")
    return redirect(url_for('get_top_artists'))



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
    artists = top_artists['items']
    nr = 0
    return render_template('top-artists.html', artists=artists, nr=nr)
    

@app.route('/generate-playlist', methods=["GET", "POST"])
def generate_playlist():
    if sp_oauth.validate_token(cache_handler.get_cached_token()):
        if request.method == "POST":
            current_user = sp.me()
            user_id = current_user['id']
            playlist_name = request.form['playlist_name']
            playlist_description = request.form['playlist_description']
            playlist = sp.user_playlist_create(user_id, playlist_name, public=True, collaborative=False, description=playlist_description)
            playlist_id = playlist['id']
            session['playlist_id'] = playlist_id
            return redirect(url_for('recommendations'))
        else:
            return render_template('generate_playlist.html')

@app.route('/recommendations', methods=["GET", "POST"])
def recommendations():
    if sp_oauth.validate_token(cache_handler.get_cached_token()):
            recco_list = sp.recommendation_genre_seeds()
            if request.method == "POST":
                if request.is_json:
                    data = request.json
                    genre_seeds = data.get('genres')
                    recco_limit = data.get('recco_limit')
                else:
                    genre_seeds = request.form['genres']
                    recco_limit = request.form['recco_limit']

                reccos = sp.recommendations(seed_genres=genre_seeds, limit=recco_limit, market="SE")

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

@app.route('/generate-playlist-year', methods=["GET", "POST"])
def generate_playlist_year():
    if sp_oauth.validate_token(cache_handler.get_cached_token()):
        if request.method == "POST":
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
        
@app.route('/search', methods=["GET", "POST"])
def search():

    if sp_oauth.validate_token(cache_handler.get_cached_token()):
        decades = ['50s', '60s', '70s', '80s', '90s', '00s']   

        if request.method == "POST":
            if request.is_json:
                data = request.json
                years = data.get('decades')
                search_limit = data.get('search_limit')
                print(years)
                print(search_limit)
            else:
                years = request.form.get('decades')
                search_limit = request.form.get('search_limit')
                
            #search = sp.search(year=years, limit=recco_limit, market="SE")
            
            
            if 'playlist_id' in session:
                playlist_id = session['playlist_id']
                track_list = []  

                search_terms = [f"{decade}" for decade in years]
                combined_search = ' '.join(search_terms)
                searches = sp.search(q= combined_search, type='track', market="SE")
                '''for decade in years:
                    search_term = f"{decade}s"  
                    searches = sp.search(q=f'year:{search_term}', type='track', limit=recco_limit, market="SE")'''


                for track in searches['tracks']:
                    print(track['uri'])
                    

                sp.playlist_add_items(playlist_id, track_list, position=None)

            return jsonify({"message": "Spellista skapad!"}), 200
        
        else:
            return render_template('search.html', decades=decades)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    return render_template("signup.html")



@app.route('/logout')
def logout():
    '''The logout page is used to clear the Flask session.'''
    if 'is_logged_in' in session:
        flash(f"Du är utloggad!")
    else:
        flash(f"Du är inte inloggad!")
    session.clear()   
    return redirect(url_for('home'))




'''Makes sure that the program is run from this file and not from anywhere else.'''
if __name__ == '__main__':
    app.run(debug=True)



