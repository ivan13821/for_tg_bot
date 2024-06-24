from database import testing_database


def in_group(message):
    for key in testing_database.keys():
        if testing_database[key]['id'] == message.chat.id:
            return True
    else:
        return False