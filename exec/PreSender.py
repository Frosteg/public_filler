from aiogram import types
from connector import bot
from data.config import channel_id, send, up, cur, conn, admin_id

print('К отправке готов!')

cur.execute("CREATE TABLE IF NOT EXISTS Next_to_send('file_id' BLOB, 'group_id' TEXT, 'mes_type' TEXT)")
conn.commit() 

async def presend_smthg():
    InputMediaPhoto = types.InputMediaPhoto
    cur.execute("SELECT * FROM Next_to_send")
    cur.execute("DELETE FROM Next_to_send")
    conn.commit
    cur.execute("SELECT file_id FROM Content where sent = 0 LIMIT 1")                           #выбирает ссылку поста еще не отправленую
    result = cur.fetchone()
    if result == None:
        sender = await bot.send_message(admin_id, "Контент закончился! Необходимо пополнить!")                                #Если реультат выборки None - отправить особщение
    else:                                                                                   #Если есть результат - запустить процесс отправки
        last_sent = result[0]
        cur.execute(f"SELECT group_id FROM Content where file_id = '{last_sent}'")                     #Выбрать ссылки по выбраному посту
        result_id = cur.fetchone()[0]
        if result_id != 'NotGroup':
            cur.execute(f"SELECT * FROM Content where group_id = '{result_id}'")
            results_id = cur.fetchall()
            for result in results_id:
                row = result
                file_id = row[0]
                group_id = row[1]
                mes_type = row[2]
                inserting = (file_id, group_id, mes_type)
                cur.execute(f"INSERT INTO Next_to_send (file_id,group_id, mes_type) VALUES (?,?,?);", inserting)
                conn.commit()
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
                    sender = await bot.send_media_group(admin_id, media=mediagroup)
        if result_id == 'NotGroup':
            cur.execute(f"SELECT * FROM Content where file_id = '{last_sent}'") 
            row = cur.fetchall()[0]
            file_id = row[0]
            group_id = row[1]
            mes_type = row[2]
            inserting = (file_id, group_id, mes_type)
            cur.execute(f"INSERT INTO Next_to_send (file_id,group_id, mes_type) VALUES (?,?,?);", inserting)
            conn.commit()
            if mes_type == "Photo":                                                             #если категория Картинки
                photo = last_sent
                sender = await bot.send_photo(admin_id, photo, send)
            elif mes_type == "Video":                                                             #если категория Видео
                photo = last_sent
                sender = await bot.send_video(admin_id,photo, caption=send)
            elif mes_type == "Animation":                                                             #если категория Видео
                photo = last_sent
                sender = await bot.send_animation(admin_id, photo, caption=send)
            elif mes_type == "Document":                                                             #если категория Видео
                photo = last_sent
                sender = await bot.send_document(admin_id, photo, caption=send)
    return sender 
