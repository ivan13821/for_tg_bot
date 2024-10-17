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
    def yes_or_no():
        kb = [
            [types.KeyboardButton(text="Да"), types.KeyboardButton(text="Нет")]
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
                types.KeyboardButton(text="Цены на бирже"), types.KeyboardButton(text="Ресурсы для повышения производства")
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
                types.KeyboardButton(text="100%"), types.KeyboardButton(text="Назад")
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
            [types.KeyboardButton(text="Выйти в меню"), types.KeyboardButton(text="admin")]
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
    def groups():
        kb = [
            [types.KeyboardButton(text="Создать группу"), types.KeyboardButton(text="Присоединиться к группе")],
            [types.KeyboardButton(text="Покинуть группу"), types.KeyboardButton(text="Игроки в группе"), types.KeyboardButton(text="Назад")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        return keyboard



    @staticmethod
    def game_for_admin():
        kb = [
            [
                types.KeyboardButton(text="Выйти в меню"),
                types.KeyboardButton(text="Ресурсы игрока")
            ],
            [
                types.KeyboardButton(text="Список игроков"),
                types.KeyboardButton(text="Cправка")
            ],
            [
                types.KeyboardButton(text="Закончить игру"),
            ]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        return keyboard








    @staticmethod
    def menu_in_game():
        kb = [
            [
                types.KeyboardButton(text="Выйти в меню"),
                types.KeyboardButton(text="Мои ресурсы"),
                types.KeyboardButton(text="Объединения")
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