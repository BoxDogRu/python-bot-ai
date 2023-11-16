#Importing the required libraries
import turtle as donatello
import random

#Set the width of the pen Donatello uses
donatello.width(12.5)

#Set the maximum speed of drawing because we don't have all day
donatello.speed(0)

#The main algorithm
for i in range(100):

    donatello.color(*[random.random() for i in range(3)])

    steps = int(random.randrange(20, 50))
    angle = int(random.randrange(0, 181))

    if random.randrange(2) == 1:
        donatello.right(angle)

    else:
        donatello.left(angle)

    donatello.forward(steps)

donatello.color('black')
donatello.write('Donatello', align='right', font =
                ('Times New Roman', 30, 'italic'))

donatello.Screen().exitonclick()