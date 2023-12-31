import  datetime
today = datetime.date.today()
print(today)

birthday = datetime.date(2000,5,14)
dayslived = (today- birthday).days
print(dayslived)

# geting days ahead
tdlta = datetime.timedelta(days=10)
print(today + tdlta)
print(today.weekday())

#getting minutes and tsec and timesonne
print(datetime.time(7,2,3,21))
#datetime.date(yr,month,dy)
#datetime.time(h,m,s,ms)
#datetime.datetime(Y, M, D, h,, m, s , ms)
hrdelta = datetime.timedelta(hours = 20)
print(datetime.datetime.now() + hrdelta)