import asyncio
import logging
from itertools import count

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config import *
from database import *
from func import *
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from magic_filter import F


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)

dp = Dispatcher()

user_data = {}



def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="1", callback_data="num_one"),
            types.InlineKeyboardButton(text="2", callback_data="num_two"),
            types.InlineKeyboardButton(text="3", callback_data="num_three"),
            types.InlineKeyboardButton(text="4", callback_data="num_four"),
            types.InlineKeyboardButton(text="5", callback_data="num_five"),
            types.InlineKeyboardButton(text="6", callback_data="num_six"),
            types.InlineKeyboardButton(text="7", callback_data="num_seven"),
            types.InlineKeyboardButton(text="8", callback_data="num_eight"),
            types.InlineKeyboardButton(text="9", callback_data="num_nine")
        ],
        [types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def update_num_text(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"id лобби: {new_value}",
            reply_markup=get_keyboard()
        )

@dp.message(Command("game"))
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = ''
    await message.answer("Придумайти id лобби", reply_markup=get_keyboard())


@dp.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: types.CallbackQuery):
    user_value = user_data.get(callback.from_user.id, '')
    action = callback.data.split("_")[1]

    if action == "one":
        user_data[callback.from_user.id] = user_value+'1'
        await update_num_text(callback.message, user_value+'1')
    elif action == "two":
        user_data[callback.from_user.id] = user_value+'2'
        await update_num_text(callback.message, user_value+'2')
    elif action == "three":
        user_data[callback.from_user.id] = user_value+'3'
        await update_num_text(callback.message, user_value+'3')
    elif action == "four":
        user_data[callback.from_user.id] = user_value+'4'
        await update_num_text(callback.message, user_value+'4')
    elif action == "five":
        user_data[callback.from_user.id] = user_value+'5'
        await update_num_text(callback.message, user_value+'5')
    elif action == "six":
        user_data[callback.from_user.id] = user_value+'6'
        await update_num_text(callback.message, user_value+'6')
    elif action == "seven":
        user_data[callback.from_user.id] = user_value+'7'
        await update_num_text(callback.message, user_value+'7')
    elif action == "eight":
        user_data[callback.from_user.id] = user_value+'8'
        await update_num_text(callback.message, user_value+'8')
    elif action == "nine":
        user_data[callback.from_user.id] = user_value+'9'
        await update_num_text(callback.message, user_value+'9')
    elif action == "finish":
        if list(user_data.values()).count(user_value) == 1:
            await callback.message.edit_text(f"лобби успешно созданно с id: {user_value}")
        else:
            user_data[callback.from_user.id] = ''
            await callback.message.edit_text(f"id уже занято придумайте другое")

    await callback.answer()


# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     kb = [
#         [types.KeyboardButton(text="С пюрешкой")],
#         [types.KeyboardButton(text="Без пюрешки")]
#     ]
#     keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
#     await message.answer("Как подавать котлеты?", reply_markup=keyboard)
#
#
#
# @dp.message(F.text == 'Начать игру')
# async def about_bot(message: types.Message):
#
#     """Описывает процесс игры"""
#
#     await message.reply("Привет!", reply_markup=kb.greet_kb)







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