import random
# INTEGER
random_INT = random.randint(1, 60)
print(random_INT)

# FLOAT
random_FLOAT = random.random()
print(random_FLOAT)

# RANDOM CHOICE
random_CHOICE = random.choice([1, 2, 3, 4, 5])
print(random_CHOICE)

# SHUFFLE   
list = [1, 2, 3, 4, 5]
print("unshuffled" , list)
random.shuffle(list)
print("shuffled" , list)