from aiogram import Bot
import asyncio
import os

async def delete_webhook():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Webhook удалён")

asyncio.run(delete_webhook())
