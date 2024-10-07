from economik_game.database_config import game_db, users_l, users_name



class Years(): #True значит что пользователь уже повышал уровень производства, False значит что еще не повышал

    @staticmethod
    def change_year(chat_id):

        """ Меняет флаг с True на False и обратно"""

        if game_db[users_l[chat_id]]['users'][chat_id]['ready']:
            game_db[users_l[chat_id]]['users'][chat_id]['ready'] = False

        else:
            game_db[users_l[chat_id]]['users'][chat_id]['ready'] = True


    @staticmethod
    def show_year(message) -> bool:

        """ Возвращает текущение значение флажка (Повышал ли пользователь в этом году уровень производства или нет)"""

        return game_db[users_l[message.chat.id]]['users'][message.chat.id]['ready']


    @staticmethod
    def new_year(message):

        """ Проверяет может ли начаться новый год если да то начинает его """

        for i in game_db[users_l[message.chat.id]]['users'].keys():

            if not game_db[users_l[i]]['users'][i]['ready']:
                return False

        for i in game_db[users_l[message.chat.id]]['users'].keys():

            Years.change_year(i)

        return 'new year'



