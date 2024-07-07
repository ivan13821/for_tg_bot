from database import testing_database
from database_config import *

def in_group(message):
    for key in testing_database.keys():
        if testing_database[key]['id'] == message.chat.id:
            return True
    else:
        return False


def admin(message):
    global administrations

    if message.chat.id in administrations:
        return True
    else:
        return False

def add_admin(message):
    global password, administrations
    print(message.text.split()[-1].strip())
    if message.text.split()[-1].strip() == password:
        administrations.append(message.chat.id)
        return 'Ваш пароль принят'
    else:
        return 'Вы ввели неправильный пароль'