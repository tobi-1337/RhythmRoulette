import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

host = os.environ.get("host")
database = os.environ.get("database")
user = os.environ.get("user")
password = os.environ.get("password")
port = os.environ.get("port")


def check_user_in_db(user_id):
    '''
    Checks if the user is already in the database. If it is, returns True, otherwise False.

    Parameters: 
        - user_id (str): The spotify ID provided from spotipy through authorization.
    '''
    cur.execute(
                '''
                SELECT s_id FROM a_user
                WHERE s_id = %s
                ''', (user_id,)        
        )
    existing_user = cur.fetchall()
    if len(existing_user) == 0:
        return False
    else:
        return existing_user


def search_users(search_value):
    '''
    Compares the search_value recieved from main.py with the s_id columns in the a_user table
    to search for users.
    Parameters: 
        - search_value (str): what the user searches for in the application. 
    '''
    cur.execute(
                '''
                SELECT s_id FROM a_user
                WHERE s_id LIKE %s
                ''', ('%' + search_value + '%',) 
    )
    return cur.fetchall()


def become_friends(user_1, user_2):
    cur.execute(
        '''
        INSERT INTO friends_with
        VALUES (%s, %s)
        ''', (user_1, user_2)
    )
    conn.commit()

def check_if_friends(user_1, user_2):
    cur.execute(
        '''
        SELECT * FROM friends_with
        WHERE user_one = %s AND user_two = %s OR user_one = %s AND user_two = %s
        ''', (user_1, user_2, user_2, user_1)
    )
    friends_with = cur.fetchall()
    if len(friends_with) > 0:
        return True
    else: 
        return False


def remove_friend(user_1, user_2):
    cur.execute(
        '''
        DELETE FROM friends_with 
        WHERE user_one = %s AND user_two = %s OR user_one = %s AND user_two = %s
        ''', (user_1, user_2, user_2, user_1)
    )
    conn.commit()


def register_user(user_id):
    '''
    Registers a user to the database.

    Parameters:
        - user_id (str): the Spotify-id from the current user.
    '''
    cur.execute(
                '''
                INSERT INTO a_user
                VALUES (%s)
                ''', (user_id,)      
    )
    conn.commit()


def delete_user(user_id):
    '''
    Compares user_id to to s_id in the a_user table, then deletes matching users.
    
    Parameters: 
        - user_id (str): The Spotify-id from the current user.
    '''
    cur.execute(
                '''
                DELETE FROM a_user
                WHERE s_id = %s
                ''', (user_id,)
    )
    conn.commit()


def add_playlist(pl_id,pl_url,user_id):
    '''
    Saves the playlist to the database
    Parameters:
        - pl_id: The ID of the Spotify playlist created through the application.
        - pl_url: The uri of the playlist created through the application.
        - user_id: The Spotify ID of the user created the playlist.
    '''

    cur.execute(
                '''
                INSERT INTO playlist(pl_id, pl_url, user_id)
                VALUES (%s, %s, %s)
                ''',(pl_id, pl_url, user_id)
    )
    conn.commit()

def generated_playlist_info(playlist_id, playlist_name, nr_songs, created_date):
    '''
    Inserting information about a playlist generated
        Parameters: 
        - pl_id (str): The playlist-id from the current playlist.
    Returns:
        - pl_name (str): The name of the playlist.
        - nr_songs (int): The number of songs in the playlist.
        - date_created (date): The date when the playlist was created.
	'''

    cur.execute(
				'''
				INSERT INTO about_generated_playlist(pl_id, playlist_name, playlist_length, last_updated_datetime)
				VALUES (%s, %s, %s, %s)
				''', (playlist_id, playlist_name, nr_songs, created_date)
    )

    conn.commit()

def check_if_playlist_is_own(pl_id):
    
    cur.execute(
                '''
                SELECT user_id FROM playlist 
                WHERE pl_id = %s
                ''',(pl_id,)
    )

    return cur.fetchone()[0]

def check_playlist(user_id):
    '''
    Checks which user is connected to the saved playlist.

    Parameters: 
        - user_id: The ID of the current user
    '''

    cur.execute(
                '''
                SELECT pl_id FROM playlist 
                WHERE user_id = %s
                ''',(user_id,)
    )

    return cur.fetchall()


def delete_playlist(pl_id):
    '''
    Compares pl_id(str) with pl_id in the playlist table. Deletes matches.

    Parameters:
        - pl_id(str): The provided playlist ID.
    '''
    cur.execute(
                ''' 
                DELETE FROM playlist
                WHERE pl_id = %s 
                ''', (pl_id,)
    )
    conn.commit()


def save_user_bio(user_id, bio_text):
    ''' Adds a user biopraph of maximum 500 words into the database or update if one already exist'''
    user_id = str(user_id)
    bio_text = str(bio_text)
    cur.execute(
                '''
                INSERT INTO a_user(s_id, user_bio)
                VALUES  (%s, %s) 
                ON CONFLICT (s_id) DO UPDATE SET user_bio = EXCLUDED.user_bio
                ''', (user_id, bio_text)
    ) 
    conn.commit()

def get_user_bio(user_id):
    cur.execute(
                '''
                SELECT user_bio FROM a_user
                WHERE s_id = %s
                ''', (user_id, )
    )
    return cur.fetchone()[0]


def get_user_r_date(user_id):
    cur.execute(
            '''
            SELECT TO_CHAR(r_date, 'YYYY-MM-DD HH24:MI') as formatted_date
            FROM a_user
            WHERE s_id = %s;
            ''', (user_id, )
    )
    registered = cur.fetchone()[0]
    if len(registered) == 0:
        return False
    return registered

def comment_user(user_1, user_2, comment_text):
    cur.execute(
            '''
            INSERT INTO comment_user (user_one, user_two, u_comment)
            VALUES(%s, %s, %s)
            ''', (user_1, user_2, comment_text )
    )
    conn.commit()

def get_user_comments(user_id):
            cur.execute(
                '''
                SELECT user_one, user_two, u_comment, TO_CHAR(c_date, 'YYYY-MM-DD HH24:MI') as formatted_date
                FROM comment_user
                WHERE user_two = %s
                ''', (user_id,)
    )
            return cur.fetchall()


def remove_comment(user_1, user_2, comment_text):
    cur.execute(
            '''
            DELETE FROM comment_user
            WHERE user_one = %s AND user_two = %s AND u_comment = %s
            ''', (user_1, user_2, comment_text )
    )
    conn.commit()








try: 
    conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password,
    port=port  
    )

    cur = conn.cursor()
    
except psycopg2.Error as error: 
    print(f"Error: unable to connect to the database\n {error}")