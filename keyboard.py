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
             types.KeyboardButton(text="В"), ]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        return keyboard

    @staticmethod
    def back_del_op():
        kb = [
            [types.KeyboardButton(text="Завершить все операции связанные с игрой"),
             types.KeyboardButton(text="Выйти в меню")]
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