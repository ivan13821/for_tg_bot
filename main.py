import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.state import StatesGroup, State
from config import *
from database import *
from func import *
from game import *
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove
from database_config import users


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)

dp = Dispatcher()


class MyForm(StatesGroup):
    message_from_all = State()
    join_or_create = State()
    game = State()
    input_id = State()

@dp.message(Command(commands=["send_all"]))
async def admin_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if str(user_id) == str(admin_id):
        await message.answer('Напишите сообщение для рассылки')
        await state.set_state(MyForm.message_from_all)
        # Ожидаем ответ админа


@dp.message(MyForm.message_from_all)
async def handle_message_for_broadcast(message: types.Message, state: FSMContext):

    """Отправка сообщений всем"""

    state_message = message.text
    user_id = message.from_user.id
    if str(user_id) == str(admin_id):
    # Получаем список всех пользователей
        for user_id in users:
        # Отправляем сообщение каждому пользователю
            await bot.send_message(user_id, state_message)

        await state.clear()


@dp.message(F.text == 'Завершить все операции связанные с игрой')
async def stop_all_op(message: types.Message, state: FSMContext):

    """"Удаление пользователя из БД"""


    del game_db[(x := found_user_on_lobbyes(message))]['users'][message.chat.id]

    if game_db[x]['users'] == {}:
        del game_db[x]

    kb = [
        [types.KeyboardButton(text="Начать новую игру"), types.KeyboardButton(text="Присоединиться")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)

    await state.clear()

    await message.answer('Все ваши операции связанные с игрой завершены', reply_markup=keyboard)




@dp.message(StateFilter(None), F.text == '/game')
async def start_game(message: types.Message, state: FSMContext):

    """Первый шаг при запуске/приединение к игре"""

    kb = [
        [types.KeyboardButton(text="Начать новую игру"), types.KeyboardButton(text="Присоединиться")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Вы хотите начать новую игру или присоединиться к существующей?", reply_markup=keyboard)
    await state.set_state(MyForm.join_or_create)



@dp.message(MyForm.join_or_create, F.text == 'Начать новую игру')
async def step_start_1(message: types.Message, state: FSMContext):

    """Функция описывает 1 шаг при создании лоббии"""

    id_lobby = create_lobby(message)


    if type(id_lobby) == type(1):
        kb = [
            [types.KeyboardButton(text="Операции в игре..."),
             types.KeyboardButton(text="Выйти в меню")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        await message.answer(f'id лобби: {id_lobby}', reply_markup=keyboard)
    else:
        kb = [
            [types.KeyboardButton(text="Завершить все операции связанные с игрой"),
             types.KeyboardButton(text="Выйти в меню")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        await message.answer(f'{id_lobby}', reply_markup=keyboard)

    await state.set_state(MyForm.game)



@dp.message(MyForm.join_or_create, F.text == 'Присоединиться')
async def join_to_lobby(message: types.Message, state: FSMContext):

    """Для присоединения человека к лобби, ввод id на след шаге"""

    await message.answer('Введите id лобби к которому вы хотите подключиться', reply_markup=ReplyKeyboardRemove())
    await state.set_state(MyForm.input_id)



@dp.message(MyForm.input_id)
async def join_to_lobby(message: types.Message, state: FSMContext):

    """Получение id"""

    kb = [
        [types.KeyboardButton(text="Операции в игре..."),
         types.KeyboardButton(text="Выйти в меню")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer(add_user_on_group(message.text, message), reply_markup=keyboard)
    await state.set_state(MyForm.game)


@dp.message(MyForm.game)
async def join_to_lobby(message: types.Message, state: FSMContext):

    """Обработчик внутри игровых событий"""

    if message.text == 'Выйти в меню':
        del game_db[(x := found_user_on_lobbyes(message))]['users'][message.chat.id]

        if game_db[x]['users'] == {}:
            del game_db[x]

        kb = [
            [types.KeyboardButton(text="Меню")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        await message.answer('Вы вышли в соновное меню', reply_markup=keyboard)
        await state.clear()
    else:
        state_message = str(message.chat.username)+': '+message.text
        lobby_id = found_user_on_lobbyes(message)
        for user_id in game_db[lobby_id]['users'].keys():
            if user_id == message.chat.id:
                continue
            await bot.send_message(user_id, state_message)






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

    if (x := message.chat.id) not in users:
        users.append(x)


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
            #print(message.text.lower().split(':')[0])

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