custom_tuple = (input("Enter Tuple Elements with a space : "))
intermediate = (custom_tuple.split())
TUPLE = tuple(intermediate)
print(TUPLE)

#

custom_list1 = input("Enter List Elements with a space : ")
LIST1 =  custom_list1.split()
print(LIST1)
n = int(input("Select Element Index to be printed : "))

#

if n < 0 or n >= len(LIST1):
    print("Index out of range")
else:
    print(f"{n} Indexed Element is : {LIST1[n]}")

#

custom_list2 = input(f"\nEnter List Elements with a space : ")
LIST2 =  custom_list2.split()
print(f"{LIST2}")

LIST3 = LIST1 + LIST2
print(f"\nSummation of Lists - {LIST3}")

# 

def EmptyList(LIST):
    if len(LIST) == 0:
        return "List is Empty"
    else:
        return "List is not Empty"

print(f"\n{EmptyList(LIST3)}")


