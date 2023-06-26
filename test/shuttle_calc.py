from datetime import datetime


# convert from hour with minute to minute
def convert_to_minute(time: list):
    return 60*time[0] + time[1]


def get_is_running(time: list):
    if len(time) == 2 and type(time[0]) == str and type(time[1]) == str:
        first_time = list(map(lambda n: int(n.rstrip()), time[0].split(':')))
        last_time = list(map(lambda n: int(n.rstrip()), time[1].split(':')))
        now = datetime.now()
        # now = datetime(year=2023, month=5, day=25, hour=8, minute=40)
        return (convert_to_minute([now.hour, now.minute]) >= convert_to_minute([first_time[0], first_time[1]])) and (convert_to_minute([now.hour, now.minute]) <= convert_to_minute([last_time[0], last_time[1]]))
    else:
        return False   # invalid value


time = ['8:30', '20:30']
print(get_is_running(time))
