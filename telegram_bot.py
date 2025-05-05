from telegram import Bot
from constants import BOT_TOKEN, CHAT_ID
from utility import update_status

bot = Bot(token=BOT_TOKEN)

async def send_message_to_tg(message):
    try:
        await bot.initialize()
        await bot.send_message(chat_id=CHAT_ID, text=message)
        await bot.shutdown()
    except Exception:
        update_status(f"Faild to send TG message: ```{message}```", "error")
