hour = int(input("Enter the hour: "))
minute = int(input("Enter the minute: "))
second = int(input("Enter the second: "))
if hour < 0 or hour > 23 or minute < 0 or minute > 59 or second < 0 or second > 59:
    print("Invalid time")   

else:
    hour_arc = hour * 30
    minute_arc = minute * 0.5

arc = float(hour_arc + minute_arc)
print(f"The angle travelled by hour hand is {arc} degrees")
