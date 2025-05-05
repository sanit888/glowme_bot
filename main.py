import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

days = [
    "✨ День 1: Я имею право хотеть",
    "✨ День 2: Ясность начинается с честности",
    "✨ День 3: Чего я точно не хочу",
    "✨ День 4: Что мне важно на самом деле",
    "✨ День 5: Мой идеальный день",
    "✨ День 6: Первые шаги и поддержка",
    "✨ День 7: Моя Ясность"
]

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    for i, day in enumerate(days):
        keyboard.add(InlineKeyboardButton(text=f"{day}", callback_data=f"day_{i+1}"))
    await message.answer("Привет! Выбери день:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("day_"))
async def day_handler(callback_query: types.CallbackQuery):
    day_index = int(callback_query.data.split("_")[1]) - 1
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Ты выбрала: {days[day_index]}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
