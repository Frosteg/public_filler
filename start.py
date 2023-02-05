from connector import dp
from aiogram.utils import executor
import logging
async def bot_online(_):  
    print('Я готов!')

logging.basicConfig(level=logging.INFO, filename="data/py_log.log",filemode="a",format="%(asctime)s %(levelname)s %(message)s")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")

import exec

executor.start_polling(dp, skip_updates=True, on_startup=bot_online)

