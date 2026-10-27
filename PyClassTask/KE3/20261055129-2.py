num=int(input('请输入星数，（数值在1-9之间的奇数）'))
if num%2==1 and 1 <= num <= 9:
    for i in range(1,num+1,2):
        print(format('*'*i,f' ^{num}'))
    for i in range(num-2,-1,-2):
        print(format('*'*i,f' ^{num}'))
else :
    print('error')