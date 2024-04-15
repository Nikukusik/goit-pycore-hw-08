import datetime as dt
from datetime import datetime as dtdt
def get_upcoming_birthdays(users):
    tdate = dtdt.today().date()
    birthdays = []
    for user in users:
        bdate = user["birthday"]
        bdate = dtdt.strptime(bdate, "%d.%m.%Y").date()
        year_now = dtdt.today().year
        bdate = bdate.replace(year = year_now)
        week_day = bdate.isoweekday()
        days_between = (bdate - tdate).days
        if 0<=days_between < 7:
            if week_day < 6:
                birthdays.append({"name": user["name"], 'congratulation_date': bdate.strftime("%d.%m.%Y")})
            else:
                if (bdate+dt.timedelta(days=1)).weekday()==0:
                    birthdays.append({'name':user['name'], 'congratulation_date':(bdate+dt.timedelta(days=1)).strftime("%d.%m.%Y")})
                elif (bdate+dt.timedelta(days=2)).weekday()==0: 
                    birthdays.append({'name':user['name'], 'congratulation_date':(bdate+dt.timedelta(days=2)).strftime("%d.%m.%Y")})
    return birthdays
users = [
    {"name": "Jane Smith", "phone": "0937757425", "birthday": "13.04.2002"},
    {"name": "Jane Smitt", "phone": "0937757425", "birthday": "11.04.2003"}
]
print(get_upcoming_birthdays(users))
phone = []
