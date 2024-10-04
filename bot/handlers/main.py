from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _

from bot.buttons.inline import JoinInlineButton
from db.models import User, ChannelGroupList


main_router = Router()


@main_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user = await User.get(id_=message.from_user.id)
    is_subscribed = await check_sub_channel(bot=message.bot, user_id=message.from_user.id)
    if not user:
        await User.create(id=message.from_user.id, fullname=message.from_user.full_name, username=message.from_user.username)

    if not is_subscribed:
        await message.answer(
            _("❌ Sorry you need to subscribe to these channels before using our bot."),
            reply_markup=(await JoinInlineButton())
        )
    else:
        await message.answer(_(f"Assalomu alaykum {message.from_user.full_name} welcome to our bot.\n\nPlease send the movie code."))


@main_router.callback_query(F.data == "check")
async def confirm_subscription(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    is_subscribed = await check_sub_channel(bot=bot, user_id=user_id)

    if is_subscribed:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.delete()
        await callback.message.answer(_("Assalomu alaykum ... welcome to our bot.\n\nPlease send the movie code."))
    else:
        await callback.answer(_("You are still not subscribed to all channels."), show_alert=True)


async def check_sub_channel(bot: Bot, user_id: int):
    channels = await ChannelGroupList.get_all()
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel.username_, user_id=user_id)
        if chat_member.status not in ["member", "administrator", "creator"]:
            return False
    return True

