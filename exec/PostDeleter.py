from data.config import  cur, conn, up, admin_id
from connector import dp, bot

print('К удалению готов!')

async def delete_smthg():
    cur.execute("SELECT file_id FROM Next_to_send LIMIT 1")                           #выбирает ссылку поста еще не отправленую
    result = cur.fetchone()
    if result == None:
        await bot.send_message(admin_id, "Контент закончился! Необходимо пополнить!")
        return                         #Если реультат выборки None - отправить особщение
    else:                                                                                   #Если есть результат - запустить процесс отправки
        last_sent = result[0]
        cur.execute(f"SELECT group_id FROM Next_to_send where file_id = '{last_sent}'")                     #Выбрать ссылки по выбраному посту
        result_id = cur.fetchone()[0]
        if result_id != 'NotGroup':
            cur.execute(f"UPDATE Content set sent = '{up}' where group_id = '{result_id}'")       #обновление данных таблицы все вхождения по ссылке поста - отметить 1
            conn.commit()   
        if result_id == 'NotGroup':
            cur.execute(f"DELETE FROM Content WHERE file_id = '{last_sent}'")          #обновление данных таблицы все вхождения по ссылке поста - отметить 1
            conn.commit()         
    cur.execute("SELECT * FROM Next_to_send")
    cur.execute("DELETE FROM Next_to_send")
    conn.commit
