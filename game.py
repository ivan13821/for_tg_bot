
from main import bot, message_from_user
import datetime
game_db = {}
users_l = {}
users_name = {}
from database_config import back_game

class Game():

    @staticmethod
    def create_lobby(message):

        """Создание лобби для игры"""

        game_db['operations'] = {}

        try:
            x = users_l[message.chat.id]
            return 'Вы не можете создать лобби так как вы уже находитесь в игре'
        except:

            try:
                id_lobby = list(game_db.keys())[-1]+1
            except:
                id_lobby = 1

            users_l[message.chat.id] = id_lobby

            game_db[id_lobby] = {'users':{}}

            Game.add_user_on_group(id_lobby, message)
            return id_lobby




    @staticmethod
    def add_user_on_group(id_lobby, message):

        """Добавляет нового участника в уже существующее лобби"""
        try:
            id_lobby = int(id_lobby)
        except:
            return 'id должен состоять из цифр'
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
    def add_operation(message, text=None):

        """сохраняет данные об финансовых операциях"""
        if text == None:
            try:
                game_db['operations'][message.chat.id].append(message.text)
            except:
                game_db['operations'][message.chat.id] = [message.text]

        else:
            try:
                game_db['operations'][message.chat.id].append(text)
            except:
                game_db['operations'][message.chat.id] = [text]






    @staticmethod
    async def message_from_list(message, users_id, but_id=None):

        """Отправка сообщений всем"""

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
            return True

        else:
            return False


    @staticmethod
    def bye(message) -> str:

        """Покупка ресурсов у игрока или биржи"""
        # | действие | пользователь | ресурс | количество | цена


        string = message.text.strip().split()[1::]

        if string[0] != 'биржа':
            Game.add_operation(message.text)


        if string[0] == 'биржа':

            if len(string) != 3:
                return 'При продаже на биржу не нужно указывать цену'

            try:
                cost = back_game['ресурсы'][string[1]]
            except:
                return 'данного ресурса нет в перечне ресурсов, проверьте написание'

            if not string[2].isdigit(): return 'В позицию количества вы ввели не число'

            text = message.text.split()

            text.append(str(cost))

            text = ' '.join(text)

            cost = cost * int(string[2])
            Game.add_operation(message, text=text)

            if game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы']['деньги'] < cost: return 'Недостаточно денег'

            game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы']['деньги'] -= cost

            game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы'][string[1]] += int(string[2])

            return 'Успешно'


        if len(string) != 4:
            return 'Неверное количество составляющих. *Посмотрите шаблон*'



        #found nik
        for i in users_name.items():
            if i [1]['nik'] == string[0]:
                user_id = i[0]
                break
        else:
            return 'Неправильный ник пользователя'

        try:
            cost = int(string[-1])
        except:
            return 'данного ресурса нет в перечне ресурсов, проверьте написание'

        if not string[2].isdigit(): return 'В позицию количества вы ввели не число'
        if not string[3].isdigit(): return 'В позицию цены вы ввели не число'

        cost = cost * int(string[2])

        if game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы']['деньги'] < cost: return 'Недостаточно денег'

        if game_db[users_l[user_id]]['users'][user_id]['ресурсы'][string[1]] < int(string[2]): return 'Недостаточно ресурсов'

        game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы']['деньги'] -= cost
        game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы'][string[1]] += int(string[2])

        game_db[users_l[user_id]]['users'][user_id]['ресурсы']['деньги'] += cost
        game_db[users_l[user_id]]['users'][user_id]['ресурсы'][string[1]] -= int(string[2])

        return 'Успешно'









    @staticmethod
    def sold(message):

        """Продажа ресурсов на биржу"""

        string = message.text.strip().split()[1::]

        if string[0] != 'биржа':
            Game.add_operation(message.text)


        if string[0] == 'биржа':

            if len(string) != 3:
                return 'При продаже на биржу не нужно указывать цену'

            try:
                cost = back_game['ресурсы'][string[1]]
            except:
                return 'данного ресурса нет в перечне биржи, проверьте написание'

            if not string[2].isdigit(): return 'В позицию количества вы ввели не число'
            text = message.text.split()

            text.append(str(cost))

            text = ' '.join(text)

            cost = cost * int(string[2])
            text = ' '.join(message.text.split().append(string[1]))
            Game.add_operation(message, text=text)


            if game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы'][string[1]] < int(string[2]): return 'Недостаточно ед. ресурса'

            game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы']['деньги'] += cost

            game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы'][string[1]] -= int(string[2])

            return 'Успешно'

        if len(string) != 4:
            return 'Неверное количество составляющих. *Посмотрите шаблон*'


        for i in users_name.items():
            if i [1]['nik'] == string[0]:
                user_id = i[0]
                break
        else:
            return 'Неправильный ник пользователя'

        try:
            cost = int(string[-1])
        except:
            return 'данного ресурса нет в перечне ресурсов, проверьте написание'

        if not string[2].isdigit(): return 'В позицию количества вы ввели не число'
        if not string[3].isdigit(): return 'В позицию цены вы ввели не число'

        cost = cost * int(string[2])

        if game_db[users_l[user_id]]['users'][user_id]['ресурсы']['деньги'] < cost: return 'Недостаточно денег'
        if game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы'][string[1]] < int(string[2]): return 'Недостаточно ресурсов'

        game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы']['деньги'] += cost
        game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы'][string[1]] -= int(string[2])

        game_db[users_l[user_id]]['users'][user_id]['ресурсы']['деньги'] -= cost
        game_db[users_l[user_id]]['users'][user_id]['ресурсы'][string[1]] += int(string[2])

        return 'Успешно'



    @staticmethod
    def swap(message):

        """Обмен ресурсами c игроком"""
        #| действие | 2 сторона | ресурс 1 | количество рес 1 | ресурс 2 | количество рес 2 | ресурс 1 идет пользователю отправившему сообщение

        Game.add_operation(message)

        string = message.text.strip().split()[1::]

        for i in users_name.items():
            if i [1]['nik'] == string[0]:
                user_id = i[0]
                break
        else:
            return 'Неправильный ник пользователя'


        if not string[2].isdigit(): return 'В позицию количества вы ввели не число'

        if game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы'][string[1]] < int(string[2]): return 'У вас недостаточно ресурсов'
        if game_db[users_l[user_id]]['users'][user_id]['ресурсы'][string[1]] < int(string[2]): return 'У 2 стороны недостаточно ресурсов'

        game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы'][string[1]] += int(string[2])
        game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы'][string[3]] -= int(string[4])

        game_db[users_l[user_id]]['users'][user_id]['ресурсы'][string[1]] -= int(string[2])
        game_db[users_l[user_id]]['users'][user_id]['ресурсы'][string[1]] += int(string[2])

        return 'Успешно'

    @staticmethod
    async def show_operations(message):
        try:
            text = '\n'.join(game_db['operations'][message.chat.id])
        except:
            text = 'Финансовых операций еще не проводилось'
        await message_from_user(message.chat.id, text)
