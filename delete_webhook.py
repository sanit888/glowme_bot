from aiogram import Bot
import asyncio
import os

async def delete_webhook():
    bot = Bot(token=os.getenv("8085072986:AAGkWbFj_JKl9mrZwG99ixbF6M4R3Zsayw8"))
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Webhook удалён")

asyncio.run(delete_webhook())
