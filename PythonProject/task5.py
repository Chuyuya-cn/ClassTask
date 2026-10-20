bm=0

n,m = map(int, input().split())
ar=list(map(int,input().split()))
lis=[0]*(n)


for i in range(m):
    w=str(input())
    if w[0]=="I":
        _,a,b=map(w)
        int(a,b)
        ar.insert(a+1+lis[a],b)
        lis[a]+=1
    else:
        if w=="MIN_GAP":
            for i in range(n):
                b = abs(ar[i] - ar[i - 1])
                if b > bm:
                    bm = b
        elif w=="MIN_SORT_GAP":
            new=ar.copy()
            new.sort()
            for i in range(n):
                b = abs(new[i] - new[i - 1])
                if b > bm:
                    bm = b
