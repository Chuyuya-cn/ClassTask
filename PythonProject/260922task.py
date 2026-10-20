task=int(input(f'第几道题  1or2'))
if task==1:
    num=list(map(int,input().split()))
    import math
    print(sum(num))
    print(sum(num)/len(num))

elif task==2:
    a,b,c=map(float,input().split())
    import math
    p=(a+b+c)/2
    print(f'周长{2*p}面积{math.sqrt(p*(p-a)*(p-b)*(p-c))}')