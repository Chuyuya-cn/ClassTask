num = str(input('请输入一个四位10进制整数进行加密'))
if num.isdigit() and len(num) == 4:
    a=''
    for i in range(4):
        a+=str((int(num[i])+5)%10)
    b=''
    b+=a[2]
    b+=a[3]
    b+=a[0]
    b+=a[1]
    print(f'加密后的整数为：{b}')
else:
    print('输入的不是整数')