import requests
from bs4 import BeautifulSoup
from datetime import datetime


def parse_weather_data_from_html(documents):
    # 가져와야 하는 항목
    # 1. 최저/최고기온 (documents[0])
    # 2. 미세먼지, 초미세먼지 (documents[0])
    # 3. 날씨 (documents[1])
    soup = BeautifulSoup(documents[0], features='html.parser')

    # 1. 최저/최고기온
    temp_src = soup.select('span.minmax')[0]
    temp_src = temp_src.text.lstrip('최저').split('최고')

    # 2. 미세먼지, 초미세먼지
    dust_src = soup.select('ul.wrap-2.air-wrap.no-underline > li')
    dust_src = list(
        map(lambda n: n.text.lstrip().rstrip(), dust_src))[0:2]
    for idx, dust in enumerate(dust_src):
        dust_src[idx] = dust[dust.find('\n')+1:dust.find('㎍')]

    # 3. 날씨
    soup = BeautifulSoup(documents[1], features='html.parser')

    # 현재 시간 가져오가
    now = datetime.now()
    if len(str(now.month)) < 2:
        data_date = f'{now.year}-0{now.month}-{now.day}'
    else:
        data_date = f'{now.year}-{now.month}-{now.day}'
    data_time = f'{now.hour+1}:00'

    # 현재 시간 기반으로 날씨 데이터 탐색
    weather_src = soup.find(
        'ul', {'data-date': data_date, 'data-time': data_time})

    weather_start_idx = weather_src.text.find('날씨:')
    weather_end_idx = weather_src.text.find('기온')

    current_temp = weather_src.select('span.hid.feel')[0]
    current_temp = current_temp.text[:current_temp.text.find('℃')]

    weather = {
        'minTemp': temp_src[0].rstrip('℃'),
        'currentTemp': current_temp,
        'maxTemp': temp_src[1].rstrip('℃'),
        'weather': weather_src.text[weather_start_idx+4:weather_end_idx].rstrip(),
        'microDust': dust_src[0],
        'ultraMicroDust': dust_src[1],
    }

    return weather


def handler():
    URLs = [
        "https://www.weather.go.kr/w/wnuri-fct2021/main/current-weather.do?code=4146555500&unit=m/s&aws=N",
        "https://www.weather.go.kr/w/wnuri-fct2021/main/digital-forecast.do?code=4146555500&unit=m/s&hr1=Y"
    ]
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68"
    }

    documents = []

    for idx, URL in enumerate(URLs):
        response = requests.get(URL, headers=headers)
        if response.status_code == 200:
            try:
                json_data = response.json()
                with open(f'./response{idx+1}.json', 'w') as f:
                    f.write(json_data)
            except requests.exceptions.JSONDecodeError:
                documents.append(response.text)
                if idx == len(URLs) - 1:
                    return parse_weather_data_from_html(documents)

        else:
            return response.content


def main():
    print(handler())


main()
