import re
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from aiogram.dispatcher.filters import Text
from connector import dp, bot
from data.config import admin_id, end, begin,day
from random import randint
from exec import PostChecker, PostDeleter, PreSender, Seneder
from data.dict import FIRST_START,  STOPP
import asyncio
import time
give = True
take = True

keyboard = types.InlineKeyboardMarkup()
keyboard.add(types.InlineKeyboardButton(text="Удалить", callback_data="delete"))
keybord_start = types.InlineKeyboardMarkup()
keybord_start.add(types.InlineKeyboardButton(text="Запустить отправку", callback_data="send"))
keyboard_end = types.InlineKeyboardMarkup()
keyboard_end.add(types.InlineKeyboardButton(text="Остановить отправку", callback_data="stop"))

del_btn = InlineKeyboardButton(text="Удалить", callback_data="delete")
stp_btn = InlineKeyboardButton(text="Остановить отправку", callback_data="stop")
inline_kb_full = InlineKeyboardMarkup(row_width=2).add(del_btn,stp_btn)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global give
    print(give)
    await message.reply(FIRST_START)

@dp.message_handler(Text(contains='',ignore_case=True))
async def time_send(message: types.Message):
    global usermsg,userdel
    user_msg = message.text
    split = user_msg.split()
    usermsg = int(split[0])
    userdel = int(split[1])
    await message.reply(
    f"Отлично. \n\
Твои посты буду выходить раз в {usermsg} с погрешностью {userdel}.")
    await message.answer("Нажмите чтобы запустить отправку", reply_markup=keybord_start)

async def delay_count():
    global delay
    delaer = 60 * (usermsg + randint(0, userdel))
    delay = delaer

async def night_delay_count():
    global delay
    delaer = usermsg + randint(0, userdel)
    one = day - minute_total_now + begin + delaer
    delay = 60*one

async def IsTimeTrue():
    global minute_total_now, IsTimeInPlace
    time_local = time.localtime(time.time())
    hour = time_local[3] * 60
    minute = time_local[4]
    minute_total_now = hour + minute
    IsTimeInPlace =  begin <= minute_total_now <= end

async def time_check():
    global give, diff
    await IsTimeTrue()
    if IsTimeInPlace == True:
        await delay_count()
        min_send = delay/60
        difference = end - minute_total_now
        diff = difference > min_send
        if diff == False:
            await night_delay_count()
    else:
        await night_delay_count()

async def post_time():
    global post
    newdelay = time.time() + delay
    time_local = time.localtime(newdelay)
    post = time.strftime('%H:%M:%S', time_local)

async def SendCheck():
    global posts,main_result
    await time_check()
    posts = PostChecker.check_post()
    main_result = PostChecker.main_result
    if main_result == 0:
        await bot.send_message(admin_id, f"{posts}. Отпрвлять нечего")
        while main_result == 0:
            await asyncio.sleep(5)
            main_result = PostChecker.main_result

async def PresendAndSend():
    await post_time()
    await PreSender.presend_smthg()
    await bot.send_message(admin_id, f'Следующий пост в {post}\n{posts}\nВыберите действие', reply_markup=inline_kb_full)
    await asyncio.sleep(delay) 
    await Seneder.send_smthg()  

@dp.callback_query_handler(text = 'send')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    message: types.Message
    global give
    give = True
    await bot.send_message(admin_id, 'Запускаю отправку')
    while give == True:
        await SendCheck()
        if main_result != 0:
            await PresendAndSend()
    else:
        while give == False:
            await asyncio.sleep(5)

@dp.callback_query_handler(text = 'delete')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await PostDeleter.delete_smthg()
    await bot.send_message(callback_query.from_user.id,'Неугодный пост удален')
    await SendCheck()
    if main_result != 0:
        await post_time()
        await PreSender.presend_smthg()
        await bot.send_message(admin_id, f'Следующий пост в {post}\n{posts}\nВыберите действие', reply_markup=inline_kb_full)

@dp.callback_query_handler(text = 'stop')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    global give
    give = False
    await bot.send_message(callback_query.from_user.id, STOPP)
    await bot.send_message(admin_id, "Нажмите чтобы запустить отправку", reply_markup=keybord_start)