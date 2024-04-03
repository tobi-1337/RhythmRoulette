import psycopg2
from config import db_password, host, database, user, port

host = host
database = database
user = user
password = db_password
port = port

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