from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from data.config import token
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()


bot = Bot(token=token,parse_mode="html")
dp = Dispatcher(bot, storage=storage)