import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Новый способ задания parse_mode
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message()
async def start_handler(message: Message):
    if message.text == "/start":
        await message.answer("Привет! Это GlowMe Бот ✨ Твой путь Ясности начинается здесь.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
