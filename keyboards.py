from typing import List, TYPE_CHECKING

from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks import FindMusicCallback

if TYPE_CHECKING:
    from youtube_api import YoutubeVideo


def get_search_result_keyboard(search_result: List['YoutubeVideo']) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.max_width = 1
    for video in search_result:
        data = FindMusicCallback(video_id=video.video_id)
        builder.button(text=video.video_title, callback_data=data.pack())
    return builder
