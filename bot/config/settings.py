import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from environs import Env

# Env Conf
env = Env()
env.read_env('.env')

# Get Web Path
web_dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'web'))
sys.path.append(web_dir_path)

# Telegram Conf
TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
storage = MemoryStorage()

dp = Dispatcher(storage=storage)

from bot.core.handlers import Handlers
from bot.core.registers import register_handlers

handlers: Handlers = Handlers()

# Register Handlers
register_handlers(
    dp=dp,
    handlers=handlers
)

"""
    WEBHOOK
"""
WEBHOOK_URL: str = '/tg-webhook'
WEBHOOK_HOST: str = env("HTTPS_URL")
WEBHOOK_URL_PATH: str = f"{WEBHOOK_HOST}{WEBHOOK_URL}"


async def on_startup(
        app
) -> None:
    """
    When Start Bot
    """
    await bot.set_webhook(
        WEBHOOK_URL_PATH,
        allowed_updates=[
            "message", "my_chat_member", "chat_member", "channel_post"
        ]
    )


async def on_shutdown(
        app
) -> None:
    """
    When Stop Bot
    """
    await bot.delete_webhook()
