custom_list = input("Enter List Elements with a space : ")
LIST = list((map(int, custom_list.split())))
print(LIST)
EVEN_LIST = []
ODD_LIST = []

for i in range(len(LIST)):
    if LIST[i] % 2 == 0:
        EVEN_LIST.append(LIST[i])
    else:
        ODD_LIST.append(LIST[i])


print(ODD_LIST)
print(EVEN_LIST)