from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from db.models import Movie, HistoryUser

movie_router = Router()
@movie_router.message(F.video, F.chat.type == "supergroup")
async def update_video(message: Message):
    message_id = message.message_id
    file_id = message.video.file_id
    film = await Movie.get_by_file_id(file_id=file_id)
    try:
        if not film:
            await Movie.create(file_id=file_id, message_id=message_id)
            await message.answer(_("Movie saved."))
        else:
            await message.answer(_("Movie is already saved."))
    except Exception as error:
        await message.answer(_("Something went wrong"))
        await message.answer(str(error))


@movie_router.message(F.text)
async def get_movie_by_code(message: Message):
    try:
        movie_id = int(message.text)
        movie = await Movie.get(id_=movie_id)

        if movie:
            await HistoryUser.create(sent_codes=movie_router, user_id=message.from_user.id)
            await message.answer_video(video=movie.file_id, caption=movie.descreption)
        else:
            await message.answer(_("Movie not found. Please check the movie code."))
    except ValueError:
        await message.answer(_("Please send a valid movie code."))
    except Exception as error:
        await message.answer(_("Something went wrong"))
        await message.answer(str(error))




