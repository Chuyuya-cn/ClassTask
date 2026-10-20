st = str(input())
ans = ''
for i in range(0, len(st)):
    ans += st[len(st) - i-1]
print(ans)
