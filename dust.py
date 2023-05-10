# 미세먼지, 초미세먼지

from datetime import datetime
import requests

now = datetime.now()

key = "xRK3zZCK6F6hMc3f3qqv5drNygw4XHJ1ZCtPgokw4Gb0AmeW8QcQqW7z1j8VQwr89EwYdj+dCAFpP6wtHuo7BA=="

params = {
    'serviceKey': key,
    'returnType': "json",
    'numOfRows': 1,
    'pageNo': 1,
    'stationName': '기흥',
    'dataTerm': 'DAILY',
    'ver': 1.0
}

print(params)

URL = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'

res = requests.get(URL, params=params)
print(res.json())
