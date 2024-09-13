import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, I18n, SimpleI18nMiddleware
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("TELEGRAM_TOKEN")

dp = Dispatcher()
i18n = I18n(path="locales", default_locale="en", domain="messages")
dp.message.middleware(SimpleI18nMiddleware(i18n))


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        _("Hello, {name}!").format(
            name=html.quote(message.from_user.full_name)
        )
    )


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
