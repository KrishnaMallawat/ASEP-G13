sample_set = {1, 2, 3}
sample_list = [4, 5, 6]
for item in sample_list:
    sample_set.add(item)
print(sample_set)

#

set1 = {1, 2, 3}
set2 = {3, 4, 5}
for item in set2:
    if item in set1:
        set1.remove(item)
print(set1)

#

set_a = {1, 2, 3}
set_b = {3, 4, 5}
result = set_a ^ set_b
print(result)

#

set1 = {1, 2, 3}
set2 = {4, 5, 9}
common = bool(set1.intersection(set2))
print(common)
#

set1 = {1, 2, 3}
set2 = {3, 4, 5}
set1 = {item for item in set1 if item in set2}
print(set1)