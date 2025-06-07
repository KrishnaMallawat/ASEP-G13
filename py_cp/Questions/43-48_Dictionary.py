dict1 = {
    "name": "Aayush",
    "age": 18,
    "profession": "Developer"
}
dict2 = {
    "name": "Aayush",
    "age": 17,
    "city": "Nagpur",
    "profession": "Developer"
}

#

dict1["city"] = "Pune"
print("After insertion:", dict1)

del dict1["age"]
print("After deletion:", dict1)

# 

merged_dict = {**dict1, **dict2,}
print("Merged dictionary:", merged_dict)

#

merged_dict = {}

for key in dict1:
    merged_dict[key] = dict1[key]

for key in dict2:
    merged_dict[key] = dict2[key]

print("Merged dictionary:", merged_dict)