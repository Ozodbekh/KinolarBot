from db.models import Advertising, User


async def get_admin_ids(user_id):
    ids = await Advertising.get_all()
    admin_ids = [id_.admin_id for id_ in ids]
    return user_id in admin_ids


async def get_all_bot_users():
    ids = await User.get_all()
    user_ids = [user.id for user in ids]
    return user_ids