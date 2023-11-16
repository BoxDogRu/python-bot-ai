import turtle as t
import random


def get_line_length():
    return 45


def get_line_width():
    return 5


line_length = get_line_length()
line_width = get_line_width()

t.shape('turtle')
t.fillcolor('green')
t.bgcolor('black')
t.speed('fastest')
t.pensize(line_width)
t.pendown()
t.color("white")


def inside_window():

    left_limit = (-t.window_width() / 2) + 100
    right_limit =(t.window_width() /2) -100
    top_limit = (t.window_height() / 2) - 100
    bottom_limit = (-t.window_height() / 2) + 100
    (x, y) = t.pos()
    inside = left_limit < x < right_limit and bottom_limit < y < top_limit

    return inside


def move_turtle(line__length):
    pen_colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
    t.pencolor(random.choice(pen_colors))
    if inside_window():
        angle = random.randint(0, 180)
        t.right(angle)
        t.forward(line__length)
    else:
        t.backward(line__length)


while True: move_turtle(line_length)
t.Screen().exitonclick()
