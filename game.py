


game_db = {}

def create_lobby(message):

    """Создание лобби для игры"""


    if found_user_on_lobbyes(message) == 0:
        try:
            id_lobby = list(game_db.keys())[-1]+1
        except:
            id_lobby = 1

        game_db[id_lobby] = {'users':
                                 {
                                     message.chat.id:{

                                     }
                                 }
        }
    else:
        id_lobby = 'Вы не можете создать лобби так как вы уже находитесь в игре'
    #print(game_db)
    return id_lobby


def add_user_on_group(id_lobby, message):

    """Добавляет нового участника в уже существующее лобби"""

    id_lobby = int(id_lobby)
    if id_lobby in game_db.keys():
        game_db[id_lobby]['users'][message.chat.id] = {}
        return 'Вы успешно добавленны в игру'
    else:
        return 'Вы ввели неправильно id лобби'



def found_user_on_lobbyes(message) -> int:

    """Находит пользователя в лобби"""

    for i in game_db.keys():
        if message.chat.id in list(game_db[i]['users'].keys()):
            return i
    else:
        return 0


