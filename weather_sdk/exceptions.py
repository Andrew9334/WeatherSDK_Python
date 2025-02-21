class WeatherSDKException(Exception):
    """Базовое исключение SDK для обработки общих ошибок."""
    pass

class WeatherAPIException(WeatherSDKException):
    """Исключение, которое возникает, если API OpenWeather возвращает ошибку."""
    def __init__(self, message="Ошибка API OpenWeather"):
        self.message = message
        super().__init__(self.message)

class InvalidCityException(WeatherSDKException):
    """Исключение, которое возникает, если город не найден в OpenWeather."""
    def __init__(self, city_name, message="Город не найден"):
        self.city_name = city_name
        self.message = f"{message}: {self.city_name}"
        super().__init__(self.message)

class NetworkErrorException(WeatherSDKException):
    """Исключение для обработки сетевых ошибок."""
    def __init__(self, message="Ошибка сети. Проверьте подключение к Интернету"):
        self.message = message
        super().__init__(self.message)

class DataNotUpdatedException(WeatherSDKException):
    """Исключение, если данные не были обновлены в течение ожидаемого времени."""
    def __init__(self, message="Данные о погоде не обновлялись в течение 10 минут"):
        self.message = message
        super().__init__(self.message)
