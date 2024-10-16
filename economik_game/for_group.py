from economik_game.database_config import game_db, users_l, groups, users_name



class Group():




    @staticmethod
    def create_group(message):

        """ Создает группу для слияния пользователей в большую компанию """

        if gr := Group.user_in_group(message):
            return f'Вы уже состоите в группе {gr}'

        id_lobby = users_l[message.chat.id]

        name = message.text #Пользователь должен ввести название группы

        try:
            let = game_db[id_lobby]['users'][name]
            return 'Группа с таким названием уже существует'
        except:
            pass

        groups[id_lobby] = {}
        groups[id_lobby][name] = [message.chat.id]

        users_name[users_l[message.chat.id]][message.text] = {'nik':message.text, 'username':'Группа'}




        game_db[id_lobby]['users'][name] = {
            'ресурсы': {
                'деньги': 0,
                'здание': 0,
                'оборудование': 0,
                'технология': 0,
                'сырье': 0,
                'рабочие': 0,
                'транспорт': 0
            },
            'credit': {
                '25%': 0,
                '50%': 0
            },
            'ready': False
        }




        for i in game_db[id_lobby]['users'][name]['ресурсы'].keys(): #Добавляем значения пользователя в ресурсы
            game_db[id_lobby]['users'][name]['ресурсы'][i] = game_db[id_lobby]['users'][message.chat.id]['ресурсы'][i]



        for i in game_db[id_lobby]['users'][name]['credit'].keys():  # Добавляем значения пользователя в кредиты
            game_db[id_lobby]['users'][name]['credit'][i] = game_db[id_lobby]['users'][message.chat.id]['credit'][i]


        del game_db[id_lobby]['users'][message.chat.id]


        return 'Успешно'











    @staticmethod
    def add_user_on_group(message):

        """ Осушествляет выход пользователя из группы"""

        id_lobby = users_l[message.chat.id]

        name = message.text

        try:
            let = groups[id_lobby][name]
        except:
            return 'Группы с таким названием не существует'


        if name_group := Group.user_in_group(message):
            return f'Вы уже состоите в группе {name_group}'

        groups[id_lobby][name].append(message.chat.id)


        for i in game_db[id_lobby]['users'][message.chat.id]['ресурсы'].keys():
            game_db[id_lobby]['users'][name]['ресурсы'][i] += game_db[id_lobby]['users'][message.chat.id]['ресурсы'][i]

        for i in game_db[id_lobby]['users'][message.chat.id]['credit'].keys():
            game_db[id_lobby]['users'][name]['credit'][i] += game_db[id_lobby]['users'][message.chat.id]['credit'][i]

        del game_db[id_lobby]['users'][message.chat.id]

        return 'Успешно'









    @staticmethod
    def leave_on_group(message):

        """ Пользователь выходит из объединения """

        if not (name_group := Group.user_in_group(message)):
            return 'Вы не состоите не в одном из объединений'

        from economik_game.economik_game import EconomicGame
        EconomicGame.add_user_on_lobby(users_l[message.chat.id], message)

        for i in game_db[users_l[message.chat.id]]['users'][name_group][
            'ресурсы'].keys():  # Удалет часть ресурсов из группы (пропорционально кол-ву игроков) и добавляет их пользователю

            game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы'][i] = \
            game_db[users_l[message.chat.id]]['users'][name_group]['ресурсы'][i] // len(
                groups[users_l[message.chat.id]][name_group])

            game_db[users_l[message.chat.id]]['users'][name_group]['ресурсы'][i] -= \
            game_db[users_l[message.chat.id]]['users'][name_group]['ресурсы'][i] // len(
                groups[users_l[message.chat.id]][name_group])

        for i in game_db[users_l[message.chat.id]]['users'][name_group][
            'credit'].keys():  # Удалет часть ресурсов из группы (пропорционально кол-ву игроков) и добавляет их пользователю

            game_db[users_l[message.chat.id]]['users'][message.chat.id]['credit'][i] = \
            game_db[users_l[message.chat.id]]['users'][name_group]['credit'][i] // len(
                groups[users_l[message.chat.id]][name_group])

            game_db[users_l[message.chat.id]]['users'][name_group]['credit'][i] -= \
            game_db[users_l[message.chat.id]]['users'][name_group]['credit'][i] // len(
                groups[users_l[message.chat.id]][name_group])

        print(groups[users_l[message.chat.id]][name_group])
        print(groups)

        groups[users_l[message.chat.id]][name_group].remove(message.chat.id)

        if not groups[users_l[message.chat.id]][name_group]:

            del game_db[users_l[message.chat.id]]['users'][name_group]
            del groups[users_l[message.chat.id]][name_group]


        return 'Успешно'

    @staticmethod
    def user_in_group(message=None, chat_id=None):

        """ Показывает состоит ли пользователь в каком либо объединении """



        if message is not None:
            id_user = message.chat.id

            try:

                for i in groups[users_l[id_user]].keys():
                    if id_user in groups[users_l[id_user]][i]:
                        return i

            except KeyError:
                return False

            return False

        if chat_id is not None:
            id_user = chat_id

            try:

                for i in groups[users_l[id_user]].keys():
                    if id_user in groups[users_l[id_user]][i]:
                        return i

            except:
                return False

            return False

        return None







    @staticmethod
    def show_users_in_group(message):

        """ Показывает пользователей зарегистрированных в той же группе"""

        name = Group.user_in_group(message)
        if not name:
            return 'Вы не состоите в группе'

        result = ''
        for i in groups[users_l[message.chat.id]][name]:

            result += f'{users_name[users_l[message.chat.id]][i]['username']}: {users_name[users_l[message.chat.id]][i]['nik']}\n'


        return result








