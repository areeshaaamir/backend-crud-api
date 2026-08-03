import sqlite3

conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS tasks(
                   id INTEGER PRIMARY KEY,
                   title TEXT,
                   done BOOLEAN
               )""")

cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]

if count == 0:
    cursor.executemany("""
                       INSERT INTO tasks (title, done)
                       VALUES (?, ?)
                       """,
                       [
                           ("Complete the FlyRank AI Assignment", False),
                           ("Farm 1000 Primogems in Genshin", False),
                           ("Make dinner", False)
                       ])
    conn.commit()