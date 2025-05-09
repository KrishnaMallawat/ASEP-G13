print("Enter first time (h m s):")
h1 = int(input())
m1 = int(input())
s1 = int(input())

print("Enter second time (h m s):")
h2 = int(input())
m2 = int(input())
s2 = int(input())

time1 = h1 * 3600 + m1 * 60 + s1
time2 = h2 * 3600 + m2 * 60 + s2

diff = time2 - time1

print("Difference in seconds:", diff)
