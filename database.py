import sqlite3

conn=sqlite3.connect("users.db",check_same_thread=False)
cursor=conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
telegram_id INTEGER,
email TEXT UNIQUE
)
""")

conn.commit()


def add_user(tg_id,email):
    try:
        cursor.execute(
        "INSERT INTO users (telegram_id,email) VALUES (?,?)",
        (tg_id,email))
        conn.commit()
        return True
    except:
        return False


def get_user(tg_id):
    cursor.execute(
    "SELECT * FROM users WHERE telegram_id=?",
    (tg_id,))
    return cursor.fetchone()
