import sqlite3
import datetime

token="your_bot_token"
chat_link = 'your_chat_link'
channel_id = 'your_channeil_id'
admin_id = 'your_id'

send = f'<a href="{chat_link}">*your_chanel_name*</a>' #caption 

conn = sqlite3.connect('data/database.db')
cur = conn.cursor()

up = 1
sent = 0

main_start1 = datetime.time(8,00,0) #время начала отправки постов
main_end1 = datetime.time(23,59,0) #время конца отправки постов
date_time = datetime.datetime.now().time()

end = 1439 #количество минут  от полуночи до установленного в main_end1 времени
