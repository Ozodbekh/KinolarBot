import asyncio
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from bot.handlers.functions import get_all_bot_users, get_admin_ids


add_router = Router()


class AdvertiseState(StatesGroup):
    media = State()
    description = State()


@add_router.message(F.text.lower() == 'advertise')
async def advertise_handler(message: Message, state: FSMContext):
    check_user = await get_admin_ids(message.from_user.id)
    if check_user:
        await state.set_state(AdvertiseState.media)
        await message.answer(_("Please send promotional media 🔽"))
    else:
        await message.answer(_("You do not have the right to post an ad 🛑"))


@add_router.message(AdvertiseState.media)
async def advertise_media(message: Message, state: FSMContext):
    if message.photo:
        file_id = message.photo[-1].file_id
        await state.update_data(media_type='photo', file_id=file_id)
        await state.set_state(AdvertiseState.description)
        await message.answer(_("Image accepted. Send the text now 🔽"))
    elif message.video:
        file_id = message.video.file_id
        await state.update_data(media_type='video', file_id=file_id)
        await state.set_state(AdvertiseState.description)
        await message.answer(_("Video accepted. Send the text now 🔽"))

@add_router.message(AdvertiseState.description)
async def advertise_description(message: Message, state: FSMContext, bot: Bot):
    description = message.text
    data = await state.get_data()
    await state.clear()
    file_id = data.get('file_id')
    media_type = data.get('media_type')

    user_ids = await get_all_bot_users()
    tasks = []
    count = 0

    if media_type == 'photo':
        for user in user_ids:
            tasks.append(bot.send_photo(chat_id=user, photo=file_id, caption=description))
            count += 1
            if count % 28 == 0:
                await asyncio.gather(*tasks)
                tasks = []
        if tasks:
            await asyncio.gather(*tasks)

    elif media_type == 'video':
        for user in user_ids:
            tasks.append(bot.send_video(chat_id=user, video=file_id, caption=description))
            count += 1
            if count % 28 == 0:
                await asyncio.gather(*tasks)
                tasks = []
        if tasks:
            await asyncio.gather(*tasks)

    await message.answer(_("Advertisement sent to all users ✅"))