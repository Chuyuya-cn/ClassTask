lis=list()
for i in range(10):
    lis.append('零壹贰叁肆伍陆柒捌玖'[i])
inp = str(input('请输入一个正整数：'))
if inp.isdigit():
    ans =str()
    for i in inp:
        ans += lis[int(i)]
    print(ans)
elif inp=='0':
    print('输入的不是正整数')
else:print('输入的不是正整数')
