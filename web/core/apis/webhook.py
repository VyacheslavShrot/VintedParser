from aiogram import types
from aiogram.types import Update
from fastapi import Request
from fastapi.responses import JSONResponse

from bot.config.settings import dp, bot
from web.config.logger import logger


class WebHookHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        SingleTone Pattern
        """
        if not cls._instance:
            return super(WebHookHandler, cls).__new__(cls)
        if cls._instance:
            raise Exception("Only one instance of WebHookHandler can be created.")

    @staticmethod
    async def webhook(
            request: Request
    ):
        """
        Simple WebHook for Telegram Bot
        """
        logger.info(f"\n----Start WebHook")
        try:
            # Get Data
            json_data: dict = await request.json()

            # Update Data
            update: Update = types.Update(**json_data)

            # Handle Update
            await dp.feed_update(
                bot=bot,
                update=update
            )
            return JSONResponse(
                {
                    "status": "success"
                },
                status_code=200
            )
        except Exception as e:
            logger.error(f"An unexpected error occurred while getting data from telegram webhook | {e}")
            return JSONResponse(
                {
                    "error": f"An unexpected error occurred while getting data from telegram webhook | {str(e)}"
                },
                status_code=500
            )
