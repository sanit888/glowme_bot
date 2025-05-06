import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

API_TOKEN = "8085072986:AAGkWbFj_JKl9mrZwG99ixbF6M4R3Zsayw8"

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# FSM состояния
class DaySteps(StatesGroup):
    waiting_for_step = State()
    current_day = State()

# Шаги для каждого дня
DAYS = {
    "день 1": ["Шаг 1.1", "Шаг 1.2", "Шаг 1.3"],
    "день 2": ["Шаг 2.1", "Шаг 2.2", "Шаг 2.3"],
    "день 3": ["Шаг 3.1", "Шаг 3.2", "Шаг 3.3"],
    "день 4": ["Шаг 4.1", "Шаг 4.2", "Шаг 4.3"],
    "день 5": ["Шаг 5.1", "Шаг 5.2", "Шаг 5.3"],
    "день 6": ["Шаг 6.1", "Шаг 6.2", "Шаг 6.3"],
    "день 7": ["Шаг 7.1", "Шаг 7.2", "Шаг 7.3"]
}

user_progress = {}

@dp.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Привет! Выбери день: " + ", ".join(DAYS.keys()))
    await state.clear()

@dp.message(F.text.in_(DAYS.keys()))
async def choose_day(message: Message, state: FSMContext):
    user_id = message.from_user.id
    day = message.text
    user_progress[user_id] = {"day": day, "step": 0}
    await state.set_state(DaySteps.waiting_for_step)
    await send_next_step(message.chat.id, user_id)

@dp.message(DaySteps.waiting_for_step)
async def proceed_step(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in user_progress:
        await message.answer("Пожалуйста, сначала выбери день.")
        return
    user_progress[user_id]["step"] += 1
    await send_next_step(message.chat.id, user_id)

async def send_next_step(chat_id, user_id):
    day = user_progress[user_id]["day"]
    step_index = user_progress[user_id]["step"]
    steps = DAYS[day]
    if step_index < len(steps):
        await bot.send_message(chat_id, f"{steps[step_index]}\nНапиши что-то, чтобы перейти дальше.")
    else:
        await bot.send_message(chat_id, f"{day} завершён! Напиши /start, чтобы начать заново.")
        user_progress.pop(user_id, None)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

