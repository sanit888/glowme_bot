from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta, time as dt_time
import asyncio
import logging
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
scheduler = AsyncIOScheduler()

# Состояния шагов внутри дня
class StepState(StatesGroup):
    waiting_for_step = State()

# Данные маршрутов на 7 дней
days = {
    f"day_{i}": [
        f"День {i}: Шаг 1 — практика осознанности",
        f"День {i}: Шаг 2 — телесная практика",
        f"День {i}: Шаг 3 — вечерняя рефлексия"
    ] for i in range(1, 8)
}

user_progress = {}

# Кнопка выбора дня
@dp.message(commands=["start"])
async def cmd_start(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    for i in range(1, 8):
        builder.button(text=f"День {i}", callback_data=f"day_{i}_step_0")
    await message.answer("Выбери день:", reply_markup=builder.as_markup())

# Обработка нажатия на шаг дня
@dp.callback_query()
async def handle_step(callback: CallbackQuery, state: FSMContext):
    data = callback.data
    day_key, _, step_num = data.split('_')
    step_num = int(step_num)
    user_id = callback.from_user.id

    # Проверка, завершил ли предыдущий шаг
    if step_num > 0 and user_progress.get(user_id, {}).get(day_key, -1) < step_num - 1:
        await callback.answer("Сначала заверши предыдущий шаг.", show_alert=True)
        return

    steps = days[day_key]
    if step_num < len(steps):
        await callback.message.answer(steps[step_num])
        await state.set_state(StepState.waiting_for_step)
        await state.update_data(day_key=day_key, step_num=step_num)
        user_progress.setdefault(user_id, {})[day_key] = step_num

        # Планируем напоминание через 6 часов, если это не ночь
        now = datetime.now()
        next_time = now + timedelta(hours=6)
        if not (22 <= next_time.hour or next_time.hour < 8):
            scheduler.add_job(
                send_reminder,
                trigger=DateTrigger(run_date=next_time),
                args=[user_id, day_key, step_num]
            )

        # Кнопка следующего шага, если не последний
        if step_num + 1 < len(steps):
            builder = InlineKeyboardBuilder()
            builder.button(
                text=f"Перейти к шагу {step_num + 2}",
                callback_data=f"{day_key}_step_{step_num + 1}"
            )
            await callback.message.answer("Когда будешь готов(а), переходи к следующему шагу:", reply_markup=builder.as_markup())
    else:
        await callback.message.answer("Все шаги на сегодня пройдены ✨")

# Напоминание
async def send_reminder(user_id: int, day_key: str, step_num: int):
    try:
        await bot.send_message(user_id, f"Напоминание: ты не завершил(а) шаг {step_num + 1} дня {day_key[-1]}")
    except Exception as e:
        logging.warning(f"Не удалось отправить напоминание: {e}")

async def main():
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
