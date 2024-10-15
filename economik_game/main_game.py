from aiogram.fsm.state import StatesGroup, State
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from Homework.database import get_db
from economik_game.keyboard import *
from economik_game.economik_game import *
from economik_game.credit_func import *
from economik_game.year import *
from economik_game.for_group import *



router = Router()

class MyForm(StatesGroup):
    message_from_all = State()
    join_or_create = State()
    game = State()
    choice = State()
    input_id = State()
    stop_op = State()
    input_name = State()
    production_option = State()
    reference = State()
    game_credit = State()
    add_credit = State()
    pay_for_credit = State()
    want_exit = State()
    groups = State()
    create_group = State()
    join_to_group = State()
    get_res = State()




@router.message(MyForm.stop_op)
async def stop_all_op(message: types.Message, state: FSMContext):

    """"Удаление пользователя из БД"""

    id_lobby = users_l[message.chat.id]

    try:
        del game_db[id_lobby]['users'][message.chat.id]
    except KeyError:
        pass

    try:
        admins[id_lobby].remove(message.chat.id)

        if admins[id_lobby] == []:
            del admins[id_lobby]

    except KeyError:
        pass


    try:
        groups[id_lobby][Group.user_in_group(message)].remove(message.chat.id)

        if not groups[id_lobby][Group.user_in_group(message)]:
            del groups[id_lobby][Group.user_in_group(message)]

        if not not groups[id_lobby]:
            del groups[id_lobby]

    except KeyError:
        pass


    del users_l[message.chat.id]

    if game_db[id_lobby]['users'] == {}:
        del game_db[id_lobby]



    await state.clear()

    await message.answer('Все ваши операции связанные с игрой завершены', reply_markup=MyKeyboard.menu())












@router.message(StateFilter(None), F.text == '/game')
async def start_game(message: types.Message, state: FSMContext):

    """Первый шаг при запуске/приединение к игре"""

    await message.answer("Вы хотите начать новую игру или присоединиться к существующей?", reply_markup=MyKeyboard.join_create())
    await state.set_state(MyForm.join_or_create)











@router.message(MyForm.join_or_create, F.text == 'Начать новую игру')
async def step_start_1(message: types.Message, state: FSMContext):

    """Функция описывает 1 шаг при создании лобби"""

    id_lobby = EconomicGame.create_lobby(message)


    if type(id_lobby) == type(1):
        await message.answer(f'id лобби: {id_lobby}', reply_markup=MyKeyboard.A_B_C())
        await message.answer('Выберете пожалуйста кокой вариант ресурсов вы хотели бы получить при начале игры')
        await message.answer('Вариант А\n'
                             'деньги: 4000\n'
                             'Здание: 7 ед\n'
                             'Сырье: 30 ед\n'
                             '\n'
                             'Вариант Б\n'
                             'Деньги: 4000\n'
                             'Оборудование: 14 ед\n'
                             'Рабочие: 18 ед\n'
                             '\n'
                             'Вариант В\n'
                             'Деньги: 4000\n'
                             'Технология: 10 ед\n'
                             'Транспорт: 12 ед\n')

        await state.set_state(MyForm.choice)
    else:
        await message.answer(f'{id_lobby}', reply_markup=MyKeyboard.back_on_menu())












@router.message(MyForm.join_or_create, F.text == 'Присоединиться')
async def join_to_lobby(message: types.Message, state: FSMContext):

    """Для присоединения человека к лобби, ввод id на след шаге"""

    await message.answer('Введите id лобби к которому вы хотите подключиться', reply_markup=ReplyKeyboardRemove())
    await state.set_state(MyForm.input_id)














@router.message(MyForm.input_id)
async def input_id(message: types.Message, state: FSMContext):

    """Получение id"""

    if message.text == 'Выйти в меню':
        await stop_all_op(message, state)
    else:
        result_add = EconomicGame.add_user_on_lobby(message.text, message)

        await message.answer(result_add, reply_markup=MyKeyboard.back_on_menu())
        if result_add == 'Вы успешно добавленны в игру':
            #await EconomicGame.message_from_list(f'К игре присоединился: {message.chat.username}', list(game_db[int(message.text)]['users'].keys()), but_id=message.chat.id)
            await message.answer('Выберете пожалуйста кокой вариант ресурсов вы хотели бы получить при начале игры', reply_markup=MyKeyboard.A_B_C())
            await message.answer('Вариант А\n'
                                 'деньги: 4000\n'
                                 'Здание: 7 ед\n'
                                 'Сырье: 30 ед\n'
                                 '\n'
                                 'Вариант Б\n'
                                 'Деньги: 4000\n'
                                 'Оборудование: 14 ед\n'
                                 'Рабочие: 18 ед\n'
                                 '\n'
                                 'Вариант В\n'
                                 'Деньги: 4000\n'
                                 'Технология: 10 ед\n'
                                 'Транспорт: 12 ед\n')

            await state.set_state(MyForm.choice)














@router.message(MyForm.choice)
async def choice(message: types.Message, state: FSMContext):

    """Пользователь выбирает какой вариант ресурсов он хочет получить"""

    if message.text == 'admin':

        EconomicGame.add_admin(message)

        await message.answer('Вы добавлены в игру как администратор', reply_markup=MyKeyboard.game_for_admin())
        await state.set_state(MyForm.game)


    else:
        if message.text == 'Выйти в меню':
            await stop_all_op(message, state)

        else:
            result = EconomicGame.add_start_res(message)
            if result:
                await message.answer('Начальные ресурсы получены', reply_markup=ReplyKeyboardRemove())
                await message.answer('Введите пожалуста ник под которым вы будете играть (ник не должен быть больше 10 символов)')
                await state.set_state(MyForm.input_name)
            else:
                await message.answer('Выберете пожалуйста вариант из всплывающей клавиатуры')
                await state.set_state(MyForm.choice)















@router.message(MyForm.input_name)
async def input_name(message: types.Message, state: FSMContext):

    """Пользователь пишет свой ник"""

    if message.text == 'Выйти в меню':
        await stop_all_op(message, state)

    else:

        if len(list(message.text)) > 10:
            await message.answer(f'Введите пожалуста ник до 10 символов')
            await state.set_state(MyForm.input_name)
        else:

            for i in users_name.keys():
                if users_name[i]['nik'] == message.text:
                    await message.answer('К сожалению этот ник уже занят, напишите пожалуйста другой')
                    await state.set_state(MyForm.input_name)
                    break
            else:
                users_name[message.chat.id] = {'nik':message.text, 'username':message.chat.username}
                await message.answer(f'Вы в игре под ником {message.text.strip()}', reply_markup=MyKeyboard.menu_in_game())
                await state.set_state(MyForm.game)
















@router.message(MyForm.game)
async def game(message: types.Message, state: FSMContext):

    """Обработчик внутри игровых событий"""


    if message.text == 'Выйти в меню': #Выводит игрока в игру и удаляет все данные о нем
        await message.answer('Вы хотите выйти из игры?\nЕсли вы выйдете из игры все данные будут удалены', reply_markup=MyKeyboard.yes_or_no())
        await state.set_state(MyForm.want_exit)





    elif message.text == 'История': #
        await EconomicGame.show_operations(message)



    elif message.text == 'Объединения':

        await message.answer('Выберете действие', reply_markup=MyKeyboard.groups())
        await state.set_state(MyForm.groups)




    elif message.text == 'Ресурсы игрока' and message.chat.id in admins[users_l[message.chat.id]]: #admin_command

        await message.answer('Введите ник игрока', reply_markup=ReplyKeyboardRemove())
        await state.set_state(MyForm.get_res)






    elif message.text == 'Мои ресурсы':#Показывает экономические ресурсы пользователя

        result_message = ''

        if Group.user_in_group(message):
            for i in game_db[users_l[message.chat.id]]['users'][Group.user_in_group(message)]['ресурсы'].items():
                result_message = result_message + f'{i[0]}: {i[1]}\n'
            await EconomicGame.message_from_user(message.chat.id, result_message)

        else:
            for i in game_db[users_l[message.chat.id]]['users'][message.chat.id]['ресурсы'].items():
                result_message = result_message+f'{i[0]}: {i[1]}\n'
            await EconomicGame.message_from_user(message.chat.id, result_message)





    elif message.text == 'Повысить уровень производства':
        await message.answer('Выберете вариант производства, который вы хотели бы приобрести', reply_markup=MyKeyboard.product_option())
        await state.set_state(MyForm.production_option)





    elif message.text == 'Кредит':
        await message.answer('Выберете действие', reply_markup=MyKeyboard.credit())
        await state.set_state(MyForm.game_credit)





    elif message.text == 'Cправка':
        await message.answer('Выберете какую информацию вы хотели бы получить', reply_markup=MyKeyboard.reference())
        await state.set_state(MyForm.reference)





    elif 'купить' in message.text.lower():#покупка ресурсов
        await message.answer(EconomicGame.bye(message), parse_mode="Markdown")




    elif message.text == 'admin_res' and str(message.chat.id) in ['1077069914','5410213052']: #it is admin id
        EconomicGame.admin_res(message)
        await message.answer('Ресурсы для админа добавленны')




    elif 'продать' in message.text.lower():#продажа ресурсов
        await message.answer(EconomicGame.sold(message), parse_mode="Markdown")





    elif 'обменять' in message.text.lower() or 'обмен' in message.text.lower():#обмен ресурсов
        await message.answer(EconomicGame.swap(message), parse_mode="Markdown")




    elif message.text == 'Закончить игру' and message.chat.id in admins[users_l[message.chat.id]]:


        await EconomicGame.show_winner(users_l[message.chat.id], message=message)

        del game_db[users_l[message.chat.id]]





    elif message.text == 'Список игроков':#вывод всех игроков

        result = ''
        for i in game_db[users_l[message.chat.id]]['users'].keys():
            try:
                result += f'{users_name[i]['username']}: {users_name[i]['nik']}\n'
            except KeyError:
                for j in groups[users_l[message.chat.id]][i]:
                    result += f'{users_name[j]['username']}: {users_name[j]['nik']} (В группе: {i})\n'

        await message.answer(result)

    else:
        await message.answer('К сожалению я не знаю такой команды, убедитесь в правильности ее написания')








@router.message(MyForm.get_res)
async def get_res_from_admin(message: types.Message, state: FSMContext):

    """Получение ника пользователя для просмотра админом его ресурсов"""

    result_message = ''

    user_id = None

    for i in users_name.items():
        if i[1]['nik'] == message.text:
            user_id = i[0]
            break
    else:
        await message.answer('Неправильный ник пользователя', reply_markup=MyKeyboard.game_for_admin())
        await state.set_state(MyForm.game)

    if user_id is not None:
        if Group.user_in_group(chat_id=user_id):
            for i in game_db[users_l[message.chat.id]]['users'][Group.user_in_group(message)]['ресурсы'].items():
                result_message = result_message + f'{i[0]}: {i[1]}\n'
            await message.answer(result_message, reply_markup=MyKeyboard.game_for_admin())
            await state.set_state(MyForm.game)

        else:
            for i in game_db[users_l[message.chat.id]]['users'][user_id]['ресурсы'].items():
                result_message = result_message + f'{i[0]}: {i[1]}\n'
            await message.answer(result_message, reply_markup=MyKeyboard.game_for_admin())
            await state.set_state(MyForm.game)









@router.message(MyForm.groups)
async def groups_keyboard(message: types.Message, state: FSMContext):

    """ Взаимодейтвие с группами """

    if message.text == 'Назад':
        await message.answer('Вы вышли в основное меню игры', reply_markup=MyKeyboard.menu_in_game())
        await state.set_state(MyForm.game)

    elif message.text == 'Создать группу':
        await message.answer('Введите название группы', reply_markup=MyKeyboard.back_on_menu())
        await state.set_state(MyForm.create_group)

    elif message.text == 'Присоединиться к группе':
        await message.answer('Введите название группы', reply_markup=MyKeyboard.back_on_menu())
        await state.set_state(MyForm.join_to_group)

    elif message.text == 'Покинуть группу':
        await message.answer(Group.leave_on_group(message))

    elif message.text == 'Игроки в группе':
        await message.answer(Group.show_users_in_group(message))

    else:
        await message.answer('Выберете пожалуйста вариант из всплывающей клавиатуры')







@router.message(MyForm.join_to_group)
async def create_group(message: types.Message, state: FSMContext):

    """ Пользователь присоединяется к группе """

    if message.text != 'Выйти в меню':
        result = Group.add_user_on_group(message)


        await message.answer(result, reply_markup=MyKeyboard.menu_in_game())
        await state.set_state(MyForm.game)


    else:
        await message.answer('Вы вернулись в меню игры', reply_markup=MyKeyboard.menu_in_game())
        await state.set_state(MyForm.game)










@router.message(MyForm.create_group)
async def create_group(message: types.Message, state: FSMContext):

    """ Обрабатывает название группы и создает группу с таким названием """

    if message.text != 'Выйти в меню':
        result = Group.create_group(message)


        await message.answer(result, reply_markup=MyKeyboard.menu_in_game())
        await state.set_state(MyForm.game)


    else:
        await message.answer('Вы вернулись в меню игры', reply_markup=MyKeyboard.menu_in_game())
        await state.set_state(MyForm.game)















@router.message(MyForm.want_exit)
async def want_exit(message: types.Message, state: FSMContext):

    """Проверяет хочет ли пользователь выйти или хочет вернуться в игру"""

    if message.text == 'Да':
        await stop_all_op(message, state)

    elif message.text == 'Нет':
        await message.answer('Вы вернулись в игру', reply_markup=MyKeyboard.menu_in_game())
        await state.set_state(MyForm.game)

    else:
        await message.answer('Выберете пожалуйста вариант из списка')











@router.message(MyForm.production_option)
async def prod_option(message: types.Message, state: FSMContext):

    """ Повышает уровень производства и, если нужно отправляет всем пользователям в группе уведомление о начале нового года """

    result = EconomicGame.sold_on_rialto(message)


    await message.answer(result, reply_markup=MyKeyboard.menu_in_game())

    if result == 'Успешно':
        EconomicGame.add_operation(message, text=f'Повышение уровня производства на {message.text}')

    if Years.new_year(message):
        credit.choice_credit_bid(users_l[message.chat.id])
        credit.new_year(message)
        await EconomicGame.message_from_list('Начался новый год!!!', game_db[users_l[message.chat.id]]['users'].keys(), main_message=message)

    await state.set_state(MyForm.game)




@router.message(MyForm.game_credit)
async def with_credit(message: types.Message, state: FSMContext):

    """ Взаимодейтвие с кредитом """

    if message.text == 'Назад':
        await message.answer('Вы вышли в основное меню игры', reply_markup=MyKeyboard.menu_in_game())
        await state.set_state(MyForm.game)

    elif message.text == 'Взять кредит':
        await message.answer('Введите сумму кредита')
        await state.set_state(MyForm.add_credit)

    elif message.text == 'Заплатить по кредиту':
        await message.answer('Введите сумму платежа')
        await state.set_state(MyForm.pay_for_credit)

    elif message.text == 'Посмотреть задолжность':
        await message.answer(credit.show_user_credit(message))

    elif message.text == 'Посмотреть ставку':
        await message.answer(credit.show_credit_bid(message))









@router.message(MyForm.add_credit)
async def add_credit(message: types.Message, state: FSMContext):

    """ Добавляет новый кредит """

    await message.answer(credit.add_credit(message), reply_markup=MyKeyboard.menu_in_game())
    await state.set_state(MyForm.game)







@router.message(MyForm.pay_for_credit)
async def pay_credit(message: types.Message, state: FSMContext):

    """ Выполняет платеж по кредиту"""

    await message.answer(credit.pay_credit(message), reply_markup=MyKeyboard.menu_in_game())
    await state.set_state(MyForm.game)













@router.message(MyForm.reference)
async def prod_option(message: types.Message, state: FSMContext):

    if message.text == 'Тех. карта':#Информация о этапах производства и нужных для этого ресурсах


        for i in back_game['тех_карта'].items():
            result_message = ''
            result_message += '*'+i[0]+ '%' +'*'+'\n'+'*'+'экономические ресурсы:'+'*'+'\n'
            for j in i[1]['эк_рес'].items():
                result_message += j[0]+': '+str(j[1])+'\n'

            result_message += '*' + 'себестоимость: ' + str(i[1]['себестоимость']) + '*' + '\n'
            result_message += '*' + 'выручка: ' + str(i[1]['выручка']) + '*' + '\n'
            await message.answer(result_message, parse_mode="Markdown")

    elif message.text == 'Шаблоны':#Показывает шаблоны сообщений
        await message.answer('Шаблон 1 (покупка или продажа):\n'
                             '*| действие | пользователь | ресурс | количество | цена\n*'
                             'Пример:\n'
                             '*купить иван сырье 5 500\n*'
                             '(Покупка у пользователя под ником "иван" ресурс "сырье" в количестве 5 шт и по цене 500 д.ед)', parse_mode="Markdown")
        await message.answer('Если вы продаете или покапаете ресурсы на биржу, то не нужно указывать цену',
                             parse_mode="Markdown")

        await message.answer('Шаблон 2 (обмен ресурсами):\n'
                             '| действие | 2 сторона | ресурс 1 | количество рес 1 | ресурс 2 | количество рес 2 | *ресурс 1 идет вам*|\n'
                             'Например\n'
                             '*обмен олег сырье 7 оборудование 2*', parse_mode="Markdown")


    elif message.text == 'Биржа':#Информация о ценах на бирже
        result_message = ''
        for i in back_game['ресурсы'].items():
            result_message = result_message + f'{i[0]}: {i[1]}\n'
        await EconomicGame.message_from_user(message.chat.id, result_message)

    elif message.text == 'Назад':

        try:
            if message.chat.id in admins[users_l[message.chat.id]]:
                await message.answer('Вы вернулись в игру', reply_markup=MyKeyboard.game_for_admin())
                await state.set_state(MyForm.game)
            else:
                await message.answer('Вы вышли в игру', reply_markup=MyKeyboard.menu_in_game())
                await state.set_state(MyForm.game)
        except KeyError:
            await message.answer('Вы вышли в игру', reply_markup=MyKeyboard.menu_in_game())
            await state.set_state(MyForm.game)


