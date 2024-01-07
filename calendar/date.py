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

#timezones    here we get timezones into date time
import pytz
leo = datetime.datetime.now(tz = pytz.UTC) 
print(leo) 
leo_pacific = leo.astimezone(pytz.timezone('US/Pacific'))
print(leo_pacific) 
pytz.all_timezones # get all time zones

for tz in pytz.all_timezones:
    print(tz)

leo_pacific.strftime('%B, %d ,%Y')

# manipualtinbg imported dates 
# note strftime for fromatting   and strptime for parsing 
dt_parse = datetime.datetime.strptime('January 06, 2024','%B  %d, %Y')
print(dt_parse)

# use maya to manipulate dates 



