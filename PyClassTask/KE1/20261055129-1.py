#INIT
import turtle as t
t.screensize(1000,600)
t.setup(1000,600)
t.pensize(12)
t.speed(0)
def d(color,x,y):
    t.penup()
    t.goto(x,y)
    t.pendown()
    t.color(color)
    t.circle(60)
#1
d("blue",-150,0)
d("black",0,0)
d("red",150,0)
#2
d("yellow",-75,-60)
d("green",75,-60)
#


t.hideturtle()
t.done()
