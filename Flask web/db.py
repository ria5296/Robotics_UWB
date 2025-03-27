import sqlite3

db = sqlite3.connect('users.db')
cursor = db.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

db.commit()
db.close()
print("db 생성")
