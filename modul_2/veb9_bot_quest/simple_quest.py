import random

print('Приветствую тебя, дорогой игрок!')

print('''Предлагаю тебе сыграть в игру, в которой от твоих вариантов ответа зависит исход. 
Ты готов(а)? Введи 1/2''')

choice = int(input())
win = False
if choice == 1:
    print('''Тогда поехали!
Ты очнулся в тёмном помещении, не видишь собственных пальцев. Не долго мешкая, ты начинаешь искать
что угодно на полу, водя по нему руками. Вдруг находишь зажигалку (какой-никакой, а источник света).
Пройдя немного вперед, ты видишь два пути: 
1. Вправо
2. Влево. 
Куда пойдешь?''')

    choice = int(input())

    if choice == 1:
        print('''Завернув направо, ты начинаешь ощущать холод... Что-то зловщее в этой части лабиринта, в который
ты попал. Идя уже минут 10 вперед, ты наталкиваешься на некое существо, которое не реагирует
на твою зажигалку. Будить?
1. Да
2. Не надо''')
        choice = int(input())
        if choice == 1:
            print('''Существо просыпается, но не проявляет агрессии. А предлагает угадать загаданное им число
за 5 попыток, тогда оно пропустит тебя дальше. Кажется, любопытнее согласиться... 
Существо говорит, что загадало число от 1 до 20. Как думаешь, какое?''')

            cnt_try = 5

            random_number = random.choice(range(1, 20))

            while cnt_try > 0:
                choice = int(input())
                cnt_try -= 1
                if random_number > choice:
                    print(f'Нет, число больше. Осталось {cnt_try} попыток.')
                elif random_number < choice:
                    print(f'Нет, число меньше. Осталось {cnt_try} попыток.')
                elif random_number == choice:
                    print('Ура, ты угадал(а)!')
                    break
            if random_number == choice:
                win = True
                print('Существо жмет тебе руку, дает фонарик и пропускает вперед')
            else:
                print('К сожалению, ты не угадал число, существо прогнало тебя и ты заплутал в лабиринте...')
        else:
            win = True
            print('''И правда, зачем его будить... Оглядевшись, ты обнаружил подозрительно выпирающий камень.
Надавив на него, стена отодвинулась и ты нашел выход''')
    else:
        print('''Да, слева показалось безопаснее. Идя вперед, ты неожиданно заметил бумажку на стене. Берешь?
1. Да
2. Нет''')
        choice = int(input())

        if choice == 1:
            print('''На бумажке были какие-то 4 цифры. Непонятно, но ладно, ты положил ее в карман.
В какой-то момент перед собой ты увидел дверь. С замком. С кодом. Из цифр. Ты смекнул)
Попробуй перебирать цифры на замке, пока не угадаешь пароль.''')
            
            password = 1432

            while choice != password:
                choice = int(input())
                if choice == password:
                    win = True
                else:
                    print('Попытайся еще')
            if win:
                print('Ура, пароль подошел!')
            print('За дверью (ожидаемо :)) оказался выход')
        else:
            print('''Подозрительная бумажка. В какой-то момент перед собой ты увидел дверь. С замком.
Ты всё понял, побежал обратно за бумажкой, но ее там уже не было...''')

else:
    print('''Что ж, тогда желаю удачи, пока!''')

if win:
    print("Ура, вы выиграли!")
else:
    print("Увы, вы проиграли :(")