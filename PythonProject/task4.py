s = input().strip()
x = 0
chang = 0
var = ''
j = 1
t = 1
i = 0
n = len(s)
while i < n:
    c = s[i]
    if c == '+':
        t = 1
        i += 1
    elif c == '-':
        t = -1
        i += 1
    elif c == '=':
        j = -1
        t = 1
        i += 1
    else:
        num = 0
        den = False
        while i < n and s[i].isdigit():
            den = True
            num = num * 10 + int(s[i])
            i += 1
        if i < n and s[i].islower():
            var = s[i]
            val = num if den else 1
            x += j * t * val
            i += 1
        else:
            chang += j * t * num

ans = -chang / x
if abs(ans) < 0.0005:
    ans = 0.0
print(f"{var}={ans:.3f}")