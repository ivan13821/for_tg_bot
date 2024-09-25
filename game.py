
from main import bot
import datetime
game_db = {}
users_l = {}
from database_config import back_game

class Game():

    @staticmethod
    def create_lobby(message):

        """Создание лобби для игры"""

        try:
            x = users_l[message.chat.id]
            return 'Вы не можете создать лобби так как вы уже находитесь в игре'
        except:

            try:
                id_lobby = list(game_db.keys())[-1]+1
            except:
                id_lobby = 1

            users_l[message.chat.id] = id_lobby
            now = datetime.datetime.now()

            game_db[id_lobby] = {'users':{}}

            Game.add_user_on_group(id_lobby, message)
            return id_lobby




    @staticmethod
    def add_user_on_group(id_lobby, message):

        """Добавляет нового участника в уже существующее лобби"""

        id_lobby = int(id_lobby)
        if id_lobby in game_db.keys():
            users_l[message.chat.id] = id_lobby
            game_db[id_lobby]['users'][message.chat.id] = {
                'лицевой счет': {
                    'приход': 0,
                    'расход': 0,
                    'остаток': 0
                },

                'ресурсы': {
                    'деньги': 0,
                    'эк_рес': 0,
                    'здание': 0,
                    'оборудование': 0,
                    'технология': 0,
                    'сырье': 0,
                    'рабочие': 0,
                    'транспорт': 0
                }
            }
            return 'Вы успешно добавленны в игру'
        else:
            return 'Вы ввели неправильно id лобби'




    @staticmethod
    async def message_from_list(message, users_id, but_id=None):

        """Отправка сообщений всем"""

        # Получаем список всех пользователей
        for user_id in users_id:
            if user_id == but_id:
                continue
            # Отправляем сообщение каждому пользователю
            await bot.send_message(user_id, message)


    @staticmethod
    def add_start_res(message):

        """Добавляет начальные ресурсы"""

        if message.text == 'А' or message.text == 'Б' or message.text == 'В':

            res = back_game['старт_кап'][message.text]

            for i in res.items():
                game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы'][i[0]] += i[1]
            print(game_db)
            return True

        else:
            return False

    @staticmethod
    def show_res():

        """Показывает пользователю какие ресурсы у него есть в наличии"""

