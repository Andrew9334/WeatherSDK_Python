class WeatherSDKException(Exception):
    pass

class WeatherAPIException(WeatherSDKException):
    def __init__(self, message="Ошибка API OpenWeather"):
        self.message = message
        super().__init__(self.message)

class InvalidCityException(WeatherSDKException):
    def __init__(self, city_name, message="Город не найден"):
        self.city_name = city_name
        self.message = f"{message}: {self.city_name}"
        super().__init__(self.message)

class NetworkErrorException(WeatherSDKException):
    def __init__(self, message="Ошибка сети. Проверьте подключение к Интернету"):
        self.message = message
        super().__init__(self.message)

class DataNotUpdatedException(WeatherSDKException):
    def __init__(self, message="Данные о погоде не обновлялись в течение 10 минут"):
        self.message = message
        super().__init__(self.message)
