import asyncio
import logging
from os import getenv

from aiogram.fsm.storage.memory import MemoryStorage

from config import *
from aiogram import Bot, Dispatcher, types
from hendlers import router
TOKEN = getenv(TG_TOKEN)
bot = Bot(token=TG_TOKEN)


dp = Dispatcher(storage=MemoryStorage())


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
