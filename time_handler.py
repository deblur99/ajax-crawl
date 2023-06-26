from datetime import datetime
import pytz


def get_weekday(date):
    weekdays = ["MON", "TUE", "WED", "THUR", 'FRI']
    days_of_week = ["MON", "TUE", "WED", "THUR", 'FRI', "SAT", "SUN"]
    return days_of_week[date.weekday()] in weekdays


# convert from hour with minute to minute
def convert_to_minute(time: list):
    return 60*time[0] + time[1]
        

# 첫차, 막차 시간 여부
# [{hour}, {minute}] 형태
def get_is_running(time: list):
    if len(time) == 2 and type(time[0]) == str and type(time[1]) == str:
        first_time = list(map(lambda n: int(n.rstrip()), time[0].split(':')))
        last_time = list(map(lambda n: int(n.rstrip()), time[1].split(':')))
        timezone = pytz.timezone('Asia/Seoul')
        now = datetime.now(timezone)
        return (convert_to_minute([now.hour, now.minute]) >= convert_to_minute([first_time[0], first_time[1]])) and (convert_to_minute([now.hour, now.minute]) <= convert_to_minute([last_time[0], last_time[1]]))
    else:
        return False   # invalid value
    

def get_now_timestamp():
    timezone = pytz.timezone('Asia/Seoul')
    current_time = datetime.now(timezone)
    timestamp_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return timestamp_str
    