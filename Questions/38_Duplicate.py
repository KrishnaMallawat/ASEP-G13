custom_list = input("Enter List Elements with a space : ")
LIST = list(map(int, custom_list.split()))
print(LIST)

i = 0
while i < len(LIST):
    for j in range(i + 1, len(LIST)):
        if LIST[i] == LIST[j]:
            LIST.pop(j)
            break
    else:
        i += 1

print("Updated List: ", LIST)
