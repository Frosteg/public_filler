from aiogram_media_group import media_group_handler
from aiogram import types
from connector import dp, bot
from data.config import cur, conn, admin_id, sent
from exec import post_checker
from aiogram.dispatcher.filters import MediaGroupFilter
from typing import List

print('Паехали! Жду контент!!!')

cur.execute("CREATE TABLE IF NOT EXISTS Content('file_id' BLOB, 'group_id' TEXT, 'mes_type' TEXT, 'sent' INT)")
conn.commit() 

async def data_collector(message: types.Message):
    global file_id
    global mes_type
    if message.photo:
        mes_type = 'Photo'
        file_id = message.photo[0].file_id
    elif message.video:
        mes_type = 'Video'
        file_id = message.video.file_id
    elif message.document:
        mes_type = 'Document'
        file_id = message.document.file_id
    elif message.animation:
        mes_type = 'Animation'
        file_id = message.animation.file_id
    group_id = message.media_group_id
    if group_id == None:
        group_id = 'NotGroup'
    
    cur.execute(f"SELECT * FROM 'Content' where 'file_id' = '{file_id}'")
    if cur.fetchone() is None:
        rss_input= (file_id, group_id, mes_type, sent)
        cur.execute(f"INSERT INTO 'Content' (file_id,group_id, mes_type, sent) VALUES(?, ?, ?, ?);", rss_input)
        conn.commit()

@dp.message_handler(MediaGroupFilter(is_media_group=True), content_types=['photo', 'video', 'animation'])
@media_group_handler
async def album_handler(messages: List[types.Message]):
    for message in messages:
        await data_collector(message)
    posts = post_checker.check_post() 
    await bot.send_message(admin_id, f'Файл получен и добавлен в бд\n{posts}')
    
@dp.message_handler(content_types=['photo','video','animation'])
async def process_parser(message: types.Message):
    await data_collector(message)
    posts = post_checker.check_post() 
    await bot.send_message(admin_id, f'Файл получен и добавлен в бд\n{posts}')
