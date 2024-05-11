import psycopg2
from config import password, host, database, user, port


host = host
database = database
user = user
password = password
port = port


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
        - pl_id: The id of the Spotify playlist created through the application.
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
    
    cur.execute(
                '''
                INSERT INTO user_bio(user_id, user_bio)
                VALUES  (%s, %s) 
                ON DUPLICATE KEY UPDATE user_bio = VALUES (user_bio)
                ''', (user_id, bio_text)
    ) 
    conn.commit()

def get_user_bio(user_id):
    cur.execute(
                '''
                SELECT * FROM user_bio
                WHERE * user_id = %s
                ''', (user_id, )
    )
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