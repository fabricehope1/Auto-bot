import time
import random

def start_session(bot,chat_id,amount):

    steps=5
    current=amount

    for step in range(1,steps+1):

        result=random.choice(["WIN","LOSS"])

        bot.send_message(
            chat_id,
            f"Step {step}\nAmount: ${current}\nResult: {result}"
        )

        if result=="WIN":
            bot.send_message(chat_id,"✅ Session Profit Finished")
            return

        current=current*2
        time.sleep(5)

    bot.send_message(chat_id,"❌ Session Finished (Max Steps)")
