from aiogram import types
from connector import bot
from data.config import channel_id, send, up, cur, conn, admin_id

print('К отправке готов!')

async def send_smthg():
    InputMediaPhoto = types.InputMediaPhoto
    cur.execute("SELECT file_id FROM Next_to_send LIMIT 1")                           #выбирает ссылку поста еще не отправленую
    result = cur.fetchone()
    if result == None:
        sender = await bot.send_message(admin_id, "Контент закончился! Необходимо пополнить!")                                #Если реультат выборки None - отправить особщение
    else:                                                                                   #Если есть результат - запустить процесс отправки
        last_sent = result[0]
        cur.execute(f"SELECT group_id FROM Next_to_send where file_id = '{last_sent}'")                     #Выбрать ссылки по выбраному посту
        result_id = cur.fetchone()[0]
        if result_id != 'NotGroup':
            cur.execute(f"SELECT * FROM Next_to_send where group_id = '{result_id}'")                     #Выбрать ссылки по выбраному посту
            results_id = cur.fetchall()
            count = len(results_id)
            if count > 1:
                group = len(results_id)                                                                   #подсчет количества ссылок
                maxtop = 10                                                                         #максимальное количество медиа в посте
                if group != 1:                                                                      #если количество ссылок больше 1 - формировать media_group
                    mediagroup = [] 
                    p = len(mediagroup) 
                    for row in results_id:                                                            #если категория - Картинки формировать в медиагруп и отправлять с помощью send_group_media
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
                    sender = await bot.send_media_group(channel_id, media=mediagroup)
                cur.execute(f"UPDATE Content set sent = '{up}' where group_id = '{result_id}'")       #обновление данных таблицы все вхождения по ссылке поста - отметить 1
                conn.commit()                    
        if result_id == 'NotGroup':                                                                #если найдена 1 ссылка в таблице
            cur.execute(f"SELECT mes_type FROM Next_to_send where file_id = '{last_sent}'")    
            exp_id = cur.fetchone()[0]
            if exp_id == "Photo":                                                             #если категория Картинки
                photo = last_sent
                sender = await bot.send_photo(channel_id, photo, send)
                cur.execute(f"UPDATE Content set sent = '{up}' where file_id = '{last_sent}';")#обновление данных таблицы все вхождения по ссылке поста - отметить 1
                conn.commit()
            elif exp_id == "Video":                                                             #если категория Видео
                photo = last_sent
                sender = await bot.send_video(channel_id,photo, caption=send)
                cur.execute(f"UPDATE Content set sent = '{up}' where file_id = '{last_sent}';")#обновление данных таблицы все вхождения по ссылке поста - отметить 1
                conn.commit()
            elif exp_id == "Animation":                                                             #если категория Видео
                photo = last_sent
                sender = await bot.send_animation(channel_id, photo, caption=send)
                cur.execute(f"UPDATE Content set sent = '{up}' where file_id = '{last_sent}';")#обновление данных таблицы все вхождения по ссылке поста - отметить 1
                conn.commit()
            elif exp_id == "Document":                                                             #если категория Видео
                photo = last_sent
                sender = await bot.send_document(channel_id, photo, caption=send)
                cur.execute(f"UPDATE Content set sent = '{up}' where file_id = '{last_sent}';")#обновление данных таблицы все вхождения по ссылке поста - отметить 1
                conn.commit()
    return sender     
