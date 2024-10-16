from config import API_TOKEN
from aiogram import Bot

from economik_game.credit_func import credit
from economik_game.database_config import *
from economik_game.for_group import Group
from economik_game.keyboard import MyKeyboard

bot = Bot(token=API_TOKEN)

class EconomicGame():

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

            game_db[id_lobby] = {'users':{}}

            credit.create(users_l[message.chat.id])

            EconomicGame.add_user_on_lobby(id_lobby, message)

            game_db[id_lobby]['operations'] = {}

            users_name[id_lobby] = {}

            return id_lobby



    @staticmethod
    def all_clear(id_lobby):

        """Удаляет все данные связанные с лобби"""

        #удаление groups
        try:
            del groups[id_lobby]
        except KeyError:
            pass


        #удаление admins
        try:
            del admins[id_lobby]
        except KeyError:
            pass


        #удаление credit_db
        del credit_db[id_lobby]




        #удаление users_name
        try:
            del users_name[id_lobby]
        except KeyError:
            pass



        #удаление game_db
        del game_db[id_lobby]



        #удаление users_l
        for i in list(users_l.items()):

            if i[1] == id_lobby:
                del users_l[i[0]]

    @staticmethod
    async def clear_user(chat_id, state):

        """ Функция для очистки баз данных от определенного пользователя"""


        id_lobby = users_l[chat_id]

        # удаление из groups
        # if not groups:
        #     for i in groups[id_lobby].items():
        #         if chat_id in i[1]:
        #             groups[id_lobby][i[0]].remove(chat_id)
        #             if not groups[id_lobby][i[0]]:
        #                 del groups


        # удаление из admins
        if not admins:
            try:
                if chat_id in admins[id_lobby]:
                    admins[id_lobby].remove(chat_id)

                    if not admins[id_lobby]:
                        del admins[id_lobby]
            except KeyError:
                pass


        # удаление из users_name
        try:
            del users_name[id_lobby][chat_id]

        except KeyError:
            pass

        finally:
            # Если лобби пустое удаляем его
            try:
                if not users_name[id_lobby]:
                    del users_name[id_lobby]
            except KeyError:
                pass


        # удаление из game_db
        try:
            del game_db[id_lobby]['users'][chat_id]

        except KeyError:
            pass

        finally:
            # Если лобби пустое удаляем его
            try:
                if not game_db[id_lobby]['users']:
                    del game_db[id_lobby]
            except KeyError:
                pass


        # удаление из users_l
        try:
            del users_l[chat_id]
        except KeyError:
            pass

        await state.clear()
        await bot.send_message(chat_id=chat_id, text='Вы вышли из игры', reply_markup=MyKeyboard.menu())




    @staticmethod
    def cost_all_res(chat_id, id_lobby):

        """Возвращает стоимость всех ресурсов в наличии у игрока"""


        result = 0


        for i in game_db[id_lobby]['users'][chat_id]['ресурсы'].items():

            if i[0] == 'деньги':
                result += int(i[1])
            else:
                result += int(back_game['ресурсы'][i[0]])*int(i[1])

        return result









    @staticmethod
    async def show_winner(id_lobby, message=None):

        """Отправляет всем сообщение о конце игры а также о ее победителе"""

        maxi = 0
        name_winner = ''

        for i in game_db[id_lobby]['users'].keys():

            res = EconomicGame.cost_all_res(i, id_lobby)

            if res > maxi:
                name_winner = users_name[id_lobby][i]['nik']
                maxi = res

        name_winner = f'Игра законченна победитель: {name_winner} результат {maxi}'

        await EconomicGame.message_from_list(name_winner, admins[id_lobby], main_message=message)
        await EconomicGame.message_from_list(name_winner, game_db[id_lobby]['users'].keys(), main_message=message)












    @staticmethod
    async def message_from_user(user_id, message):

        """Отправка сообщения пользователю по id"""

        await bot.send_message(user_id, message)











    @staticmethod
    def add_user_on_lobby(id_lobby, message):

        """Добавляет нового участника в уже существующее лобби"""
        try:
            id_lobby = int(id_lobby)
        except:
            return 'id должен состоять из цифр'

        if id_lobby not in game_db.keys():
            return 'Такого id не существует'


        # Проверка не был ли закончен 1 год, если да то пользователь не может зайти
        if credit.show_credit_bid(message, id_lobby=id_lobby) == '50%':
            users_l[message.chat.id] = id_lobby

            return 'Вы не можете зайти в игру, т.к в игре прошло уже больше года игрового времени'


        if id_lobby in game_db.keys():
            users_l[message.chat.id] = id_lobby
            game_db[id_lobby]['users'][message.chat.id] = {
                'ресурсы': {
                    'деньги': 0,
                    'здание': 0,
                    'оборудование': 0,
                    'технология': 0,
                    'сырье': 0,
                    'рабочие': 0,
                    'транспорт': 0
                },
                'credit':{
                    '25%':0,
                    '50%':0
                },
                'ready':False
            }


            return 'Вы успешно добавленны в игру'
        else:
            return 'Вы ввели неправильно id лобби'

















    @staticmethod
    def add_operation(message, nik_user_2=None, text=None):

        """сохраняет данные об финансовых операциях"""

        id_user_2 = None

        id_lobby = users_l[message.chat.id]



        if Group.user_in_group(message):
            user_id = Group.user_in_group(message)
            user_chat_id = message.chat.id
        else:
            user_id = message.chat.id
            user_chat_id = user_id



        if nik_user_2 is not None:
            for i in users_name[users_l[user_id]].items():
                if i[1]['nik'] == nik_user_2:
                    id_user_2 = i[0]
                    break


        #Добавляем операцию для 2го пользователя если он есть
        if not(id_user_2 == None):
            if text == None:
                try:
                    game_db[id_lobby]['operations'][id_user_2].append(f'{users_name[id_lobby][user_id]['nik']}: {message.text}')
                except:
                    game_db[id_lobby]['operations'][id_user_2] = [f'{users_name[id_lobby][user_id]['nik']}: {message.text}']

            else:
                try:
                    game_db[id_lobby]['operations'][id_user_2].append(f'{users_name[id_lobby][user_id]['nik']}: {text}')
                except:
                    game_db[id_lobby]['operations'][id_user_2] = [f'{users_name[id_lobby][user_id]['nik']}: {text}']



        #Добавляем операцию для пользователя, который отправил сообщение
        if text == None:
            try:
                game_db[id_lobby]['operations'][user_id].append(f'{users_name[id_lobby][user_id]['nik']}: {message.text}')
            except:
                game_db[id_lobby]['operations'][user_id] = [f'{users_name[id_lobby][user_id]['nik']}: {message.text}']

        else:
            try:
                game_db[id_lobby]['operations'][user_id].append(f'{users_name[id_lobby][user_id]['nik']}: {text}')
            except:
                game_db[id_lobby]['operations'][user_id] = [f'{users_name[id_lobby][user_id]['nik']}: {text}']












    @staticmethod
    async def message_from_list(message, users_id, but_id=None, main_message=None, reply_markup=None):

        """Отправка сообщений всем"""

        for user_id in users_id:

            if type(user_id) != type('str'):

                if user_id == but_id:
                    continue
                # Отправляем сообщение каждому пользователю
                if reply_markup is not None:
                    await bot.send_message(user_id, message, reply_markup=reply_markup)
                else:
                    await bot.send_message(user_id, message)

            else:

                for new_id in groups[users_l[main_message.chat.id]][user_id]:

                    if new_id == but_id:
                        continue

                    if reply_markup is not None:
                        await bot.send_message(user_id, message, reply_markup=reply_markup)
                    else:
                        await bot.send_message(new_id, message)






    @staticmethod
    def add_admin(message):

        """Добавляет админа в игру"""

        #удаление из базы данных игры
        try:
            del game_db[users_l[message.chat.id]]['users'][message.chat.id]
        except KeyError:
            pass


        #Добавление в базу админов
        try:
            admins[users_l[message.chat.id]].append(message.chat.id)
        except:
            admins[users_l[message.chat.id]] = [message.chat.id]

        return 'Вы добавлены в игру как администратор'






    @staticmethod
    def add_start_res(message):

        """Добавляет начальные ресурсы"""

        if message.text == 'А' or message.text == 'Б' or message.text == 'В':

            res = back_game['старт_кап'][message.text]

            for i in res.items():
                game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы'][i[0]] += i[1]
                if i[0] == 'деньги':
                    credit.add_credit(message, number=int(i[1]))

            return True

        else:
            return False














    @staticmethod
    def bye(message) -> str:

        """Покупка ресурсов у игрока или биржи"""
        # | действие | пользователь | ресурс | количество | цена


        string = message.text.lower().strip().split()[1::]

        if Group.user_in_group(message):
            user_id = Group.user_in_group(message)
        else:
            user_id = message.chat.id


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

            text += f'на сумму {cost}'

            if game_db[users_l[message.chat.id]]['users'][user_id]['ресурсы']['деньги'] < cost: return 'Недостаточно денег'

            game_db[users_l[message.chat.id]]['users'][user_id]['ресурсы']['деньги'] -= cost

            game_db[users_l[message.chat.id]]['users'][user_id]['ресурсы'][string[1]] += int(string[2])

            EconomicGame.add_operation(message, text=text)

            return 'Успешно'


        if len(string) != 4:
            return 'Неверное количество составляющих. *Посмотрите шаблон*'



        #found nik
        for i in users_name[users_l[user_id]].items():
            if i [1]['nik'] == string[0]:
                another_user_id = i[0]
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

        if game_db[users_l[message.chat.id]]['users'][user_id]['ресурсы']['деньги'] < cost: return 'Недостаточно денег'

        if game_db[users_l[message.chat.id]]['users'][another_user_id]['ресурсы'][string[1]] < int(string[2]): return 'Недостаточно ресурсов'

        game_db[users_l[message.chat.id]]['users'][user_id]['ресурсы']['деньги'] -= cost
        game_db[users_l[message.chat.id]]['users'][user_id]['ресурсы'][string[1]] += int(string[2])

        game_db[users_l[message.chat.id]]['users'][another_user_id]['ресурсы']['деньги'] += cost
        game_db[users_l[message.chat.id]]['users'][another_user_id]['ресурсы'][string[1]] -= int(string[2])

        if string[0] != 'биржа':
            EconomicGame.add_operation(message, nik_user_2=string[0])

        return 'Успешно'





















    @staticmethod
    def sold(message):

        """Продажа ресурсов на биржу или другому игроку"""

        string = message.text.lower().strip().split()[1::]

        if Group.user_in_group(message):
            user_id = Group.user_in_group(message)
        else:
            user_id = message.chat.id


        if string[0] == 'биржа':

            if len(string) != 3:
                return 'При продаже на биржу не нужно указывать цену'

            try:
                cost = back_game['ресурсы'][string[1]]
            except:
                return 'данного ресурса нет в перечне биржи, проверьте написание'

            if not string[2].isdigit(): return 'В позицию количества вы ввели не число'

            text = message.text.split()



            cost = cost * int(string[2])

            text.pop(-1)

            text.append(str(cost))

            text = f'{text[0]} {text[1]} {text[2]} на сумму {text[3]}'


            if game_db[users_l[message.chat.id]]['users'][user_id]['ресурсы'][string[1]] < int(string[2]): return 'Недостаточно ед. ресурса'

            game_db[users_l[message.chat.id]]['users'][user_id]['ресурсы']['деньги'] += cost

            game_db[users_l[message.chat.id]]['users'][user_id]['ресурсы'][string[1]] -= int(string[2])

            EconomicGame.add_operation(message, text=text)

            return 'Успешно'

        if len(string) != 4:
            return 'Неверное количество составляющих. *Посмотрите шаблон*'


        for i in users_name[users_l[user_id]].items():
            if i [1]['nik'] == string[0]:
                another_user_id = i[0]
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

        if game_db[users_l[message.chat.id]]['users'][another_user_id]['ресурсы']['деньги'] < cost: return 'Недостаточно денег'
        if game_db[users_l[message.chat.id]]['users'][user_id]['ресурсы'][string[1]] < int(string[2]): return 'Недостаточно ресурсов'

        game_db[users_l[message.chat.id]]['users'][user_id]['ресурсы']['деньги'] += cost
        game_db[users_l[message.chat.id]]['users'][user_id]['ресурсы'][string[1]] -= int(string[2])

        game_db[users_l[message.chat.id]]['users'][another_user_id]['ресурсы']['деньги'] -= cost
        game_db[users_l[message.chat.id]]['users'][another_user_id]['ресурсы'][string[1]] += int(string[2])

        if string[0] != 'биржа':
            EconomicGame.add_operation(message.text, nik_user_2=string[0])




















    @staticmethod
    def swap(message):

        """Обмен ресурсами c игроком"""
        #| действие | 2 сторона | ресурс 1 | количество рес 1 | ресурс 2 | количество рес 2 | ресурс 1 идет пользователю отправившему сообщение


        if Group.user_in_group(message):
            user_id = Group.user_in_group(message)
        else:
            user_id = message.chat.id

        string = message.text.lower().strip().split()[1::]

        for i in users_name[users_l[user_id]].items():
            if i [1]['nik'] == string[0]:
                another_user_id = i[0]
                break
        else:
            return 'Неправильный ник пользователя'


        if not string[2].isdigit(): return 'В позицию количества вы ввели не число'

        if game_db[users_l[message.chat.id]]['users'][user_id]['ресурсы'][string[1]] < int(string[2]): return 'У вас недостаточно ресурсов'
        if game_db[users_l[user_id]]['users'][another_user_id]['ресурсы'][string[1]] < int(string[2]): return 'У 2 стороны недостаточно ресурсов'

        game_db[users_l[message.chat.id]]['users'][user_id]['ресурсы'][string[1]] += int(string[2])
        game_db[users_l[message.chat.id]]['users'][user_id]['ресурсы'][string[3]] -= int(string[4])

        game_db[users_l[user_id]]['users'][another_user_id]['ресурсы'][string[1]] -= int(string[2])
        game_db[users_l[user_id]]['users'][another_user_id]['ресурсы'][string[1]] += int(string[2])

        EconomicGame.add_operation(message, nik_user_2=string[0])

        return 'Успешно'












    @staticmethod
    async def show_operations(message):

        """Показывает какие фин. операции совершал пользователь"""


        if Group.user_in_group(message):
            user_id = Group.user_in_group(message)
        else:
            user_id = message.chat.id


        try:
            text = '\n'.join(game_db[users_l[message.chat.id]]['operations'][user_id])
        except:
            text = 'Финансовых операций еще не проводилось'
        await EconomicGame.message_from_user(message.chat.id, text)




    @staticmethod
    def admin_res(message):

        try:

            for i in game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы'].keys():
                game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы'][i] += 100000

        except KeyError:

            key = Group.user_in_group(message)

            for i in game_db[users_l[message.chat.id]]['users'][key]['ресурсы'].keys():
                game_db[users_l[message.chat.id]]['users'][key]['ресурсы'][i] += 100000











    @staticmethod
    def sold_on_rialto(message):

        """Продажа ресурсов на биржу на повышение производства"""

        try:

            try:
                tip = back_game['тех_карта'][message.text]
            except:
                return 'Данного типа производства несуществует, пожалуйста выберете из данных вариантов'


            if game_db[users_l[message.chat.id]]['users'][message.chat.id]['ready'] == True:
                return 'Вы не можете совершать операции на бирже пока не закончится год (год заканчивается когда все игроки продали ресурсы на повышение производства'


            result = []
            for i in back_game['тех_карта'][message.text]['эк_рес'].keys():


                if game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы'][i] < back_game['тех_карта'][message.text]['эк_рес'][i]:
                    result.append(i)

            if result == []:
                for i in back_game['тех_карта'][message.text]['эк_рес'].keys():
                    game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы'][i] -= back_game['тех_карта'][message.text]['эк_рес'][i]

            else:
                text = 'Нехватает ресурсов: '
                text += ', '.join(result)
                return text



            game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы']['деньги'] += back_game['тех_карта'][message.text]['выручка']
            game_db[users_l[message.chat.id]]['users'][message.chat.id]['ready'] = True


            for i in game_db[users_l[message.chat.id]]['users'].keys():
                if not game_db[users_l[message.chat.id]]['users'][i]['ready']:
                    break
            else:
                return 'Успешно'


            return 'Успешно'






        except KeyError: # Если пользователь == объединение

            key = Group.user_in_group(message)

            try:
                tip = back_game['тех_карта'][message.text]
            except:
                return 'Данного типа производства несуществует, пожалуйста выберете из данных вариантов'

            if game_db[users_l[message.chat.id]]['users'][key]['ready'] == True:
                return 'Вы не можете совершать операции на бирже пока не закончится год (год заканчивается когда все игроки продали ресурсы на повышение производства'

            result = []
            for i in back_game['тех_карта'][message.text]['эк_рес'].keys():

                if game_db[users_l[message.chat.id]]['users'][key]['ресурсы'][i] < \
                        back_game['тех_карта'][message.text]['эк_рес'][i]:
                    result.append(i)

            if result == []:
                for i in back_game['тех_карта'][message.text]['эк_рес'].keys():
                    game_db[users_l[message.chat.id]]['users'][key]['ресурсы'][i] -= \
                    back_game['тех_карта'][message.text]['эк_рес'][i]

            else:
                text = 'Нехватает ресурсов: '
                text += ', '.join(result)
                return text

            game_db[users_l[message.chat.id]]['users'][key]['ресурсы']['деньги'] += \
            back_game['тех_карта'][message.text]['выручка']
            game_db[users_l[message.chat.id]]['users'][key]['ready'] = True

            for i in game_db[users_l[message.chat.id]]['users'].keys():
                if not game_db[users_l[message.chat.id]]['users'][i]['ready']:
                    break
            else:
                return 'Успешно'

            return 'Успешно'











    @staticmethod
    def new_year(id_lobby):

        """ Позволяет пользователю вновь торговать своими ресурсами """

        for i in game_db[id_lobby]['users'].keys():
            game_db[id_lobby]['users'][i]['ready'] = False
