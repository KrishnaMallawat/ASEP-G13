import random

custom_list = input("Enter List Elements with a space : ")
LIST = list((map(int, custom_list.split())))
print(LIST)

random_INT = random.randint(1, 20)
print(f"Random Integer : {random_INT}")

FINAL_LIST = LIST + [random_INT]
print(FINAL_LIST)