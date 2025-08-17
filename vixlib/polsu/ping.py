class PlayerPing:
    def __init__(self, polsu_data: dict, uuid: str) -> None:
        self._uuid = uuid
        self._polsu_data = polsu_data

        self.data: dict = self._polsu_data.get("data", {}).get("stats", {})

        self.average_ping = self.__get_average_ping()

    
    def __get_average_ping(self):
        average = self.data.get("avg", 0)

        return round(average)
