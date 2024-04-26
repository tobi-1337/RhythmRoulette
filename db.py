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

    Args: user_id: The spotify ID provided from spotipy through authorization.
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
    '''
    cur.execute(
                '''
                INSERT INTO a_user
                VALUES (%s)
                ''', (user_id,)      
    )
    conn.commit()

def delete_user(user_id):

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
    checks which user is connected to the saved playlist
    '''

    cur.execute(
    '''
    SELECT pl_id FROM playlist 
    WHERE user_id = %s
    ''',(user_id,)
    )

    return cur.fetchall()

def delete_playlist(user_id):
    cur.execute(
        ''' 
        DELETE FROM playlists 
        WHERE pl_id = %s 
        ''', (user_id,)
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