import turtle as t


def rectangle(horizontal, vertical, color):
    t.pendown() #Опускает перо и начинает рисовать
    t.pensize(1)
    t.color(color)
    t.begin_fill()
    for counter in range(2): #Числа внутри списка range (1,3) означают, что цикл сделает 2 прохода.
        t.forward(horizontal)
        t.right(90)
        t.forward(vertical)
        t.right(90)
    t.end_fill()
    t.penup() #Поднимает перо, чтобы прекратить рисование

t.penup()
t.bgcolor('Dodger blue') #Делает фон светло-васильковым.`
t.speed('slow') #Устанавливает скорость «медленно».

# ступни. Этот комментарий поясняет, какую часть робота мы рисуем.
t.goto(-100, - 150) #Перемещает черепашку в точку с координатами х =-100, у = -150.
rectangle(50, 20, 'blue') #Рисует синий прямоугольник шириной 50 и высотой 20 пикселей.
t.goto(-30, -150)
rectangle(50, 20, 'blue')

# ноги
t.goto(-25, -50)
rectangle(15, 100, 'grey')
t.goto(-55, -50)
rectangle(-15, 100, 'grey')

# туловище
t.goto(-90, 100)
rectangle(100, 150, 'red')

# руки
t.goto(-150, 70)
rectangle(60, 15, 'grey')
t.goto(-150, 110)
rectangle(15, 40, 'grey')
t.goto(10, 70)
rectangle(60, 15, 'grey')
t.goto(55, 110)
rectangle(15, 40, 'grey')

# шея
t.goto(-50, 120)
rectangle(15, 20, 'grey')

# голова
t.goto(-85, 170)
rectangle(80, 50, 'red')

# глаза
t.goto(-60, 160)
rectangle(30, 10, 'white')
t.goto(-55, 155)
rectangle(5, 5, 'black')
t.goto(-40, 155)
rectangle(5, 5, 'black')

# рот
t.goto(-65, 135)
rectangle(40, 5, 'black')
t.hideturtle()
t.done()
