import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.handlers import router
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    '''Основная асинхронная функция, которая запускает бота.'''
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO) # Логирование для дебага
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Обработка прерывания от клавиатуры (Ctrl+C)
        print('Выход')