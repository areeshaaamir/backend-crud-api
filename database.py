import sqlite3
from datetime import datetime

now = datetime.now().isoformat()

conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS tasks(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT,
                   done BOOLEAN,
                   created_at TEXT,
                   updated_at TEXT
               )""")

cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]

if count == 0:
    cursor.executemany("""
                       INSERT INTO tasks (title, done, created_at, updated_at)
                       VALUES (?, ?, ?, ?)
                       """,
                       [
                           ("Complete the FlyRank AI Assignment", False, now, now),
                           ("Farm 1000 Primogems in Genshin", False, now, now),
                           ("Make dinner", False, now, now)
                       ])
    conn.commit()