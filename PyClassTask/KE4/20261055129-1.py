while True:
    n=int(input('请输入一个正整数：'))
    if n==0:
        break
    elif n<0:
        print('输入错误！')
    else:
        m = 1
        for i in range(1,n+1):

            m=m*i
        print(f'{n}!={m}')
