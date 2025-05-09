print("\nRectangle Visualization:")
print(f"  (x3, y3) -------- (x4, y4)")
print("   |                     |")
print(f"  (x1, y1) -------- (x2, y2)")

x1, y1 = map(int, input("Enter coordinates of point 1 (x y): ").split())
x2, y2 = map(int, input("Enter coordinates of point 2 (x y): ").split())
x3, y3 = map(int, input("Enter coordinates of point 3 (x y): ").split())

if x1 == x2:
    x4 = x3
elif x1 == x3:
    x4 = x2
else:
    x4 = x1


if y1 == y2:
    y4 = y3
elif y1 == y3:
    y4 = y2
else:
    y4 = y1

print(f"The coordinates of the 4th vertex are: ({x4}, {y4})")