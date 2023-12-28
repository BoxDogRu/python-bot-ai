
# todo: написать приветственное сообщение
welcome_message = """Привет, друзья!
С наступающим Новым годом! Меня зовут Тайный Санта, и я здесь, чтобы добавить волшебства в наш праздник. Настало время веселья, удивительных сюрпризов и тайных подарков!"""



# todo: написать функцию, которая будет перемешивать пользователей
# todo: для каждого участника надо заполнить поле "send_to"
# "send_to" - id пользователя, которому участник должен сделать подарок
def shuffle_users(user_data):
    """
    Функция, перемешивающая пользователей.
    Принимает на вход словарь с данными пользователей.
    Возвращает словарь с данными пользователей, в котором каждому пользователю
    присвоен id другого пользователя, которому он должен сделать подарок.
    """
    import random
    users = list(user_data.keys())

    # Пример сортировки списков без изменения списка и с изменением списка
    # my_list = sorted(my_list, reverse=True)
    # my_list.sort(reverse=True)

    # users = random.shuffle(users)
    random.shuffle(users)

    for ind, user in enumerate(users):
        # user_data[user]["send_to"] = users[min(ind + 1, len(users) - 1)]
        user_data[user]["send_to"] = users[(ind + 1) % len(users)]
    return user_data
