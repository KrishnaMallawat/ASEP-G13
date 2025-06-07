s = input("Enter a string:")
modified_s = ""

for i in range(len(s)):
    if i % 3 != 0:
        modified_s += s[i]

print("Modified string:", modified_s)
