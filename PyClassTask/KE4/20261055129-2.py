sum=0
j,t=1,1
for i in range(1,101):
    j+=t
    t=j-t
    sum+=(j/t)
print(sum)
