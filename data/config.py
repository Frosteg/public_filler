import sqlite3
token="your_bot_token"
chat_link = 'your_chat_link'
channel_id = 'your_channel_id'
admin_id = 'your_id'

send = f'<a href="{chat_link}">*your_chanel_name*</a>' #caption 

conn = sqlite3.connect('data/database.db')
cur = conn.cursor()

up = 1
sent = 0