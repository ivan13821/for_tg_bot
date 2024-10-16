from economik_game.database_config import credit_db, game_db, users_l
from economik_game.for_group import Group


class credit():



    @staticmethod
    def create(lobby_id):

        """ Создает процентную ставку на 1 год"""

        credit_db[lobby_id] = 0.25


    @staticmethod
    def show_credit_bid(message, id_lobby=None):

        """ Возвращает текущую процентную ставку в данном лобби"""

        if id_lobby is not None:
            bid = int(credit_db[id_lobby] * 100)
        else:
            bid = int(credit_db[users_l[message.chat.id]]*100)

        return f'{bid}%'



    @staticmethod
    def show_user_credit(message) -> str:
        try:
            summa1 = int(game_db[users_l[message.chat.id]]['users'][message.chat.id]['credit']['25%'])
            summa2 =  int(game_db[users_l[message.chat.id]]['users'][message.chat.id]['credit']['50%'])
        except KeyError:
            key = Group.user_in_group(message)
            summa1 = int(game_db[users_l[message.chat.id]]['users'][key]['credit']['25%'])
            summa2 = int(game_db[users_l[message.chat.id]]['users'][key]['credit']['50%'])

        return str(summa1 + summa2)







    @staticmethod
    def choice_credit_bid(lobby_id):

        """ когда заканчивается первый год ставка кредита увеличивается с 25% до 50%"""

        if credit_db[lobby_id] == 0.25:
            credit_db[lobby_id] = 0.50




    @staticmethod
    def add_credit(message, number = None):

        """ Добавляет пользователю новый кредит """

        bid = credit.show_credit_bid(message)

        id_lobby = users_l[message.chat.id]


        if number is not None:

            summa = int(number)

            if bid == '25%':
                game_db[id_lobby]['users'][message.chat.id]['credit']['25%'] += summa

            else:
                game_db[id_lobby]['users'][message.chat.id]['credit']['50%'] += summa


            return 'кредит добавлен'


        try:
            summa = int(message.text)
        except:
            return 'Вы ввели не число'

        if bid == '25%':

            if name_group := Group.user_in_group(message):

                game_db[id_lobby]['users'][name_group]['credit']['25%'] += summa
                game_db[id_lobby]['users'][name_group]['ресурсы']['деньги'] += summa

            else:
                game_db[id_lobby]['users'][message.chat.id]['credit']['25%'] += summa
                game_db[id_lobby]['users'][message.chat.id]['ресурсы']['деньги'] += summa

        else:

            if name_group := Group.user_in_group(message):

                game_db[id_lobby]['users'][name_group]['credit']['50%'] += summa
                game_db[id_lobby]['users'][name_group]['ресурсы']['деньги'] += summa

                return 'Кредит добавлен'


            else:
                game_db[id_lobby]['users'][message.chat.id]['credit']['50%'] += summa
                game_db[id_lobby]['users'][message.chat.id]['ресурсы']['деньги'] += summa



        return 'Кредит добавлен'

    @staticmethod
    def pay_credit(message):

        """ Пользователь платит за взятый кредит сначала за кредит под 50% после за кредит под 25% """

        try:

            try:
                pay = int(message.text)
            except:
                return 'Вы ввели не число'

            if game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы']['деньги'] < pay:
                return 'Вам не хватает денег'

            if pay > game_db[users_l[message.chat.id]]['users'][message.chat.id]['credit']['50%']:

                pay -= game_db[users_l[message.chat.id]]['users'][message.chat.id]['credit']['50%']
                game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы']['деньги'] -= game_db[users_l[message.chat.id]]['users'][message.chat.id]['credit']['50%']
                game_db[users_l[message.chat.id]]['users'][message.chat.id]['credit']['50%'] = 0

            else:
                game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы']['деньги'] -= pay
                game_db[users_l[message.chat.id]]['users'][message.chat.id]['credit']['50%'] -= pay
                return 'Успешно'



            if pay > game_db[users_l[message.chat.id]]['users'][message.chat.id]['credit']['25%']:
                game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы']['деньги'] -= game_db[users_l[message.chat.id]]['users'][message.chat.id]['credit']['25%']
                game_db[users_l[message.chat.id]]['users'][message.chat.id]['credit']['50%'] = 0
                return 'Деньги которые вы переплатили мы вам вернули'

            else:
                game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы']['деньги'] -= pay
                game_db[users_l[message.chat.id]]['users'][message.chat.id]['credit']['25%'] -= pay
                return 'Успешно'

        except KeyError:

            try:
                pay = int(message.text)
            except:
                return 'Вы ввели не число'

            key = Group.user_in_group(message)

            if game_db[users_l[message.chat.id]]['users'][key]['ресурсы']['деньги'] < pay:
                return 'Вам не хватает денег'

            if pay > game_db[users_l[message.chat.id]]['users'][key]['credit']['50%']:

                pay -= game_db[users_l[message.chat.id]]['users'][key]['credit']['50%']
                game_db[users_l[message.chat.id]]['users'][key]['ресурсы']['деньги'] -= \
                game_db[users_l[message.chat.id]]['users'][key]['credit']['50%']
                game_db[users_l[message.chat.id]]['users'][key]['credit']['50%'] = 0

            else:
                game_db[users_l[message.chat.id]]['users'][key]['ресурсы']['деньги'] -= pay
                game_db[users_l[message.chat.id]]['users'][key]['credit']['50%'] -= pay
                return 'Успешно'

            if pay > game_db[users_l[message.chat.id]]['users'][key]['credit']['25%']:
                game_db[users_l[message.chat.id]]['users'][key]['ресурсы']['деньги'] -= \
                game_db[users_l[message.chat.id]]['users'][key]['credit']['25%']
                game_db[users_l[message.chat.id]]['users'][key]['credit']['50%'] = 0
                return 'Деньги которые вы переплатили мы вам вернули'

            else:
                game_db[users_l[message.chat.id]]['users'][key]['ресурсы']['деньги'] -= pay
                game_db[users_l[message.chat.id]]['users'][key]['credit']['25%'] -= pay
                return 'Успешно'


    @staticmethod
    def new_year(message):

        """ Добавляет всем участникам игры проценты по взятым кредитам """

        for i in game_db[users_l[message.chat.id]]['users'].keys():

            game_db[users_l[message.chat.id]]['users'][i]['credit']['25%'] = round(game_db[users_l[message.chat.id]]['users'][i]['credit']['25%']*1.25, 3)
            game_db[users_l[message.chat.id]]['users'][i]['credit']['50%'] = round(game_db[users_l[message.chat.id]]['users'][i]['credit']['50%']*1.5, 3)

