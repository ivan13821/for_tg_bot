import asyncio
from aiogram import Bot, Dispatcher
from Homework import main
from economik_game import main_game
from config import *






async def maiin():
    bot = Bot(token=API_TOKEN)

    dp = Dispatcher()

    dp.include_routers(main_game.router, main.router)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(maiin())