first_num = int(input("Enter a number (0 to stop): "))
widest_fragment = 1
current_fragment = 1
next_num = int(input("Enter a number (0 to stop): "))

while next_num != 0:
    if next_num == first_num:
        current_fragment += 1
    else:
        widest_fragment = max(widest_fragment, current_fragment)
        current_fragment = 1
    first_num = next_num
    next_num = int(input("Enter a number (0 to stop): "))

widest_fragment = max(widest_fragment, current_fragment)
print("Length of the widest fragment is:", widest_fragment)

