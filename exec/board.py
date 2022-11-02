from re import A
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from aiogram.dispatcher.filters import Text
from connector import dp, bot
from data.config import admin_id
from data.dict import ANSWER_START
from random import randint
from exec import give_bot
from exec import presender
from exec import post_checker
import datetime
import asyncio
import time



def time_Main1(main_start1, main_end1, date_time):
        return main_start1 <= date_time <= main_end1


main_start1 = datetime.time(8,00,0)
main_end1 = datetime.time(23,59,50)

date_time = datetime.datetime.now().time()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global give
    global take  
    give = True
    take = True
    print(take)
    print(give)
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_markup.add('Запустить отправку','Остановить отправку')
    await message.reply(ANSWER_START)
    await bot.send_message(message.chat.id,f'Парсинг: {take}\nОтправка: {give}\nБот готов к запуску', reply_markup=keyboard_markup)


@dp.message_handler(Text(contains='Время'))
async def time_send(message: types.Message):
    
    global str_msg
    usermsg = message.text
    if usermsg == 'Время':
        return 
    str_msg = (str(usermsg))
    str_msg = str_msg.replace("Время ","")
    str_msg = int(str_msg)

@dp.message_handler(Text(contains='Задержка'))
async def time_send(message: types.Message):
    global str_del
    userdel = message.text
    if userdel == 'Задержка':
        return 
    str_del = (str(userdel))
    str_del = str_del.replace("Задержка ","")
    str_del = int(str_del)

async def delay_count():
    global delay
    global post
    delay = 60 * (str_msg + randint(0, str_del))
    nowTime = time.time()
    newdelay = nowTime + delay
    time_local = time.localtime(newdelay)
    time.strftime('%H:%M:%S', time_local)
    post = time.strftime('%H:%M:%S', time_local)
    

@dp.message_handler(Text(equals='Запустить отправку'))
async def process_parser_command(message: types.Message):
    global give
    give = True
    print(give)
    await bot.send_message(message.chat.id, f'Отправка: {give}\nОтправка запущена')
    while give == True:
        date_time = datetime.datetime.now().time()
        if time_Main1(main_start1, main_end1, date_time):
            await delay_count()
            await presender.presend_smthg()
            posts = post_checker.check_post()
            await bot.send_message(admin_id, f'Следующий пост в {post}\n{posts}')
            await asyncio.sleep(delay) 
            if time_Main1(main_start1, main_end1, date_time) and give == True:
                await give_bot.send_smthg()           
        else:
            await asyncio.sleep(5)
            #continue
    else:
        await bot.send_message(message.chat.id, f'Отправка: {give}\nРабота приостановлена')

@dp.message_handler(Text(equals='Остановить отправку'))
async def process_parser_command(message: types.Message):
    global give
    give = False
    print(give)
    await bot.send_message(message.chat.id,f'Отправка: {give}\nОстановка работы отправки')
    