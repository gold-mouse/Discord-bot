from telegram import Bot
from constants import BOT_TOKEN, CHAT_ID

bot = Bot(token=BOT_TOKEN)

async def send_message_to_tg(message):
    await bot.initialize()
    await bot.send_message(chat_id=CHAT_ID, text=message)
    await bot.shutdown()
