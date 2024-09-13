from aiogram.filters.callback_data import CallbackData


class FindMusicCallback(CallbackData, prefix="find"):
    video_id: str
