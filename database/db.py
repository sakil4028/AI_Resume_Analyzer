import sqlite3


def create_database():

    conn = sqlite3.connect('database/users.db')

    cursor = conn.cursor()

    
    cursor.execute('''

        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )

    ''')

    
    cursor.execute('''

        CREATE TABLE IF NOT EXISTS history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_email TEXT,

            ats_score REAL,

            category TEXT,

            uploaded_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

    ''')

    conn.commit()

    conn.close()


create_database()