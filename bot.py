hereimport telebot
from telebot.types import ReplyKeyboardMarkup
from config import TOKEN
from database import add_user,get_user

bot=telebot.TeleBot(TOKEN)

waiting_email={}

def main_menu():
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("Register","Login")
    return kb

def dashboard():
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("Start Trade Demo")
    kb.row("Start Trade Real")
    return kb


@bot.message_handler(commands=['start'])
def start(msg):

    user=get_user(msg.from_user.id)

    if user:
        bot.send_message(msg.chat.id,
        "Welcome back Trader 📊",
        reply_markup=dashboard())
    else:
        bot.send_message(msg.chat.id,
        "Welcome Trader",
        reply_markup=main_menu())


@bot.message_handler(func=lambda m:m.text=="Register")
def register(msg):
    waiting_email[msg.from_user.id]=True
    bot.send_message(msg.chat.id,
    "Enter your email:")


@bot.message_handler(func=lambda m:m.text=="Login")
def login(msg):

    user=get_user(msg.from_user.id)

    if user:
        bot.send_message(msg.chat.id,
        "Logged in ✅",
        reply_markup=dashboard())
    else:
        bot.send_message(msg.chat.id,
        "Account not found")


@bot.message_handler(func=lambda m:True)
def email_handler(msg):

    if msg.from_user.id in waiting_email:

        email=msg.text.lower()

        ok=add_user(msg.from_user.id,email)

        if ok:
            bot.send_message(
            msg.chat.id,
            "Account Created ✅",
            reply_markup=dashboard())
        else:
            bot.send_message(
            msg.chat.id,
            "Email already used ❌")

        waiting_email.pop(msg.from_user.id)


bot.infinity_polling()
