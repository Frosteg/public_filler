from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from data.config import token

bot = Bot(token=token,parse_mode="html")
dp = Dispatcher(bot)