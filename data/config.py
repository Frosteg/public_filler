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
