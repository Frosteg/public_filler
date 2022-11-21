import re
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from aiogram.dispatcher.filters import Text
from connector import dp, bot
from data.config import admin_id, end, begin
from random import randint
from exec import give_bot, presender, post_checker, deleter
import asyncio
import time
give = True

keyboard1 = types.InlineKeyboardMarkup()
keyboard1.add(types.InlineKeyboardButton(text="Запустить отправку", callback_data="send"))

keyboard = types.InlineKeyboardMarkup()
keyboard.add(types.InlineKeyboardButton(text="Удалить", callback_data="delete"))

time_start = begin//60
start_time = f"{time_start}:00:00"

time_end = end//60
end_time = f"{time_end}:00:00"


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global give
    print(give)
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_markup.add('Запустить отправку','Остановить отправку')
    #await message.reply(ANSWER_START)
    await message.reply(f"Привет Этот бот будет отправлять посты\nс {start_time} до {end_time}\nПринимать контент этот бот может круглосуточно.\nКак часто будут выходить посты?\nОтправь мне 2 цирфы через пробел.\nПервая время между поставми, вторая погрешность для небольшой рандомизации")
    
@dp.message_handler(Text(contains='',ignore_case=True))
async def time_send(message: types.Message):
    global usermsg
    global userdel
    user_msg = message.text
    split = user_msg.split()
    usermsg = int(split[0])
    userdel = int(split[1])
    await message.reply(f"Отлично. Твои посты буду выходить раз в {usermsg} с погрешностью {userdel}.\nЧтобы начать работать отправь боту текст 'Запустить отправку' либо нажми кнопку на клавиатуре бота")
    await message.answer("Нажмите чтобы запустить отправку", reply_markup=keyboard1)

async def delay_count():
    global delay
    global post
    delay = 60 * (usermsg + randint(0, userdel))
    nowTime = time.time()
    newdelay = nowTime + delay
    time_local = time.localtime(newdelay)
    time.strftime('%H:%M:%S', time_local)
    post = time.strftime('%H:%M:%S', time_local)
    
async def IsTimeTrue():
    global minute_total_now
    #global IsTimeAfterStart
    global IsTimeInPlace
    nowTime = time.time()
    time_local = time.localtime(nowTime)
    hour = time_local[3] * 60
    minute = time_local[4]
    minute_total_now = hour + minute
    IsTimeInPlace =  begin <= minute_total_now <= end
    

async def time_check():
    global give
    min_send = delay/60
    difference = end - minute_total_now
    diff = min_send > difference
    if diff:
        give = False

async def TimeSendCheck():
    await IsTimeTrue()
    if IsTimeInPlace:
        await delay_count()
        await time_check()

async def PostSendAttempt():
    global main_result
    global posts
    posts = post_checker.check_post()
    main_result = post_checker.main_result
    if main_result == 0:
        await bot.send_message(admin_id, f"{posts}. Отпрвлять нечего")
        while main_result == 0:
            await asyncio.sleep(5)
            main_result = post_checker.main_result    

async def PresendAndSend():
    await presender.presend_smthg()
    await bot.send_message(admin_id, f'Следующий пост в {post}\n{posts}')
    await bot.send_message(admin_id,"Нажмите чтобы удалить пост", reply_markup=keyboard)
    await asyncio.sleep(delay) 
    await give_bot.send_smthg()  

@dp.callback_query_handler(text="send")
async def process_callback_button1(callback_query: types.CallbackQuery):
    message: types.Message
    global give
    global posts
    give = True
    print(give)
    await bot.send_message(admin_id, 'Запускаю отправку')
    while give == True:
        await TimeSendCheck()
        if IsTimeInPlace and give == True:
            await PostSendAttempt()                       
            if main_result != 0:
                await PresendAndSend() 
        else:
            await asyncio.sleep(5)
    else:
        await bot.send_message(admin_id, f'Отправка приостановлена')

@dp.callback_query_handler(text="delete")
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await deleter.delete_smthg()
    await bot.send_message(callback_query.from_user.id,'Неугодный пост удален')
    posts = post_checker.check_post()
    main_result = post_checker.main_result
    await PostSendAttempt()
    if main_result != 0:
        await presender.presend_smthg()
        await bot.send_message(admin_id, f'Следующий пост в {post}\n{posts}')
        await bot.send_message(admin_id, "Нажмите чтобы удалить пост", reply_markup=keyboard)

@dp.message_handler(Text(equals='Остановить отправку',ignore_case=True))
async def process_parser_command(message: types.Message):
    global give
    give = False
    print(give)
    await bot.send_message(message.chat.id,f'Остановка работы отправки')
