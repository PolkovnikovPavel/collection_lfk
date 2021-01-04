num = 78
x = 0

while True:
    num += 1
    x = num

    L = x
    M = 65
    if L % 2 == 0:
        M = 52
    while L != M:
        if L > M:
            L = L - M
        else:
            M = M - L

    if M == 26:
        print(num)
        print(M)
        break
