import requests
import json
from bus_info import BusInfoFactory


class GbisCrawler:
    def __init__(self):
        self.URL = "https://www.gbis.go.kr/gbis2014/schBusAPI.action"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68"
        }
        self.data = {
            'cmd': 'searchRealBusStationJson',
            'stationId': '',
            'routeId': ''
        }
        
    def crawl(self, name: str):
        bus_info = BusInfoFactory().create(name)
        if bus_info is None:
            return
        
        self.data['stationId'], self.data['routeId'] = bus_info.getIDs()
        
        response = requests.post(self.URL, headers=self.headers, data=self.data)
        return response.json()