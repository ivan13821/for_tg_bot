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
from keyboard import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)

dp = Dispatcher()


class MyForm(StatesGroup):
    message_from_all = State()
    join_or_create = State()
    game = State()
    choice = State()
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

        await message_from_list(state_message, users)

        await state.clear()


@dp.message(F.text == 'Завершить все операции связанные с игрой')
async def stop_all_op(message: types.Message, state: FSMContext):

    """"Удаление пользователя из БД"""


    del game_db[(x := found_user_on_lobbyes(message))]['users'][message.chat.id]

    if game_db[x]['users'] == {}:
        del game_db[x]

    await state.clear()

    await message.answer('Все ваши операции связанные с игрой завершены', reply_markup=MyKeyboard.join_create())




@dp.message(StateFilter(None), F.text == '/game')
async def start_game(message: types.Message, state: FSMContext):

    """Первый шаг при запуске/приединение к игре"""

    await message.answer("Вы хотите начать новую игру или присоединиться к существующей?", reply_markup=MyKeyboard.join_create())
    await state.set_state(MyForm.join_or_create)



@dp.message(MyForm.join_or_create, F.text == 'Начать новую игру')
async def step_start_1(message: types.Message, state: FSMContext):

    """Функция описывает 1 шаг при создании лоббии"""

    id_lobby = create_lobby(message)


    if type(id_lobby) == type(1):
        await message.answer(f'id лобби: {id_lobby}', reply_markup=MyKeyboard.A_B_C())
        await message.answer('Выберете пожалуйста кокой вариант ресурсов вы хотели бы получить при начале игры')
        await message.answer('Вариант А\n'
                             'деньги: 4000\n'
                             'Здание: 7 ед\n'
                             'Сырье: 30 ед\n'
                             '\n'
                             'Вариант Б\n'
                             'Деньги: 4000\n'
                             'Оборудование: 14 ед\n'
                             'Рабочие: 18 ед\n'
                             '\n'
                             'Вариант В\n'
                             'Деньги: 4000\n'
                             'Технология: 10 ед\n'
                             'Транспорт: 12 ед\n')

        await state.set_state(MyForm.choice)
    else:
        await message.answer(f'{id_lobby}', reply_markup=MyKeyboard.back_del_op())




@dp.message(MyForm.join_or_create, F.text == 'Присоединиться')
async def join_to_lobby(message: types.Message, state: FSMContext):

    """Для присоединения человека к лобби, ввод id на след шаге"""

    await message.answer('Введите id лобби к которому вы хотите подключиться', reply_markup=ReplyKeyboardRemove())
    await state.set_state(MyForm.input_id)



@dp.message(MyForm.input_id)
async def input_id(message: types.Message, state: FSMContext):

    """Получение id"""

    result_add = add_user_on_group(message.text, message)
    await message.answer(result_add, reply_markup=MyKeyboard.back_on_menu())
    if result_add == 'Вы успешно добавленны в игру':
        await message_from_list(f'К игре присоединился: {message.chat.username}', list(game_db[int(message.text)]['users'].keys()), but_id=message.chat.id)
        await message.answer('Выберете пожалуйста кокой вариант ресурсов вы хотели бы получить при начале игры', reply_markup=MyKeyboard.A_B_C())
        await message.answer('Вариант А\n'
                             'деньги: 4000\n'
                             'Здание: 7 ед\n'
                             'Сырье: 30 ед\n'
                             '\n'
                             'Вариант Б\n'
                             'Деньги: 4000\n'
                             'Оборудование: 14 ед\n'
                             'Рабочие: 18 ед\n'
                             '\n'
                             'Вариант В\n'
                             'Деньги: 4000\n'
                             'Технология: 10 ед\n'
                             'Транспорт: 12 ед\n')

        await state.set_state(MyForm.choice)



@dp.message(MyForm.choice)
async def game(message: types.Message, state: FSMContext):

    """Пользователь выбирает какой вариант ресурсов он хочет получить"""
    if message.text == 'Выйти в меню':
        del game_db[(x := found_user_on_lobbyes(message))]['users'][message.chat.id]

        if game_db[x]['users'] == {}:
            del game_db[x]

        await message.answer('Вы вышли в основное меню', reply_markup=MyKeyboard.menu())
        await state.clear()

    if message.text == 'А':
        await message.answer(message.text)
        await state.set_state(MyForm.game)
    elif message.text == 'Б':
        await message.answer(message.text)
        await state.set_state(MyForm.game)
    elif message.text == 'В':
        await message.answer(message.text)
        await state.set_state(MyForm.game)
    else:
        await message.answer('Выберете пожалуйста вариант из всплывающей клавиатуры')
        await state.set_state(MyForm.choice)



@dp.message(MyForm.game)
async def game(message: types.Message, state: FSMContext):

    """Обработчик внутри игровых событий"""

    if message.text == 'Выйти в меню':
        del game_db[(x := found_user_on_lobbyes(message))]['users'][message.chat.id]

        if game_db[x]['users'] == {}:
            del game_db[x]

        await message.answer('Вы вышли в основное меню', reply_markup=MyKeyboard.menu())
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