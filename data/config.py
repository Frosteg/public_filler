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

end = 1440
begin = 480

time_start = begin*60
time_start = time.gmtime(time_start)
start_time = time.strftime('%H:%M:%S', time_start)

time_end = end*60
time_end = time.gmtime(time_end)
end_time = time.strftime('%H:%M:%S', time_end)
