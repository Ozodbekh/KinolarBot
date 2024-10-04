# from aiogram import html, Router, types
# from aiogram.client import bot
# from aiogram.filters import CommandStart
# from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
# from aiogram.utils.i18n import gettext as _
#
# from bot.dispatcher import dp
# from db.models import User
#
# from sqlalchemy import select
#
# main_router = Router()
#
#
# @main_router.message(CommandStart())
# async def command_start_handler(message: Message) -> None:
#     user = await User.get(id_=message.from_user.id)
#
#     if not user:
#         await User.create(id=message.from_user.id, fullname=message.from_user.full_name)
#
#     await message.answer(_("Hello, {}!").format(html.bold(message.from_user.full_name)))
#
#
# # @main_router.message()
# # async def send_movie(message: types.Message):
# #     code = message.text.strip().upper()
# #
# #     if code in MOVIE_CODES:
# #         try:
# #             await bot.forward_message(chat_id=message.chat.id, from_chat_id=Channel_id, message_id=7)
# #         except Exception as e:
# #             await message.reply(_("Could not found movie"))
# #             print(_(f"Error: {e}"))
# #     else:
# #         await message.reply(_("Invalid code. Please try again."))
#
# @main_router.message()
# async def send_movie(message: types.Message):
#     code = message.text.strip().upper()
#     movie = await Movie.get_film(id_=code)
#     if movie.code == code:
#         await bot.forward_message(chat_id=chat_id,
#                                   from_chat_id=channel_id,
#                                   message_id=movie.code,
#                                   protect_content=True)
#     else:
#         await message.reply(_("Invalid code. Please try again."))
#
# import datetime
#
# from sqlalchemy import String, BigInteger, DateTime, Column, func
# from sqlalchemy.ext.asyncio import AsyncAttrs
# from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, declared_attr
#
# from db.utils import AbstractClass
#
#
# class Base(AsyncAttrs, DeclarativeBase):
#     @declared_attr
#     def tablename(self):
#         return self.name.lower() + "s"
#
#
# class CreatedModel(Base, AbstractClass):
#     abstract = True
#     created_at = Column(DateTime(), default=datetime.datetime.utcnow, server_default=func.now())
#     updated_at = Column(DateTime(), onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow,
#                         server_default=func.now())
#
#
# class User(CreatedModel):
#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     fullname: Mapped[str] = mapped_column(String(255))
#     phone_number: Mapped[str] = mapped_column(String(255), nullable=True)
#     is_active: Mapped[bool] = mapped_column(default=True)
#
#
# class Movie(CreatedModel):
#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     code: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
#     file_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
import bcrypt

print(bcrypt.hashpw('123'.encode(), salt=bcrypt.gensalt()))

bot = "@Kinoo25Bot"
@main_router.message(F.text,~F.video)
async def show_films(message: Message):
    cod = message.text
    if cod.isdigit():
        query = select(Kino.file_id).where(Kino.message_id == cod)
        film_url = session.execute(query).scalars().first()
        if film_url:
            await message.answer_video(film_url,
                                       width=1920, height=1080 , caption=f"Kino kodi {cod} \n 🤖 Bizning bot: {bot}")
        else:
            await message.answer(f"No film")
    else:
        pass


@main_router.message(F.video , F.chat.type == 'supergroup')
async def vidoe_handler(message: Message) :
    message_id = message.message_id
    file_id = message.video.file_id
    try:
         if message_id and file_id :
               q1 = insert(Kino).values(message_id=message_id, file_id=file_id)
               session.execute(q1)
               session.commit()
         else:
             await message.answer("Saqlanmadi")
    except Exception as e:
        await message.answer("Bu kino Mavjud")


from bot.buttons.inline import Inlien_net_link
from db.models import User, Kino, session

main_router = Router()

CHANNELS = ["@lwqmdnep", "@ibiwqdbpo"]  # Replace with your channel usernames


async def check_sub_channel(bot: Bot, user_id: int):
    for channel in CHANNELS:
        chat_member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        if chat_member.status not in ["member", "administrator", "creator"]:
            return False
    return True

new = "❌ Siz hali ham kanallarga a'zo bo'lmagansiz. Iltimos, avval kanallarga a'zo bo'ling."
@main_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    is_subscribed = await check_sub_channel(bot=message.bot, user_id=message.from_user.id)
    if not is_subscribed:
        await message.answer(
            text="❌ Kechirasiz botimizdan foydalanishdan oldin ushbu kanallarga a'zo bo'lishingiz kerak.",
            reply_markup=Inlien_net_link()
        )
    else:
        await message.answer(text="✍🏻 Kino kodini yuboring.")
