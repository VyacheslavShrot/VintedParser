from aiogram import Dispatcher, types

from bot.core.handlers import Handlers


def register_handlers(
        dp: Dispatcher,
        handlers: Handlers
) -> None:
    """
    Register Handlers with Instance of Classes
    """
    dp.message.register(handlers.handle_text_input, lambda message: message.content_type == types.ContentType.TEXT)
