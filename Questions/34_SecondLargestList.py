custom_list = input("Enter List Elements with a space : ")
LIST = list((map(int, custom_list.split())))
print(LIST)

one, two = float('-inf') , float('-inf')
for i in LIST:
    if i > one:
        two = one
        one = i
    elif i > two and i != one:
        two = i
print("Second Largest Element in the List is : ", two)