


game_db = {}
step_game = {}

def create_lobby(message):

    """Создание лобби для игры"""

    if message.chat.id not in step_game.keys():
        step_game[message.chat.id] = 2
    else:
        if step_game[message.chat.id] == 2:
            return 'Лобби не может быть созданно т.к вы уже пытаетесь создать лобби либо не завершили игру'

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
    #print(game_db)
    step_game[message.chat.id] = 2
    return id_lobby




def is_this_id(message):

    """Проверяет является ли это сообщением id или нет"""

    if message.chat.id in step_game.keys():
        if step_game[message.chat.id] == 1:
            try:
                int(message.text)
                return True
            except:
                return False

    return False


def add_user_on_group(id_lobby, message):

    """Добавляет нового участника в уже существующее лобби"""

    id_lobby = int(id_lobby)
    if id_lobby in game_db.keys():
        game_db[id_lobby]['users'][message.chat.id] = {}
        step_game[message.chat.id] = 2
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


