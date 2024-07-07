from aiogram import types
from database_config import *





def post_db(message) -> list:


    my_key = ''

    for key in testing_database.keys():
        if testing_database[key]['id'] == message.chat.id:
            my_key = key

    lesson, data, homework = list(map(lambda x: x.strip(), message.text.lower().split(';')))

    if lesson in testing_database[my_key].keys():
        if data in testing_database[my_key][lesson].keys():
            return ['Задание на этот день уже есть']
        else:
            testing_database[my_key][lesson][data] = homework
            return [f'Задание по предмету {lesson} успешно добавленно на {data}\U0001f44d']

    else:
        testing_database[my_key][lesson] = {data: homework}
        return [f'Предмет {lesson} добавлен, задание для предмета {lesson} на {data} добавленно\U0001f44d']


def get_db(message: types.Message) -> list:

    my_key = ''
    old_message = message

    for key in testing_database.keys():
        if testing_database[key]['id'] == message.chat.id:
            my_key = key

    message = list(map(lambda x: x.strip(), message.text.lower().split(';')))


    if len(message) == 1:
        result = []
        lesson = message[0]

        if not lesson in testing_database[my_key].keys():
            return [f'Такого предмета еще не добавленно, добавьте первое задание на него']

        val = testing_database[my_key][lesson].values()
        keys = testing_database[my_key][lesson].keys()

        for v, k in zip(val, keys):
            result.append(f'Задание на {k}\U0001f468\u200D\U0001f393\n{v}')

        return result


    elif len(old_message.text.split(';')) == 2:
        lesson, data = message
        if not lesson in testing_database[my_key].keys():
            return [f'Такого предмета еще не добавленно, добавьте первое задание на него']

        if not data in testing_database[my_key][lesson].keys():
            return [f'Задания на этот день еще не добавили']

        return [testing_database[my_key][lesson][data]+'\U0001f913']


    else:
        return [f'Неправильно набранно сообщение. Для получения информации по правильному введению данных введите /start']