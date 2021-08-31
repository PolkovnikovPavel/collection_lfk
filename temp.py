points = int(input())

strings = points // 16000 * 7
wolf = points // 16000 * 8
rabbit = points // 16000 * 4

count = (strings - 6) // 2
wolf = wolf - 10 - count * 2
rabbit = rabbit - 5 - count
strings = strings - 6 - count * 2

print(count)
print('______')
print(strings)
print(wolf)
print(rabbit)
input()

