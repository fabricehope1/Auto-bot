import telebot
import os
import sqlite3
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# ================= CONFIG =================

TOKEN=os.getenv("BOT_TOKEN")

bot=telebot.TeleBot(TOKEN)

# ================= DATABASE =================

conn=sqlite3.connect("users.db",check_same_thread=False)
cursor=conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
telegram_id INTEGER UNIQUE,
email TEXT
)
""")
conn.commit()

# ================= MENUS =================

def about_menu():
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Register","Login")
    return markup

def back_menu():
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("⬅ Back")
    return markup

def dashboard_menu():
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Demo Account","Real Account")
    markup.row("Deposit")
    markup.row("Start Trade Demo","Start Trade Real")
    markup.row("⬅ Back")
    return markup

# ================= START =================

@bot.message_handler(commands=['start'])
def start(message):

    text="""
🤖 AUTO TRADING BOT

Welcome Trader!

✅ Automatic OTC Trading
✅ Buy / Sell Bot
✅ Martingale System
✅ Works 24/7

Choose option below:
"""

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=about_menu()
    )

# ================= REGISTER =================

waiting_register={}

@bot.message_handler(func=lambda m: m.text=="Register")
def register(message):

    waiting_register[message.chat.id]=True

    bot.send_message(
        message.chat.id,
        "📧 Enter Email to Register:",
        reply_markup=back_menu()
    )

# ================= LOGIN =================

waiting_login={}

@bot.message_handler(func=lambda m: m.text=="Login")
def login(message):

    waiting_login[message.chat.id]=True

    bot.send_message(
        message.chat.id,
        "🔐 Enter Email to Login:",
        reply_markup=back_menu()
    )

# ================= BACK =================

@bot.message_handler(func=lambda m: m.text=="⬅ Back")
def back(message):
    start(message)

# ================= EMAIL HANDLER =================

@bot.message_handler(func=lambda message: True)
def handle_text(message):

    chat_id=message.chat.id
    email=message.text

    # ---------- REGISTER ----------

    if waiting_register.get(chat_id):

        try:
            cursor.execute(
                "INSERT INTO users(telegram_id,email) VALUES(?,?)",
                (chat_id,email)
            )
            conn.commit()

            bot.send_message(
                chat_id,
                "✅ Registration Successful!",
                reply_markup=dashboard_menu()
            )

        except:
            bot.send_message(
                chat_id,
                "❌ Account already exists."
            )

        waiting_register.pop(chat_id,None)
        return

    # ---------- LOGIN ----------

    if waiting_login.get(chat_id):

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user=cursor.fetchone()

        if user:
            bot.send_message(
                chat_id,
                "✅ Login Successful!",
                reply_markup=dashboard_menu()
            )
        else:
            bot.send_message(
                chat_id,
                "❌ Account not found."
            )

        waiting_login.pop(chat_id,None)
        return


# ================= DASHBOARD BUTTONS =================

@bot.message_handler(func=lambda m: m.text=="Demo Account")
def demo(message):
    bot.send_message(message.chat.id,"💰 Demo Balance: $10000")

@bot.message_handler(func=lambda m: m.text=="Real Account")
def real(message):
    bot.send_message(message.chat.id,"💵 Real Balance: $0")

@bot.message_handler(func=lambda m: m.text=="Deposit")
def deposit(message):
    bot.send_message(message.chat.id,"🔗 Deposit via Pocket Option")

@bot.message_handler(func=lambda m: m.text=="Start Trade Demo")
def trade_demo(message):
    bot.send_message(message.chat.id,"🚀 Demo Auto Trading Starting...")

@bot.message_handler(func=lambda m: m.text=="Start Trade Real")
def trade_real(message):
    bot.send_message(message.chat.id,"🔥 Real Auto Trading Starting...")

# ================= RUN =================

print("BOT RUNNING...")
bot.infinity_polling()
