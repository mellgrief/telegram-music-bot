import asyncio
import logging
import sys
from io import BytesIO
from os import getenv

from aiogram import Bot, Dispatcher, html, Router, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, I18n, SimpleI18nMiddleware
from dotenv import load_dotenv
from youtube_api import YouTubeApi

load_dotenv()
telegram_token = getenv("TELEGRAM_TOKEN")
google_token = getenv("GOOGLE_TOKEN")

youtube = YouTubeApi(google_token)

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


@dp.message()
async def message_handler(message: Message) -> None:
    response = youtube.search_music(message.text)[0]
    await message.answer(f"Audio title is {response.video_title}")
    audio = youtube.download_audio(response.video_id)
    audio_stream = BytesIO(audio)
    audio_stream.name = "file.mp3"
    input_file = types.BufferedInputFile(audio, filename="file.mp3")
    await message.bot.send_audio(chat_id=message.chat.id, audio=input_file, title=f"{response.video_title}")


async def main() -> None:
    bot = Bot(token=telegram_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
