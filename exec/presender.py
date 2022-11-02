from aiogram import types
from connector import  bot
from data.config import send, cur, admin_id

print('К отправке готов!')

async def presend_smthg():
    InputMediaPhoto = types.InputMediaPhoto
    cur.execute("SELECT file_id FROM Content where sent = 0 LIMIT 1")                           #выбирает ссылку поста еще не отправленую
    result = cur.fetchone()
    if result == None:
        await bot.send_message(admin_id, "Контент закончился! Необходимо пополнить!")                                #Если результат выборки None - отправить особщение
    else:                                                                                   #Если есть результат - запустить процесс отправки
        last_sent = result[0]
        cur.execute(f"SELECT group_id FROM Content where file_id = '{last_sent}'")                     #Проверить Group_id выбраннго поста
        result_id = cur.fetchone()[0]
        if result_id != 'NotGroup':
            cur.execute(f"SELECT * FROM Content where group_id = '{result_id}'")                     #Выбрать ссылки по выбраному посту
            results_id = cur.fetchall()
            count = len(results_id)
            if count > 1:
                group = len(results_id)                                                                   #подсчет количества ссылок
                maxtop = 10                                                                         #максимальное количество медиа в посте
                if group != 1:                                                                      #если количество ссылок больше 1 - формировать media_group
                    mediagroup = [] 
                    p = len(mediagroup) 
                    for row in results_id:
                        photo = row[0]
                        if p == 0:
                            mediagroup.append(InputMediaPhoto(photo, send, parse_mode='html'))
                            p = p+1
                            if p == 1:   
                                continue
                        if p >= 1:
                            mediagroup.append(InputMediaPhoto(photo))
                            p = p+1
                            if p == maxtop:   
                                break            
                    await bot.send_media_group(admin_id, media=mediagroup)
    if result_id == 'NotGroup':               
        cur.execute(f"SELECT mes_type FROM Content where file_id = '{last_sent}'")    
        exp_id = cur.fetchone()[0]
        print(f'Mestype: {exp_id}')
        if exp_id == "Photo":                                                             #если категория Картинки
            photo = last_sent
            await bot.send_photo(admin_id, photo, send)
        elif exp_id == "Video":                                                             #если категория Видео
            photo = last_sent
            await bot.send_video(admin_id,photo)
        elif exp_id == "Animation":                                                             #если категория Видео
            photo = last_sent
            await bot.send_animation(admin_id, photo, caption=send)
        elif exp_id == "Document":                                                             #если категория Видео
            photo = last_sent
            await bot.send_document(admin_id, photo, caption=send)

'''
@dp.message_handler(commands=['sender'])
async def process_parser_command(message: types.Message):
    await send_smthg()
'''