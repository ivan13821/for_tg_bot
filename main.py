import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config import *
from database import *
from func import *
from magic_filter import F
from game import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)

dp = Dispatcher()






@dp.message(F.text == 'Завершить все операции связанные с игрой')
async def about_bot(message: types.Message):

    """"Удаление пользователя из БД и обнуление в счетчике"""

    kb = [
        [types.KeyboardButton(text="Начать новую игру"), types.KeyboardButton(text="Присоединиться")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)

    for i in game_db.keys():
        if (x := message.chat.id) in list(game_db[i]['users'].keys()):
            del game_db[i]['users'][x]
            if game_db[i]['users'] == {}:
                print(1)
                del game_db[i]
            break

    step_game[message.chat.id] = 0

    await message.answer('Все ваши операции связанные с игрой завершены', reply_markup=keyboard)




@dp.message(F.text == '/game')
async def about_bot(message: types.Message):

    """Первый шаг при запуске/приединение к игре"""

    kb = [
        [types.KeyboardButton(text="Начать новую игру"), types.KeyboardButton(text="Присоединиться")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Вы хотите начать новую игру или присоединиться к существующей?", reply_markup=keyboard)



@dp.message(F.text == 'Начать новую игру')
async def about_bot(message: types.Message):

    """Функция описывает 1 шаг при создании лоббии"""

    id_lobby = create_lobby(message)

    kb = [
        [types.KeyboardButton(text="Завершить все операции связанные с игрой"), types.KeyboardButton(text="Назад")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)

    if type(id_lobby) == type(1):
        await message.answer(f'id лобби: {id_lobby}')
    else:
        await message.answer(f'{id_lobby}', reply_markup=keyboard)




@dp.message(F.text == '/about_bot')
async def about_bot(message: types.Message):

    """Функция рассказывает о назначении бота"""

    await message.answer("Этот бот был создан для облегчения поиска домашнего задания для студентов. Здесь его существенно проще найти, и не нужно ждуть пока тебе ответят твои друзья)")










@dp.message(F.text, lambda m: m.text in ['ПИЗИ23о2', 'ПИЗИ23о1'])
async def group_post(message: types.Message):

    testing_database[message.text] = {
        'id':message.chat.id,
        'sent_message':False,
                                      }

    await message.answer(f'Вы добавленны в группу {message.text}\U0001f44d')







@dp.message(F.text, Command("start"))
async def cmd_start(message: types.Message):


    await message.answer("*Чтобы добавить задание на предмет вам нужно*:\n"
                         "Написать название предмета ; потом написать дату на которую это"
                         "задание было задано потом ; а потом само задание.\n"
                         ""
                         "*Предмет; Дата; Задание*",parse_mode="Markdown")
    await message.answer("Если вы хотите получить задание на определенную дату, то вам нужно написать название предмета потом"
                         "; а потом дату.\n"                                                              
                         "*Предмет; Дата*\n"
                         "\n"
                         "Если же вы хотите получить все задания по предмету вам нужно просто написать название предмета\n"
                         "*Предмет*",parse_mode="Markdown")









@dp.message(F.text)
async def input_message(message: types.Message):

    if in_group(message):
        print(message.text.lower().split(':')[0])

        if len(message.text.lower().split(';')) == 3:
            if admin(message):
                my_message = post_db(message)
            else:
                my_message = ['Для добавления задания вы должны обладать правами администратора']
        elif message.text.lower().split(':')[0] in ['мой пароль']:
            my_message = [add_admin(message)]
        elif len(message.text.lower().split(';')) <= 2:
            #print(get_db(message))
            my_message = get_db(message)
        else:
            my_message = 'Вы ввели неправильный шаблон'

        for i in my_message:
            await message.answer(i)
    else:
        await message.answer('Нужно сначала указать вашу группу')





@dp.message()
async def error(message: types.Message):
    await message.answer('Вы отправили не текстовое сообщение')








async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())