import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz


def parse_weather_data_from_html(data: dict):
    # 가져와야 하는 항목
    # 1. 최저/최고기온
    weather_src = data['forecast_weather'][0]['weatherList']
    for region in weather_src:
        if region['name'] == '서울·경기':
            min_temp = region['minTemp']
            max_temp = region['maxTemp']

    # 2. 현재 온도, 날씨
    weather_src = data['current_weather']['weatherList']
    for region in weather_src:
        if region['name'] == '서울·경기':
            curr_temp = region['temp']
            weather = region['weather']

    # 3. 미세먼지, 초미세먼지
    dust_src = data['dust'].select('ul.wrap-2.air-wrap.no-underline > li')
    dust_src = list(
        map(lambda n: n.text.lstrip().rstrip(), dust_src))[0:2]
    for idx, dust in enumerate(dust_src):
        dust_src[idx] = dust[dust.find('\n')+1:dust.find('㎍')]

    result = {
        'minTemp': f'{min_temp}',
        'currentTemp': f'{curr_temp}',
        'maxTemp': f'{max_temp}',
        'weather': f'{weather}',
        'microDust': f'{dust_src[0]}',
        'ultraMicroDust': f'{dust_src[1]}',
    }

    return result


def handler():
    URLs = {
        'forecast_weather_url': "https://weather.kweather.co.kr/get_kweather_forecast_map",
        'current_weather_url': 'https://weather.kweather.co.kr/get_current_weather_map',
        'dust_url': "https://www.weather.go.kr/w/wnuri-fct2021/main/digital-forecast.do?code=4146555500&unit=m/s&hr1=Y"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68"
    }

    # response
    data = {
        'forecast_weather': '',
        'current_weather': '',
        'dust': ''
    }

    data['forecast_weather'] = requests.get(URLs['forecast_weather_url'],
                                            headers=headers, verify=False).json()
    data['current_weather'] = requests.get(URLs['current_weather_url'],
                                           headers=headers, verify=False).json()
    data['dust'] = BeautifulSoup(requests.get(
        URLs['dust_url'], headers=headers).text, 'html.parser')

    return parse_weather_data_from_html(data)


def lambda_handler(event, context):
    return handler()
