num=int(input('请输入星的个数，个数不能大于10'))
if num>10 or num<0:
    print("error")
else:
    for i in range(1,num+1):
      print(format('*'*i,'_>10'))
    for i in range(num,1,-1):
      print(format('*'*i,'_>10'))