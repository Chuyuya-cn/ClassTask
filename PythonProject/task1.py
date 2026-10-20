ans = []
a, b, c, d = map(float, input().split())
f = lambda x: a * x**3 + b * x**2 + c * x + d
for i in range(-100, 100):
    if f(i) * f(i + 1) <= 0:
        l_s, r_s = i, i + 1
        for _ in range(7):
            #2^-7是1/128，精度就小于0.1了
            mid = (l_s + r_s) / 2
            if f(l_s) * f(mid) <= 0:
                r_s = mid
            else:
                l_s = mid
        ans.append((l_s + r_s) / 2)
print(" ".join(f"{x:.2f}" for x in ans))