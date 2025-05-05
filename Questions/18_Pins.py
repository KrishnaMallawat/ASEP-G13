n = int(input("Enter the number of pins (N): "))
k = int(input("Enter the number of balls (K): "))

pins = ["I"] * n
print("".join(pins))

for _ in range(k):
    start = int(input("Enter the starting pin to knock down: "))
    end = int(input("Enter the ending pin to knock down: "))
    for i in range(start - 1, end):
        pins[i] = "."

print("".join(pins))