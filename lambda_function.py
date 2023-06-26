import pytz
from datetime import datetime
from gbis_crawler import GbisCrawler
from time_handler import *

# 요청해서 가져온 데이터 내부의 값은 모두 String으로
def get_bus_24_info():
    res = GbisCrawler().crawl('24')["result"]["busArrivalInfo"][0]
    
    arrivalSoon = res['stationNm1'] == '대지고등학교.전내교차로'
    
    # 첫차, 막차 시간 여부
    # [{hour}, {minute}] 형태
    is_running = get_is_running([res['firstTime'], res['lastTime']])
    
    ret_data = {
        'routeId': "24",
        'timeStamp': get_now_timestamp(),
        'firstTime': res['firstTime'],
        'lastTime': res['lastTime'],
        'predictTime1': res['predictTime1'],
        'stationNm1': res['stationNm1'],
        'predictTime2': res['predictTime2'],
        'stationNm2': res['stationNm2'],
        'isRunning': is_running,
        'arrivalSoon': arrivalSoon
    }
    
    
    return ret_data
    

def get_bus_720_3_info():
    res = GbisCrawler().crawl('720-3')["result"]["busArrivalInfo"][0]
    
    arrivalSoon = res['stationNm1'] == '대지고등학교.전내교차로'
    
    is_running = get_is_running([res['firstTime'], res['lastTime']])
    
    ret_data = {
        'routeId': "720-3",
        'timeStamp': get_now_timestamp(),
        'firstTime': res['firstTime'],
        'lastTime': res['lastTime'],
        'predictTime1': res['predictTime1'],
        'stationNm1': res['stationNm1'],
        'predictTime2': res['predictTime2'],
        'stationNm2': res['stationNm2'],
        'isRunning': is_running,
        'arrivalSoon': arrivalSoon
    }
    
    return ret_data


def get_bus_shuttle_info():
    running_times = {
        'firstTime': '8:30',
        'lastTime': '21:00'
    }
    
    min_unit = 60   # for calculating time
    
    # get current time
    timezone = pytz.timezone("Asia/Seoul")
    now = datetime.now(timezone)
    current_time = now.hour*min_unit + now.minute
    month_day = (now.month, now.day)
    
    blank = {
            'routeId': "셔틀",
            'timeStamp': get_now_timestamp(),
            'firstTime': '08:30',
            'lastTime': '20:40',
            'predictTime1': '',
            'stationNm1': '',
            'predictTime2': '',
            'stationNm2': '',
            'isRunning': False, 
            'arrivalSoon': False
        }
        
    # 운행기간 여부 조회 (1학기 기준)
    start_operate_date = (3, 2)
    end_operate_date = (6, 16)
    if month_day[0] < start_operate_date[0] or month_day[0] > end_operate_date[0]:
        return blank
    elif month_day[0] == start_operate_date[0]:
        if month_day[1] < start_operate_date[1]:
            return blank
    elif month_day[0] == end_operate_date[0]:
        if month_day[1] > end_operate_date[1]:
            return blank
    
    supplement = 2  # 셔틀버스 도착시간 근사값 보정 시간 (단위: 분)
    upcoming_time = (now.minute // 15 + 1) * 15 - now.minute - supplement
    next_time = upcoming_time + 15 - supplement
    
    first_time = list(map(lambda n: int(n.rstrip()), running_times['firstTime'].split(':')))
    last_time = list(map(lambda n: int(n.rstrip()), running_times['lastTime'].split(':')))
    
    if get_weekday(now):
        is_running = get_is_running([running_times['firstTime'], running_times['lastTime']])
    else:
        is_running = False
    
    if is_running:
        # 곧도착 기준 시간
        if upcoming_time <= 3:
            arrivalSoon = True
        else:
            arrivalSoon = False
        
        ret_data = {
            'routeId': "셔틀",
            'timeStamp': get_now_timestamp(),
            'firstTime': '08:30',
            'lastTime': '20:40',
            'predictTime1': f'{upcoming_time}',
            'stationNm1': '',
            'predictTime2': f'{next_time}',
            'stationNm2': '',
            'isRunning': get_is_running([running_times['firstTime'], running_times['lastTime']]), 
            'arrivalSoon': arrivalSoon
        }
    else:
        ret_data = {
            'routeId': "셔틀",
            'timeStamp': get_now_timestamp(),
            'firstTime': '08:30',
            'lastTime': '20:40',
            'predictTime1': '-1',
            'stationNm1': '도착 정보 없음',
            'predictTime2': '-1',
            'stationNm2': '도착 정보 없음',
            'isRunning': False,
            'arrivalSoon': False
        }
    
    return ret_data
    

def lambda_handler(event, context):
    # 노선별로 도착정보 가져온 뒤 응답값 전송
    # 버스 도착하기까지 남은 시간은 초 단위로 한다.
    # 도착 예정 없는 노선의 남은 시간은 -1초로 한다.
    
    match event['bus']:
        case '24':
            return get_bus_24_info()
                
        case '720-3':
            return get_bus_720_3_info()
        
        case 'shuttle':
            return get_bus_shuttle_info()
        
        case _:
            return f'요청값이 올바르지 않습니다. {event}'