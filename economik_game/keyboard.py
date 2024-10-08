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
    def credit():
        kb = [
            [types.KeyboardButton(text="Взять кредит"), types.KeyboardButton(text="Заплатить по кредиту")],
            [types.KeyboardButton(text="Посмотреть задолжность"), types.KeyboardButton(text="Назад"), types.KeyboardButton(text="Посмотреть ставку")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        return keyboard

    @staticmethod
    def reference():
        kb = [
            [
                types.KeyboardButton(text="Биржа"), types.KeyboardButton(text="Тех. карта")
            ],
            [
                types.KeyboardButton(text="Шаблоны"), types.KeyboardButton(text="Назад")
            ]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        return keyboard

    @staticmethod
    def product_option():
        kb = [
            [
                types.KeyboardButton(text="0%"), types.KeyboardButton(text="10%")
            ],
            [
                types.KeyboardButton(text="25%"), types.KeyboardButton(text="50%")
            ],
            [
                types.KeyboardButton(text="100%")
            ],
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
            [
                types.KeyboardButton(text="Выйти в меню"),
                types.KeyboardButton(text="Мои ресурсы")
            ],
            [
                types.KeyboardButton(text="Список игроков"),
                types.KeyboardButton(text='Повысить уровень производства')
            ],
            [
                types.KeyboardButton(text="Cправка"),
                types.KeyboardButton(text="Кредит"),
                types.KeyboardButton(text="История")
            ]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        return keyboard