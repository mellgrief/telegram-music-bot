import asyncio
import logging
import sys
from io import BytesIO
from os import getenv

from aiogram import Bot, Dispatcher, html, Router, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.formatting import TextLink
from aiogram.utils.i18n import gettext as _, I18n, SimpleI18nMiddleware
from dotenv import load_dotenv

from callbacks import FindMusicCallback
from keyboards import get_search_result_keyboard
from youtube_api import YouTubeApi

load_dotenv()
telegram_token = getenv("TELEGRAM_TOKEN")
google_token = getenv("GOOGLE_TOKEN")
telegram_url = getenv("TELEGRAM_URL")

youtube = YouTubeApi(google_token)

dp = Dispatcher()
i18n = I18n(path="locales", default_locale="en", domain="messages")
dp.message.middleware(SimpleI18nMiddleware(i18n))
dp.callback_query.middleware(SimpleI18nMiddleware(i18n))


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        _("Here you can write song which you want to find")
    )


@dp.message()
async def message_handler(message: Message) -> None:
    search_result = youtube.search_music(message.text)
    await message.answer(_("Result of search"), reply_markup=get_search_result_keyboard(search_result).as_markup())


@dp.callback_query(FindMusicCallback.filter())
async def find_music_callback_handler(query: CallbackQuery, callback_data: FindMusicCallback):
    title, audio = youtube.download_audio(callback_data.video_id)
    input_file = types.BufferedInputFile(audio, filename="file.mp3")
    message = await query.bot.send_audio(
        chat_id=query.message.chat.id,
        audio=input_file,
        title=f"{title}",
        caption=TextLink(_("BEST MUSIC"), url=telegram_url).as_html()
    )
    await query.answer()


async def main() -> None:
    bot = Bot(token=telegram_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
