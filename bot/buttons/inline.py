
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import ChannelGroupList
from aiogram.utils.i18n import gettext as _

async def JoinInlineButton():
    ikb = InlineKeyboardBuilder()

    channels = await ChannelGroupList.get_all()

    for channel in channels:
        url = channel.url
        number = channel.id
        button = InlineKeyboardButton(text=_("{} - channel".format(number)), url=url)
        ikb.add(button)

    ikb.adjust(1, repeat=True)

    ikb.add(
        InlineKeyboardButton(text=_("✅ Confirmation"), callback_data="check")
    )
    ikb.adjust(1)
    return ikb.as_markup()
