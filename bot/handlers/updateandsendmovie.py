from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from db.models import Movie

movie_router = Router()
@movie_router.message(F.video, F.chat.type == "supergroup")
async def update_video(message: Message):
    message_id = message.message_id
    file_id = message.video.file_id
    film = await Movie.get(id_=file_id)
    try:
        if not film:
            await Movie.create(file_id=file_id, message_id=message_id)
            await message.answer(_("Movie saved."))
        else:
            await message.answer(_("Movie is already saved."))
    except Exception as error:
        await message.answer(_("Something went wrong"))
        await message.answer(str(error))