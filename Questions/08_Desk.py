a = int(input("Enter the number of students in class 1: "))
b = int(input("Enter the number of students in class 2: "))
c = int(input("Enter the number of students in class 3: "))

desks_class_1 = (a + 1) // 2
desks_class_2 = (b + 1) // 2
desks_class_3 = (c + 1) // 2

total_desks = desks_class_1 + desks_class_2 + desks_class_3

print("The total number of desks needed is:", total_desks)
