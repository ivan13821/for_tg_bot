step_game = {}

game_db = {}

def create_lobby(message):

    """Создание лобби для игры"""

    if message.chat.id not in step_game.keys():
        step_game[message.chat.id] = 1
    else:
        if step_game[message.chat.id] != 0:
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
    print(game_db)
    return id_lobby
