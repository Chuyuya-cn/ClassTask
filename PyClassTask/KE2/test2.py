if int(input(f'Which task?Type 1 or 2'))==1:

    st=input()
    lis=''
    for c in st:
        if not c=='d':
            lis+=c
        else:
            lis+='a'
    print(lis)
else:
    st = input()
    print(''.join(c for c in st if c.isdigit()))