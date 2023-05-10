import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.gbis.go.kr/gbis2014/schBusAPI.action"
headers = {
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68"
}
data = {
    'cmd': 'searchRealBusStationJson',
    'stationId': '228001737',
    'routeId': '241428004'
}

response = requests.post(URL, headers=headers, data=data)

if response.status_code == 200:
    json_data = response.json()
    with open('./response.json', 'w') as f:
        f.write(response.text)

else:
    print(response.content)
