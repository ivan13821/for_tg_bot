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
    stop_op = State()
    input_name = State()

@dp.message(Command(commands=["send_all"]))
async def admin_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if str(user_id) == str(admin_id):
        await message.answer('Напишите сообщение для рассылки')
        await state.set_state(MyForm.message_from_all)
        # Ожидаем ответ админа


async def message_from_user(user_id, message):

    """Отправка сообщения пользователю по id"""

    await bot.send_message(user_id, message)


@dp.message(MyForm.message_from_all)
async def handle_message_for_broadcast(message: types.Message, state: FSMContext):

    """Отправка сообщений всем"""

    state_message = message.text
    user_id = message.from_user.id
    if str(user_id) == str(admin_id):

        await Game.message_from_list(state_message, users)

        await state.clear()


@dp.message(MyForm.stop_op)
async def stop_all_op(message: types.Message, state: FSMContext):

    """"Удаление пользователя из БД"""


    del game_db[(x := users_l[message.chat.id])]['users'][message.chat.id]
    del users_l[message.chat.id]

    if game_db[x]['users'] == {}:
        del game_db[x]

    await state.clear()

    await message.answer('Все ваши операции связанные с игрой завершены', reply_markup=MyKeyboard.menu())




@dp.message(StateFilter(None), F.text == '/game')
async def start_game(message: types.Message, state: FSMContext):

    """Первый шаг при запуске/приединение к игре"""

    await message.answer("Вы хотите начать новую игру или присоединиться к существующей?", reply_markup=MyKeyboard.join_create())
    await state.set_state(MyForm.join_or_create)



@dp.message(MyForm.join_or_create, F.text == 'Начать новую игру')
async def step_start_1(message: types.Message, state: FSMContext):

    """Функция описывает 1 шаг при создании лоббии"""

    id_lobby = Game.create_lobby(message)


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
        await message.answer(f'{id_lobby}', reply_markup=MyKeyboard.back_on_menu())




@dp.message(MyForm.join_or_create, F.text == 'Присоединиться')
async def join_to_lobby(message: types.Message, state: FSMContext):

    """Для присоединения человека к лобби, ввод id на след шаге"""

    await message.answer('Введите id лобби к которому вы хотите подключиться', reply_markup=ReplyKeyboardRemove())
    await state.set_state(MyForm.input_id)



@dp.message(MyForm.input_id)
async def input_id(message: types.Message, state: FSMContext):

    """Получение id"""

    if message.text == 'Выйти в меню':
        await stop_all_op(message, state)

    result_add = Game.add_user_on_group(message.text, message)
    await message.answer(result_add, reply_markup=MyKeyboard.back_on_menu())
    if result_add == 'Вы успешно добавленны в игру':
        await Game.message_from_list(f'К игре присоединился: {message.chat.username}', list(game_db[int(message.text)]['users'].keys()), but_id=message.chat.id)
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
async def choice(message: types.Message, state: FSMContext):

    """Пользователь выбирает какой вариант ресурсов он хочет получить"""

    if message.text == 'Выйти в меню':
        await stop_all_op(message, state)

    else:
        result = Game.add_start_res(message)
        if result:
            await message.answer('Начальные ресурсы получены', reply_markup=ReplyKeyboardRemove())
            await message.answer('Введите пожалуста ник под которым вы будете играть (ник не должен быть больше 10 символов)')
            await state.set_state(MyForm.input_name)
        else:
            await message.answer('Выберете пожалуйста вариант из всплывающей клавиатуры')
            await state.set_state(MyForm.choice)





@dp.message(MyForm.input_name)
async def game(message: types.Message, state: FSMContext):

    """Пользователь пишет свой ник"""

    if message.text == 'Выйти в меню':
        await stop_all_op(message, state)

    else:

        if len(list(message.text)) > 10:
            await message.answer(f'Введите пожалуста ник до 10 символов')
            await state.set_state(MyForm.input_name)
        else:

            for i in users_name.keys():
                if users_name[i]['nik'] == message.text:
                    await message.answer('К сожалению этот ник уже занят, напишите пожалуйста другой')
                    await state.set_state(MyForm.input_name)
                    break
            else:
                users_name[message.chat.id] = {'nik':message.text, 'username':message.chat.username}
                #print(users_name)
                await message.answer(f'Вы в игре под ником {message.text.strip()}', reply_markup=MyKeyboard.menu_in_game())
                await state.set_state(MyForm.game)






@dp.message(MyForm.game)
async def game(message: types.Message, state: FSMContext):

    """Обработчик внутри игровых событий"""

    if message.text == 'Выйти в меню':
        await stop_all_op(message, state)
    if message.text == 'История':
        await Game.show_operations(message)

    elif message.text == 'Мои ресурсы':

        result_message = ''
        for i in game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы'].items():
            result_message = result_message+f'{i[0]}: {i[1]}\n'
        await message_from_user(message.chat.id, result_message)

    elif message.text == 'Биржа':
        result_message = ''
        for i in back_game['ресурсы'].items():
            result_message = result_message + f'{i[0]}: {i[1]}\n'
        await message_from_user(message.chat.id, result_message)

    elif message.text == 'Шаблоны':
        await message.answer('Шаблон 1 (покупка или продажа):\n'
                             '*| действие | пользователь | ресурс | количество | цена\n*'
                             'Пример:\n'
                             '*купить иван сырье 5 500\n*'
                             '(Покупка у пользователя под ником "иван" ресурс "сырье" в количестве 5 шт и по цене 500 д.ед)', parse_mode="Markdown")
        await message.answer('Если вы продаете или покапаете ресурсы на биржу, то не нужно указывать цену',
                             parse_mode="Markdown")

        await message.answer('Шаблон 2 (обмен ресурсами):\n'
                             '| действие | 2 сторона | ресурс 1 | количество рес 1 | ресурс 2 | количество рес 2 | *ресурс 1 идет вам*|\n'
                             'Например\n'
                             '*обмен олег сырье 7 оборудование 2*', parse_mode="Markdown")

    elif 'купить' in message.text.lower():
        await message.answer(Game.bye(message), parse_mode="Markdown")


    elif 'продать' in message.text.lower():
        await message.answer(Game.sold(message), parse_mode="Markdown")

    elif 'обменять' in message.text.lower() or 'обмен' in message.text.lower():
        await message.answer(Game.swap(message), parse_mode="Markdown")

    elif message.text == 'Список игроков':

        result = ''
        for i in game_db[users_l[message.chat.id]]['users'].keys():
            result += f'{users_name[i]['username']}: {users_name[i]['nik']}\n'

        await message.answer(result)

    else:
        state_message = str(message.chat.username)+': '+message.text
        lobby_id = users_l[message.chat.id]
        for user_id in game_db[lobby_id]['users'].keys():
            if user_id == message.chat.id:
                continue
            await message_from_user(user_id, state_message)






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

            if len(message.text.lower().split(';')) == 3:
                if admin(message):
                    my_message = post_db(message)
                else:
                    my_message = ['Для добавления задания вы должны обладать правами администратора']
            elif message.text.lower().split(':')[0] in ['мой пароль']:
                my_message = [add_admin(message)]
            elif len(message.text.lower().split(';')) <= 2:
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