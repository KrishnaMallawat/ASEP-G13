x = int(input("Enter first number: "))
y = int(input("Enter second number: "))
if x == y:
    print("Both numbers are equal")
else:
    def maximum(a, b):
        if a > b:
            return a
        else:
            return b
print("Maximum is:", maximum(x, y))
