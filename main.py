import asyncio
import os
import logging
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# Хранение прогресса пользователей
user_progress = {}
last_step_time = {}

# 7-дневный маршрут
routes = {
    1: ["Добро пожаловать в GlowMe 🌟", "Шаг 1: Напиши, чего ты хочешь прямо сейчас."],
    2: ["Шаг 2: Дыхание живости", "Сделай 3 вдоха с ощущением тела. Где ты сейчас?"],
    3: ["Шаг 3: Твоё тело — не враг", "Положи руку на грудь. Побудь с этим ощущением 1 минуту."],
    4: ["Шаг 4: Я имею право хотеть", "Что ты хочешь почувствовать в ближайшие 24 часа?"],
    5: ["Шаг 5: Отпускание контроля", "Напиши: что сегодня можно отпустить?"],
    6: ["Шаг 6: Границы и свобода", "Назови одно «нет» и одно «да» себе сегодня."],
    7: ["Шаг 7: Ритуал завершения", "Что ты хочешь взять с собой с этого пути?"]
}

# Проверка времени — не отправлять ночью
def is_daytime():
    now = datetime.now().time()
    return now >= datetime.strptime("08:00", "%H:%M").time() and now <= datetime.strptime("22:00", "%H:%M").time()

# Напоминание через 6 часов
async def send_reminder(user_id, day):
    if user_progress.get(user_id, 0) == day:
        if is_daytime():
            await bot.send_message(user_id, f"✨ Напоминание: продолжим День {day}?")
        # Повторное напоминание через 6 часов
        schedule_reminder(user_id, day)

def schedule_reminder(user_id, day):
    reminder_time = datetime.now() + timedelta(hours=6)
    scheduler.add_job(send_reminder, trigger=DateTrigger(reminder_time), args=[user_id, day])

# Обработка /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_progress[user_id] = 1
    last_step_time[user_id] = datetime.now()
    day = 1
    for step in routes[day]:
        await message.answer(step)
    schedule_reminder(user_id, day)

# Обработка любого текста пользователя как ответ на текущий шаг
@dp.message()
async def handle_response(message: types.Message):
    user_id = message.from_user.id
    current_day = user_progress.get(user_id, 1)
    last_step_time[user_id] = datetime.now()
    
    # Завершение маршрута
    if current_day >= 7:
        await message.answer("Ты прошла весь 7-дневный маршрут 💛")
        return

    # Переход к следующему дню
    next_day = current_day + 1
    user_progress[user_id] = next_day
    for step in routes[next_day]:
        await message.answer(step)
    schedule_reminder(user_id, next_day)

# Запуск
async def main():
    logging.basicConfig(level=logging.INFO)
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
