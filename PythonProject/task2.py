a, b, c, d = map(float, input().split())

def f(x):
    return a * x**3 + b * x**2 + c * x + d

roots = []
for i in range(-100, 100):
    x1, x2 = float(i), float(i + 1)
    if f(x1) == 0:
        roots.append(x1)
    if f(x1) * f(x2) < 0:
        while x2 - x1 > 0.001:
            mid = (x1 + x2) / 2
            if f(mid) * f(x1) <= 0:
                x2 = mid
            else:
                x1 = mid
        roots.append((x1 + x2) / 2)

print("%.2f %.2f %.2f" % (roots[0], roots[1], roots[2]))