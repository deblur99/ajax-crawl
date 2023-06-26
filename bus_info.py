class BusInfo:
    def __init__(self):
        pass


class BusInfo24(BusInfo):
    def __init__(self):
        self.stationId = '228001737'
        self.routeId = '241428004'

    def getIDs(self):
        return self.stationId, self.routeId


class BusInfo720_3(BusInfo):
    def __init__(self):
        self.stationId = '228001737'
        self.routeId = '234000068'

    def getIDs(self):
        return self.stationId, self.routeId
        

class BusInfoFactory:
    def __init__(self):
        self.bus_list = ['24', '720-3']
    
    def create(self, name: str) -> BusInfo:
        if name not in self.bus_list:
            return None
        
        match name:
            case '24':
                return BusInfo24()
            
            case '720-3':
                return BusInfo720_3()
        