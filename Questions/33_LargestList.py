custom_list = input("Enter List Elements with a space : ")
LIST = list((map(int, custom_list.split())))
print(LIST)

maximum = LIST[0]

for i in LIST :
    if i > maximum:
        maximum = i
print("Largest Element in the List is : ", maximum)
