a=int(input('请输入一个正整数：'))
sum=0
if a<=0:
    print('输入错误！')
else:
    for i in range(2,a+1):
        type=False
        for j in range(2,i):
            if i%j==0:
                type = True
                break
        if type==False:
         sum += i
    print(f'从1到{a}的所有质数的和为：{sum}')