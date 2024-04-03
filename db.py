import psycopg2


host = "pgserver.mau.se"
database = "let_online_store"
user = "ao7002"
password = "ovah95n4"
port = "5432" 

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