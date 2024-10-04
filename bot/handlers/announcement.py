import asyncio

from aiogram import F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram import Router

from bot.handlers.functions import get_admin_ids, get_all_bot_users
from aiogram.utils.i18n import gettext as _

announcement = Router()


class AnnouncementStates(StatesGroup):
    announcement_text = State()


@announcement.message(F.text.lower().in_({"announcement", "add"}))
async def admin_handler(message: Message, state: FSMContext):
    check_user = await get_admin_ids(message.from_user.id)
    if check_user:
        await state.set_state(AnnouncementStates.announcement_text)
        await message.answer(_("Please send the announcement text 🔽"))
    else:
        await message.answer(_("You do not have the right to post an announcement 🛑"))


@announcement.message(AnnouncementStates.announcement_text)
async def announcement_text_handler(message: Message, state: FSMContext, bot: Bot):
    announcement_text = message.text
    await message.answer("Received announcement ✅")
    await message.answer(f"{announcement_text}")
    await state.clear()

    users_id = await get_all_bot_users()
    tasks = []
    count = 0

    for user in users_id:
        try:
            tasks.append(await bot.send_message(chat_id=user, text=announcement_text))
            count += 1
            if count % 28 == 0:
                await asyncio.gather(*tasks)
                tasks = []
                await asyncio.sleep(1)
        except Exception as e:
            print(f"Failed to send message to user {user}: {e}")

    await message.answer(f"Announcement sent to {count} users ✅")
    await message.answer(_("Announcement sent to all users ✅"))