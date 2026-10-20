n = int(input())
bm = -1
bn = ""
tot = 0
for _ in range(n):
    name, a, r, l, w, p = input().split()
    a, r, p = int(a), int(r), int(p)
    m = 0
    if a > 80 and p >= 1: m += 8000
    if a > 85 and r > 80: m += 4000
    if a > 90: m += 2000
    if a > 85 and w == 'Y': m += 1000
    if r > 80 and l == 'Y': m += 850
    tot += m
    if m > bm:
        bm, bn = m, name
print(bn)
print(bm)
print(tot)