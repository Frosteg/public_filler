from connector import dp
from aiogram.utils import executor
import logging



async def bot_online(_):  
    print('Я готов!')

logging.basicConfig(level=logging.INFO)
#logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                   # level=logging.DEBUG)

import exec

executor.start_polling(dp, skip_updates=True, on_startup=bot_online)

