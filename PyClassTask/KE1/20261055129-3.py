##INIT
import turtle as t
t.pencolor("yellow")
t.speed(0)
t.screensize(800, 500)
t.setup(800,500)

#def XING
def st(len,h,x,y):
    t.seth(h+90-18)
    t.teleport(x,y)
    t.fillcolor("yellow")
    t.begin_fill()
    a=len*0.4
    for i in range(5):
         t.fd(a)
         t.left(72)
         t.fd(a)
         t.right(180-36)
    t.end_fill()
    #左下x0



###QIzi
t.pencolor("red")
t.fillcolor("red")
t.teleport(400,-250)
t.begin_fill()
for i in range(2):
    t.left(90)
    t.fd(500)
    t.left(90)
    t.fd(800)
t.end_fill()



###XING
t.pencolor("yellow")
st(len=100,h=0,x=-300,y=70)

st(len=30,h=-40,x=-200,y=160)
st(len=30,h=-70,x=-180,y=130)
st(len=30,h=0,x=-180,y=75)
st(len=30,h=-60,x=-205,y=55)


t.hideturtle()
t.done()