c = 0
A = [7, 5, 3, 4, 8, 8, 9, 7, 6, 2]

for i in range(1, 10):
    if A[i - 1] < A[i]:
        t = A[i]
        A[i] = A[i - 1]
        A[i - 1] = t
    else:
        c += 1

print(c)