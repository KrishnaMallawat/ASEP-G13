n = int(input("How many Fibonacci numbers? "))

first = 0
second = 1

for i in range(n):
    print(first, end=" ")
    next_number = first + second
    first = second
    second = next_number
