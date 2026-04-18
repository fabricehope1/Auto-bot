import sqlite3

conn=sqlite3.connect("users.db",check_same_thread=False)
cursor=conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
telegram_id INTEGER PRIMARY KEY,
email TEXT,
demo_balance REAL DEFAULT 50000,
real_balance REAL DEFAULT 0,
energy INTEGER DEFAULT 100
)
""")

conn.commit()
