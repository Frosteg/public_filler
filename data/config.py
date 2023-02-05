import sqlite3
import time

token="your_bot_token"
chat_link = 'your_chat_link'
channel_id = 'your_channeil_id'
admin_id = 'your_id'

send = f'<a href="{chat_link}">*your_chanel_name*</a>' #caption 

conn = sqlite3.connect('data/database.db')
cur = conn.cursor()

up = 1
sent = 0

begin = 480
end = 1380
day = 1440

time_start = time.gmtime(begin*60)
start_time = time.strftime('%H:%M:%S', time_start)

time_end = time.gmtime(end*60)
end_time = time.strftime('%H:%M:%S', time_end)
