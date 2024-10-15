from economik_game.database_config import game_db, users_l, users_name
from economik_game.for_group import Group


class Years(): #True значит что пользователь уже повышал уровень производства, False значит что еще не повышал

    @staticmethod
    def change_year(chat_id, message=None):

        """ Меняет флаг с True на False и обратно"""



        if message is not None:
            group_id = chat_id
            chat_id = message.chat.id
        else:
            group_id = chat_id


        if game_db[users_l[chat_id]]['users'][group_id]['ready']:
            game_db[users_l[chat_id]]['users'][group_id]['ready'] = False

        else:
            game_db[users_l[chat_id]]['users'][group_id]['ready'] = True



    @staticmethod
    def show_year(message) -> bool:

        """ Возвращает текущение значение флажка (Повышал ли пользователь в этом году уровень производства или нет)"""

        return game_db[users_l[message.chat.id]]['users'][message.chat.id]['ready']


    @staticmethod
    def new_year(message):

        """ Проверяет может ли начаться новый год если да то начинает его """



        for i in game_db[users_l[message.chat.id]]['users'].keys():

            try:

                if not game_db[users_l[i]]['users'][i]['ready']:
                    return False

            except KeyError:
                key = Group.user_in_group(message)

                if not game_db[users_l[message.chat.id]]['users'][key]['ready']:
                    return False

        for i in game_db[users_l[message.chat.id]]['users'].keys():

            Years.change_year(i, message)

        return 'new year'



