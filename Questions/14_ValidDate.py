print("Enter day:")
d = int(input())

print("Enter month:")
m = int(input())

print("Enter year:")
y = int(input())

def LeapYear(y):
    if y%4==0:
        if y%100==0:
            if y%400==0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False
    
days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

if LeapYear(y):
    days_in_month[2] = 29

if m >= 1 and m <= 12:
    if d >= 1 and d <= days_in_month[m]:
        print("Valid date")
    else:
        print("Invalid date")
else:
    print("Invalid date")


