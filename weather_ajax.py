import requests
from bs4 import BeautifulSoup
from datetime import datetime


def parse_weather_data_from_html(document):
    # 가져와야 하는 항목
    # 1. 최저/최고기온 (documents[0])
    # 2. 미세먼지, 초미세먼지 (documents[0])
    # 3. 날씨 (documents[1])

    # 1. 최저/최고기온
    minmax_temp_src = document.select('div.daily-head > span.tminmax')[0]
    min_temp = minmax_temp_src.text[minmax_temp_src.text.find(
        '최저')+2:minmax_temp_src.text.find('℃')]
    max_temp = minmax_temp_src.text[minmax_temp_src.text.find(
        '최고')+2:].rstrip('℃')

    # 2. 미세먼지, 초미세먼지
    dust_src = document.select('ul.wrap-2.air-wrap.no-underline > li')
    dust_src = list(
        map(lambda n: n.text.lstrip().rstrip(), dust_src))[0:2]
    for idx, dust in enumerate(dust_src):
        dust_src[idx] = dust[dust.find('\n')+1:dust.find('㎍')]

    # 3. 현재 온도
    # 현재 시간 기반으로 날씨 데이터 탐색
    now = datetime.now()
    if len(str(now.month)) < 2:
        data_date = f'{now.year}-0{now.month}-{now.day}'
    else:
        data_date = f'{now.year}-{now.month}-{now.day}'

    if len(str(now.hour)) < 2:
        data_time = f'0{now.hour+1}:00'
    else:
        data_time = f'{now.hour+1}:00'

    weather_src = document.find(
        'ul', {'data-date': data_date, 'data-time': data_time})
    current_temp = weather_src.select('span.hid.feel')[0]
    current_temp = current_temp.text[:current_temp.text.find('℃')]

    # 4. 날씨
    # 현재 시간 가져오기
    weather = weather_src.select('span.wic')[0].text

    result = {
        'minTemp': min_temp,
        'currentTemp': current_temp,
        'maxTemp': max_temp,
        'weather': weather,
        'microDust': dust_src[0],
        'ultraMicroDust': dust_src[1],
    }

    return result


def handler():
    URL = "https://www.weather.go.kr/w/wnuri-fct2021/main/digital-forecast.do?code=4146555500&unit=m/s&hr1=Y"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68"
    }
    document = BeautifulSoup(requests.get(
        URL, headers=headers).text, 'html.parser')
    return parse_weather_data_from_html(document)


def main():
    print(handler())


main()
