from datetime import datetime
import requests

now = datetime.now()

key = "xRK3zZCK6F6hMc3f3qqv5drNygw4XHJ1ZCtPgokw4Gb0AmeW8QcQqW7z1j8VQwr89EwYdj+dCAFpP6wtHuo7BA=="

dates = {
    'year': f'{now.year}',
    'month': f'{now.month}',
    'day': f'{now.day}'
}

if len(dates['month']) < 2:
    dates['month'] = f"0{dates['month']}"

if len(dates['day']) < 2:
    dates['day'] = f"0{dates['day']}"

date = f"{dates['year']}{dates['month']}{dates['day']}"

hour = str(now.hour)
if len(hour) < 2:
    hour = f'0{hour}'

time = f"{hour}00"
location = (62, 122)

params = {
    'ServiceKey': key,
    'pageNo': 1,
    'numOfRows': 100,
    'dataType': "json",
    'base_date': date,
    'base_time': time,  # 'base_time': time,
    'nx': location[0],
    'ny': location[-1]
}

print(params)

URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

res = requests.get(URL, params=params)

with open('weather.json', 'w') as f:
    f.write(str(res.json()['response']['body']['items']['item']))
