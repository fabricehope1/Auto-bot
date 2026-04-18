from telebot.types import ReplyKeyboardMarkup

def dashboard_menu():

    markup=ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row("🚀 Start Demo","💼 Start Real")
    markup.row("💳 Deposit","⚡ Recharge")
    markup.row("👤 Profile","👥 Referrals")
    markup.row("💬 Manager")

    return markup
