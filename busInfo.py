class BusInfo:
    stationId = '228001737'


class BusInfo24(BusInfo):
    routeId = '241428004'

    def getIDs(self):
        return {
            'stationId': self.stationId,
            'routeId': self.routeId
        }


class BusInfo720_3(BusInfo):
    routeId = '234000068'

    def getIDs(self):
        return {
            'stationId': self.stationId,
            'routeId': self.routeId
        }
