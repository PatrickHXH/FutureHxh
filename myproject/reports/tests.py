import datetime
time ="2022-7-12"
a = time.split("-")
print()
first = datetime.date(int(a[0]),int(a[1]),int(a[2]))
now = datetime.datetime.now()
offset = datetime.timedelta(days=-90)
date = (now+offset).strftime("%Y-%m-%d")
a = date.split("-")
second = datetime.date(int(a[0]),int(a[1]),int(a[2]))

if first < second:
    print("超出90天")
else:
    print("小于等于90天")