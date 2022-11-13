import re
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from aiogram.dispatcher.filters import Text
from connector import dp, bot
from data.config import admin_id, main_start1, main_end1, date_time, end
from random import randint
from exec import give_bot, presender, post_checker, deleter
#from exec.post_checker import main_result
import asyncio
import time
give = True
take = True

keyboard = types.InlineKeyboardMarkup()
keyboard.add(types.InlineKeyboardButton(text="Удалить", callback_data="delete"))

async def time_Main1():
    global delta_time
    delta_time = main_start1 <= date_time <= main_end1

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global give
    global take  
    print(take)
    print(give)
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_markup.add('Запустить отправку','Остановить отправку')
    #await message.reply(ANSWER_START)
    await message.reply(f"Привет Этот бот будет отправлять посты\nс {main_start1} до {main_end1}\nПринимать контент этот бот может круглосуточно.\nКак часто будут выходить посты?\nОтправь мне текст 'Время X', где X это количество минут")

@dp.message_handler(Text(contains='Время',ignore_case=True))
async def time_send(message: types.Message):
    global str_msg
    usermsg = message.text
    #usermsg = usermsg.capitalize
    if usermsg == 'Время':
        return 
    str_msg = (str(usermsg))
    str_msg = str_msg.replace("Время ","")
    str_msg = int(str_msg)
    await message.reply(f"Твои посты буду выходить раз в {str_msg} минут.\nТеперь нужно установить погрешность, чтобы твои посты не отправлялись в одно и тоже время.\nОтправь мне текст 'Задержка X', где X это количество минут.")

@dp.message_handler(Text(contains='Задержка',ignore_case=True))
async def time_send(message: types.Message):
    global str_del
    userdel = message.text
    #userdel = userdel.capitalize
    if userdel == 'Задержка':
        return 
    str_del = (str(userdel))
    str_del = str_del.replace("Задержка ","")
    str_del = int(str_del)
    await message.reply(f"Отлично. Погрешность составляет {str_del} минут.\nТвои посты буду выходить раз в {str_msg} с погрешностью {str_del}.\nЧтобы начать работать отправь боту текст 'Запустить отправку' либо нажми кнопку на клавиатуре бота")

async def delay_count():
    global delay
    global post
    global time_local
    delay = 60 * (str_msg + randint(0, str_del))
    nowTime = time.time()
    newdelay = nowTime + delay
    time_local = time.localtime(newdelay)
    time.strftime('%H:%M:%S', time_local)
    post = time.strftime('%H:%M:%S', time_local)

async def time_send(delay):
    global give
    end = 1440
    min_send = delay/60
    nowTime = time.time()
    time_local = time.localtime(nowTime)
    hour = time_local[3] * 60
    minute = time_local[4]
    minute_total_now = hour + minute
    difference = end - minute_total_now
    print(difference)
    diff = min_send > difference
    print(diff)
    if diff == True:
        give = False
       
@dp.message_handler(Text(equals='Запустить отправку',ignore_case=True))
async def process_parser_command(message: types.Message):
    global give
    global posts
    give = True
    print(give)
    await bot.send_message(message.chat.id, 'Запускаю отправку')
    while give == True:
        await time_Main1()
        if delta_time:
            await delay_count()
            await time_send(delay)
            print(give)
            if delta_time and give == True:
                posts = post_checker.check_post()
                main_result = post_checker.main_result
                if main_result == 0:
                    await bot.send_message(admin_id, f"{posts}. Отпрвлять нечего")
                    while main_result == 0:
                        await asyncio.sleep(5)
                        main_result = post_checker.main_result                        
                else:
                    await presender.presend_smthg()
                    await bot.send_message(admin_id, f'Следующий пост в {post}\n{posts}')
                    await message.answer("Нажмите чтобы удалить пост", reply_markup=keyboard)
                    await asyncio.sleep(delay) 
                    await give_bot.send_smthg()           
        else:
            await asyncio.sleep(5)
    else:
        await bot.send_message(message.chat.id, f'Отправка приостановлена')

@dp.callback_query_handler(text="delete")
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await deleter.delete_smthg()
    await bot.send_message(callback_query.from_user.id,'Неугодный пост удален')
    posts = post_checker.check_post()
    main_result = post_checker.main_result
    if main_result == 0:
        await bot.send_message(admin_id, f"{posts}. Отпрвлять нечего")
    else:
        await presender.presend_smthg()
        await bot.send_message(admin_id, f'Следующий пост в {post}\n{posts}')
        await bot.send_message(admin_id, "Нажмите чтобы удалить пост", reply_markup=keyboard)

@dp.message_handler(Text(equals='Удалить',ignore_case=True))
async def process_del_command(message: types.Message):
    await deleter.delete_smthg()
    await message.reply('Неугодный пост удален')
    posts = post_checker.check_post()
    main_result = post_checker.main_result
    if main_result == 0:
        await bot.send_message(admin_id, f"{posts}. Отпрвлять нечего")
    else:
        await presender.presend_smthg()
        await bot.send_message(admin_id, f'Следующий пост в {post}\n{posts}')
    

@dp.message_handler(Text(equals='Остановить отправку',ignore_case=True))
async def process_parser_command(message: types.Message):
    global give
    give = False
    print(give)
    await bot.send_message(message.chat.id,f'Остановка работы отправки')
    
