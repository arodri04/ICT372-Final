import sqlite3

conn = sqlite3.connect('./instance/db.sqlite')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        userId INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        salt TEXT
    )
''')

conn.commit()
conn.close()