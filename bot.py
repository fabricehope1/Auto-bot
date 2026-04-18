import telebot
import os
from database import cursor,conn
from dashboard import dashboard_menu
from trading import start_session
from telebot.types import ReplyKeyboardMarkup
import threading

TOKEN=os.getenv("BOT_TOKEN")
bot=telebot.TeleBot(TOKEN)

waiting_register={}
waiting_login={}

# ================= ABOUT SCREEN =================

@bot.message_handler(commands=['start'])
def start(message):

    text="""
💎 Welcome to AUTOBOT | AI TRADE

AI Trading Bot for Pocket Option

✅ Fully Automatic
✅ OTC Trading
✅ Martingale System
✅ 24/7 Cloud Trading

Choose option:
"""

    menu=ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row("Registration","Login")

    bot.send_message(message.chat.id,text,reply_markup=menu)

# ================= REGISTER =================

@bot.message_handler(func=lambda m:m.text=="Registration")
def register(message):

    waiting_register[message.chat.id]=True

    back=ReplyKeyboardMarkup(resize_keyboard=True)
    back.row("Back")

    bot.send_message(message.chat.id,"📧 Send your Email:",reply_markup=back)

# ================= LOGIN =================

@bot.message_handler(func=lambda m:m.text=="Login")
def login(message):

    waiting_login[message.chat.id]=True

    back=ReplyKeyboardMarkup(resize_keyboard=True)
    back.row("Back")

    bot.send_message(message.chat.id,"🔐 Enter Email:",reply_markup=back)

# ================= BACK =================

@bot.message_handler(func=lambda m:m.text=="Back")
def back(message):
    start(message)

# ================= EMAIL INPUT =================

@bot.message_handler(func=lambda message:True)
def handler(message):

    chat_id=message.chat.id
    text=message.text

    # REGISTER
    if waiting_register.get(chat_id):

        cursor.execute(
            "INSERT OR REPLACE INTO users(telegram_id,email) VALUES(?,?)",
            (chat_id,text)
        )
        conn.commit()

        waiting_register.pop(chat_id,None)

        bot.send_message(
            chat_id,
            "✅ Account Created!",
            reply_markup=dashboard_menu()
        )
        return

    # LOGIN
    if waiting_login.get(chat_id):

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (text,)
        )

        user=cursor.fetchone()

        waiting_login.pop(chat_id,None)

        if user:
            bot.send_message(chat_id,"✅ Login Success",reply_markup=dashboard_menu())
        else:
            bot.send_message(chat_id,"❌ Account Not Found")
        return

# ================= DASHBOARD =================

@bot.message_handler(func=lambda m:m.text=="🚀 Start Demo")
def demo(message):

    bot.send_message(message.chat.id,"🚀 Demo Trading Started")

    threading.Thread(
        target=start_session,
        args=(bot,message.chat.id,1)
    ).start()

@bot.message_handler(func=lambda m:m.text=="💼 Start Real")
def real(message):

    bot.send_message(message.chat.id,"🔥 Real Trading Started")

    threading.Thread(
        target=start_session,
        args=(bot,message.chat.id,1)
    ).start()

@bot.message_handler(func=lambda m:m.text=="💳 Deposit")
def deposit(message):
    bot.send_message(message.chat.id,"🔗 Deposit Link")

@bot.message_handler(func=lambda m:m.text=="👤 Profile")
def profile(message):
    bot.send_message(message.chat.id,"👤 User Profile")

@bot.message_handler(func=lambda m:m.text=="👥 Referrals")
def ref(message):
    bot.send_message(message.chat.id,"👥 Referral System")

@bot.message_handler(func=lambda m:m.text=="💬 Manager")
def manager(message):
    bot.send_message(message.chat.id,"Manager Online ✅")

print("AUTOBOT RUNNING...")
bot.infinity_polling()
