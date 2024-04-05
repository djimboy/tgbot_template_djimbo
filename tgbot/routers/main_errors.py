# - *- coding: utf- 8 - *-
from aiogram import Router
from aiogram.filters import ExceptionMessageFilter
from aiogram.handlers import ErrorHandler

from tgbot.utils.misc.bot_logging import bot_logger

router = Router(name=__name__)


# Ошибка с блокировкой бота пользователем
# @router.errors(ExceptionTypeFilter(TelegramForbiddenError))
# class MyHandler(ErrorHandler):
#     async def handle(self):
#         ...


# Ошибка с редактированием одинакового сообщения
@router.errors(ExceptionMessageFilter(
    "Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message")
)
class MyHandler(ErrorHandler):
    async def handle(self):
        bot_logger.exception(
            f"====================\n"
            f"Exception name: {self.exception_name}\n"
            f"Exception message: {self.exception_message}\n"
            f"===================="
        )
