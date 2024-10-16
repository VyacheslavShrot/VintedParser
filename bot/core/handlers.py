from aiogram.types import Message

from bot.config.logger import logger


class Handlers:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Handlers, cls).__new__(cls)
            return cls._instance
        if cls._instance:
            raise Exception("Only one instance of Handlers can be created.")

    async def handle_text_input(
            self,
            message: Message
    ) -> None:
        """
        Any Text Message
        :param message: Default Aiogram Telegram Message
        :type message: Message
        """
        logger.info("\n----Text Input Handler is Starting")
        try:
            ...
        except Exception as e:
            logger.error(
                f"An unexpected error in Text Input Handler | {e}"
            )
