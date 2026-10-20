t=int(input("练习1or2"))


if t==1:
    a,b,c=map(int,input("输入用空格隔开").split())
    print(a**2+b**2+c**2)


if t==2:
    a,b,c=map(float,input("输入用空格隔开").split())
    d=b**2-4*a*c
    if d>0:
        d=d**(1/2)
        x1 = (d-b)/(2*a)
        x2 = (-d-b)/(2*a)
        print(x1)
        print(x2)
    elif d==0:
        print("重根")
        print(-b/(2*a))
    else:
        print("无实根")