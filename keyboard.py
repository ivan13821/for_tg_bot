from aiogram import Bot, Dispatcher, types


class MyKeyboard():

    @staticmethod
    def join_create():
        kb = [
            [types.KeyboardButton(text="Начать новую игру"), types.KeyboardButton(text="Присоединиться")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        return keyboard

    @staticmethod
    def A_B_C():
        kb = [
            [types.KeyboardButton(text="А"),
             types.KeyboardButton(text="Б"),
             types.KeyboardButton(text="В"), ],
            [types.KeyboardButton(text="Выйти в меню")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        return keyboard

    @staticmethod
    def back_on_menu():
        kb = [
            [types.KeyboardButton(text="Выйти в меню")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        return keyboard

    @staticmethod
    def menu():
        kb = [
            [types.KeyboardButton(text="меню")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        return keyboard

    @staticmethod
    def menu_in_game():
        kb = [
            [types.KeyboardButton(text="Выйти в меню"),
             types.KeyboardButton(text="Мои ресурсы"),
             types.KeyboardButton(text="История"),],
            [types.KeyboardButton(text="Список игроков"),
             types.KeyboardButton(text="Биржа"),
             types.KeyboardButton(text="Шаблоны")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        return keyboard
