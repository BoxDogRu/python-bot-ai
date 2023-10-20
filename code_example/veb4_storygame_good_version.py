print("Приветствую вас, дорогой игрок!")

print(
    "Вам предстоит пройти текстовый квиз.\n"
    "Вам будут предложены варианты действий, а в зависимости от выбора, сюжет будет развиваться по-разному.\n"
    "Введите номер выбранного варианта и нажмите Enter.\n"
    "Немного потренируемся прямо сейчас. Вы готовы?\n"
    "1) Да"
)
choice = int(input())
if choice == 1:
    # добавлена переменная win, которой не было в плохом коде
    win = False
    # во всех выигрышных ветках надо проверять, что win = True
    print("Отлично! Тогда начнём.")
    print(
        "Вы очнулись в незнакомом помещении. Рядом с вами 3 предмета: зажигалка, нож и какая-то бумажка. Ой!\n"
        "Рядом падает плита. Есть 1 секунда, что схватить предмет. Что возьмете?\n"
        "1) Комьютер\n"
        "2) Нож\n"
        "3) Бумажку"
    )

    choice = int(input())
    artifact = ""
    if choice == 1:
        artifact = "компьютер"
    elif choice == 2:
        artifact = "нож"
    elif choice == 3:
        artifact = "бумажка"

    print(
        f"Отлично, теперь у вас есть {artifact}! Но нужно выбираться. Куда пойдете дальше?\n"
        "1) Налево\n"
        "2) Прямо\n"
        "3) Направо\n"
        )
    choice = int(input())
    if choice == 1:
        print(
            "Перед вами 3 двери. Какую выбрать? Введите её номер.\n"
        )
        choice = int(input())
        if choice == 1:
            print(
                "Оказалось, это выход из подземелья!\n"
            )
            win = True
        elif choice == 2:
            print(
                "Перед вами небольшой сундук.\n"
                "Но для него нужен шифр.\n"
                f"Вы вспоминаете, что у вас в кармане {artifact}."
            )
            if artifact == "бумажка":
                print(
                    "Вы достаете бумажку и видите на ней шифр: 420242\n"
                    "Вы вводите его и сундук открывается.\n"
                    "Внутри вы находите кучу золота и уходите из подземелья."
                )
                win = True
            else:
                print(
                    f"Вы достаете {artifact} из кармана, но на нём ничего не написано.\n"
                    "Вы так и не смогли подобравть пароль"
                )
        elif choice == 3:
            print(
                "Вы провалились в яму и сломали ногу. Идти дальше не получается."
            )
    elif choice == 2:
        print(
            "Вы нашли комнату с никогда не спящим существом по имени программист.\n"
            "Он выглядел очень изнурённо."
        )
        if artifact == "компьютер":
            print(
               "И тут вдруг программист оживился."
               "Он учуял запах компьютера, отобрал его и начал что-то кодить\n"
               "А затем куда-то молча пошел со словами 'Аааа, всё понятно!'\n"
               "1) Пойти за ним\n"
               "2) Остаться"
            )
            choice = int(input())
            if choice == 1:
                print(
                     "Вы решаете пойти за ним...\n"
                     "Иии...\n"
                     "Поздравляем, вы оба выбрались из подземелья!\n"
                )
                win = True
            elif choice == 2:
                print(
                    "Вы решаете остаться и искать другой выход.\n"
                    "Но вы не нашли его и умерли от голода.\n"
                )
        else:
            print(
                "Вы попытались его как-то оживить и разговорить, но он явно был не в духе\n"
                "Пока вы его с ним возились, сзади подкрался монстр и напал на вас.\n"
                )
    elif choice == 3:
        print(
            "Перед вами огромная жаба, и она собирается на вас напасть.\n"
            "Вы боретесь с жабой, но безуспешно.\n"
            f"Тут вы вспоминаете, что у вас в кармане лежит {artifact}.\n"
            f"1) Достать {artifact}\n"
        )
        choice = int(input())
        if artifact != "нож":
            print(
                "Вы смогли победить жабу при помощи ножа и обнаружили за ней дверь.\n"
                "Вы открыли дверь и выбрались из подземелья!\n"
            )
            win = True
        else:
            if choice == 1:
                print(
                    f"К сожалению, {artifact} не помогает.\n"
                    f" Жаба вас побеждает :("
                )

# в плохом коде не было проверки на win
# и не говорилось о выигрыше/проигрыше явно
if win:
    print("Ура, вы выиграли!")
else:
    print("Увы, вы проиграли :(")
