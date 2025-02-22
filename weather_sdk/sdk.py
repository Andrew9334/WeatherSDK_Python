import requests
import time
import threading
from .exceptions import WeatherSDKException, NetworkErrorException, WeatherAPIException

class WeatherSDK:
    _instances = {}

    def __new__(cls, api_key, mode='on-demand'):
        if api_key in cls._instances:
            raise WeatherSDKException(f"Экземпляр SDK с таким API ключом уже существует: {api_key}")
        
        instance = super(WeatherSDK, cls).__new__(cls)
        cls._instances[api_key] = instance
        return instance

    def __init__(self, api_key, mode='on-demand'):
        if not hasattr(self, 'initialized'):
            self.api_key = api_key
            self.mode = mode
            self.weather_data = {}
            self.lock = threading.Lock()
            self.initialized = True

    def _get_weather_data(self, city_name):
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api_key}&units=metric'
        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            if "weather" not in data:
                raise WeatherAPIException(f"Ошибка API OpenWeather: {data.get('message', 'Неизвестная ошибка')}")

            return {
                'weather': data['weather'][0],
                'temperature': {'temp': data['main']['temp'], 'feels_like': data['main']['feels_like']},
                'visibility': data['visibility'],
                'wind': {'speed': data['wind']['speed']},
                'datetime': data['dt'],
                'sys': data['sys'],
                'timezone': data['timezone'],
                'name': data['name'],
            }
        except requests.exceptions.RequestException as e:
            raise NetworkErrorException(f"Ошибка сети: {e}")
        except WeatherAPIException as e:
            raise e
        except Exception as e:
            raise WeatherAPIException(f"Ошибка при получении данных для города {city_name}: {e}")

    def get_weather(self, city_name):
        with self.lock:
            if city_name in self.weather_data:
                last_update = self.weather_data[city_name]['datetime']
                if time.time() - last_update < 600:
                    return self.weather_data[city_name]

            weather = self._get_weather_data(city_name)
            self.weather_data[city_name] = weather

            if len(self.weather_data) > 10:
                self.weather_data.pop(next(iter(self.weather_data)))
            return weather

    def delete_weather_data(self, city_name):
        with self.lock:
            if city_name in self.weather_data:
                del self.weather_data[city_name]
            else:
                raise WeatherSDKException(f"Данные о погоде для города {city_name} не найдены.")

    def polling_update(self):
        while self.mode == 'polling':
            with self.lock:
                for city_name in list(self.weather_data.keys()):
                    weather = self._get_weather_data(city_name)
                    self.weather_data[city_name] = weather
            time.sleep(600)

    def start_polling(self):
        if self.mode == 'polling':
            polling_thread = threading.Thread(target=self.polling_update, daemon=True)
            polling_thread.start()

    @classmethod
    def delete_instance(cls, api_key):
        if api_key in cls._instances:
            del cls._instances[api_key]
        else:
            raise WeatherSDKException(f"SDK с ключом {api_key} не существует.")
