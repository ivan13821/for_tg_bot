import logging
from aiogram.fsm.state import StatesGroup, State

from economik_game.economik_game import EconomicGame
from Homework.func import *
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from economik_game.database_config import users
from economik_game.keyboard import *
from bot_config import *
from Homework.database import *

bot = Bot(token=API_TOKEN)

logging.basicConfig(level=logging.INFO)

router = Router()

class MyForm(StatesGroup):
    message_from_all = State()
    join_or_create = State()
    game = State()
    choice = State()
    input_id = State()
    stop_op = State()
    input_name = State()
    production_option = State()
    reference = State()

@router.message(Command(commands=["send_all"]))
async def admin_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if str(user_id) == str(admin_id):
        await message.answer('Напишите сообщение для рассылки')
        await state.set_state(MyForm.message_from_all)
        # Ожидаем ответ админа


async def message_from_user(user_id, message):

    """Отправка сообщения пользователю по id"""

    await bot.send_message(user_id, message)


@router.message(MyForm.message_from_all)
async def handle_message_for_broadcast(message: types.Message, state: FSMContext):

    """Отправка сообщений всем"""

    state_message = message.text
    user_id = message.from_user.id
    if str(user_id) == str(admin_id):

        await EconomicGame.message_from_list(state_message, users)






@router.message(F.text == '/about_bot')
async def about_bot(message: types.Message):

    """Функция рассказывает о назначении бота"""

    await message.answer("Этот бот был создан для облегчения поиска домашнего задания для студентов. Здесь его существенно проще найти, и не нужно ждуть пока тебе ответят твои друзья)")









@router.message(F.text, lambda m: m.text in ['ПИЗИ23о2', 'ПИЗИ23о1'])
async def group_post(message: types.Message):

    testing_database[message.text] = {
        'id':message.chat.id,
        'sent_message':False,
                                      }

    await message.answer(f'Вы добавленны в группу {message.text}\U0001f44d')







@router.message(F.text, Command("start"))
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









@router.message(F.text)
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





@router.message()
async def error(message: types.Message):
    await message.answer('Вы отправили не текстовое сообщение')





