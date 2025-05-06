import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

WEBHOOK_HOST = "https://dashboard.render.com/web/srv-d0cbhuqdbo4c73dh7kng"  # замените на адрес вашего Render сервиса
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", default=8000))

@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer("Привет! Бот работает через webhook.")

async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()

async def main():
    app = web.Application()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    return app

if __name__ == '__main__':
    web.run_app(main(), host=WEBAPP_HOST, port=WEBAPP_PORT)
