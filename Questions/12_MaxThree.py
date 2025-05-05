print("Enter three numbers:")
a = int(input())
b = int(input())
c = int(input())

if a >= b and a >= c:
    max_num = a
elif b >= a and b >= c:
    max_num = b
else:
    max_num = c

print("Maximum number is:", max_num)
