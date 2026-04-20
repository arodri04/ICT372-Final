import sqlite3

conn = sqlite3.connect('./instance/db.sqlite')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS todo (
        task_id INTEGER PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        done BOOLEAN NOT NULL DEFAULT 0,
        userId INTEGER NOT NULL,
        created VARCHAR(10),
        dueDate VARCHAR(10),
        FOREIGN KEY(userId) REFERENCES users(userId) ON DELETE CASCADE
    )
''')

conn.commit()
conn.close()