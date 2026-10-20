inp=str(input('请输入字符串：'))
k=inp.count(' ')
a,b,c=0,0,0
for i in range(0,len(inp)):
    st=inp[i]
    if st.isdigit():
        a+=1
    elif st.isalpha() and st.isascii():
        b+=1
    elif st==' ':
        continue
    else:
        c+=1
print('该字符串中字母数目为：'+str(b))
print('该字符串中数字数目为：'+str(a))
print('该字符串中空格数目为：'+str(k))
print('该字符串中其他字符数目为：'+str(c))