import datetime
from gbis_crawler import GbisCrawler

# 요청해서 가져온 데이터 내부의 값은 모두 String으로
def get_bus_24_info():
    res = GbisCrawler().crawl('24')["result"]["busArrivalInfo"][0]
    
    ret_data = {
        'firstTime': res['firstTime'],
        'lastTime': res['lastTime'],
        'predictTime1': res['predictTime1'],
        'stationNm1': res['stationNm1'],
        'predictTime2': res['predictTime2'],
        'stationNm2': res['stationNm2']
    }
    
    
    return ret_data
    

def get_bus_720_3_info():
    res = GbisCrawler().crawl('720-3')["result"]["busArrivalInfo"][0]
    
    ret_data = {
        'firstTime': res['firstTime'],
        'lastTime': res['lastTime'],
        'predictTime1': res['predictTime1'],
        'stationNm1': res['stationNm1'],
        'predictTime2': res['predictTime2'],
        'stationNm2': res['stationNm2']
    }
    
    return ret_data


def get_bus_shuttle_info():
    local_time = 9  # for supporting GMT+9:00
    min_unit = 60   # for calculating time
    
    # 현재 시간 계산
    # GMT+0 기준으로 현재 시간을 계산함에 유의해야 한다.
    now = datetime.datetime.now()
    current_time = (now.hour+local_time)*min_unit + now.minute
    
    # 분 단위로 환산
    firstTimeInMinute = 8*min_unit + 30
    lastTimeInMinute = 20*min_unit + 40
    
    if current_time >= firstTimeInMinute and current_time <= lastTimeInMinute:
        ret_data = {
            'firstTime': '08:30',
            'lastTime': '20:40',
            'predictTime1': f'{10 - current_time % 10}',
            'stationNm1': '',
            'predictTime2': f'{10 + 10 - current_time % 10}',
            'stationNm2': ''
        }
    else:
        ret_data = {
            'firstTime': '08:30',
            'lastTime': '20:40',
            'predictTime1': '-1',
            'stationNm1': '도착 정보 없음',
            'predictTime2': '-1',
            'stationNm2': '도착 정보 없음',
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