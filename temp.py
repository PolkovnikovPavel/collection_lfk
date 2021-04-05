count = 0
min_ = 14455
for i in range(1740, 14455):
    if i % 4 == 0 and i % 5 == 0:
        if i % 8 != 0 and i % 12 != 0 and i % 16 != 0 and i % 30 != 0:
            print(i)
            count += 1

print(count)