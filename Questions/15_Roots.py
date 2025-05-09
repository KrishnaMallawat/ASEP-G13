print("Enter coefficients a, b, c:")
a = float(input("a = "))
b = float(input("b = "))
c = float(input("c = "))

d = b * b - 4 * a * c
print( f"Discriminant is: {d}" )

if d >= 0:
    root1 = (-b + d ** 0.5) / (2 * a)
    root2 = (-b - d ** 0.5) / (2 * a)
    print("Real roots:")
    print("Root 1 =", root1)
    print("Root 2 =", root2)

else:
    real = -b / (2 * a)
    imag = ( -d ) ** 0.5 / (2 * a)
    print("Complex roots:")
    print("Root 1 =", real, "+", imag, "i")
    print("Root 2 =", real, "-", imag, "i")

