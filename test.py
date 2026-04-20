from datetime import date

testdate = "2026-4-2".split('-')

if date.today() > date(int(testdate[0]),int(testdate[1]),int(testdate[2])):
    print("Today is greater")
else:
    print("not greater")