from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from aiogram import Dispatcher

redis = Redis()

dp = Dispatcher(storage=RedisStorage(redis))