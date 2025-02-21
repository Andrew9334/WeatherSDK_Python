import requests
import time
import threading
from .exceptions import WeatherSDKException

class WeatherSDK:
    def __init__(self, api_key, mode='on-demand'):
        """
        Инициализация SDK.

        :param api_key: Ключ API для OpenWeather.
        :param mode: Режим работы SDK ('on-demand' или 'polling').
        """
        self.api_key = api_key
        self.mode = mode
        self.weather_data = {}  # Хранение данных о погоде для городов
        self.lock = threading.Lock()  # Для синхронизации доступа к данным в многозадачной среде

    def _get_weather_data(self, city_name):
        """
        Получение данных о погоде для указанного города.

        :param city_name: Название города.
        :return: Данные о погоде в формате JSON.
        """
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api_key}&units=metric'
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверка успешности запроса
            data = response.json()
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
            raise WeatherSDKException(f"Ошибка при получении данных для города {city_name}: {e}")

    def get_weather(self, city_name):
        """
        Получение данных о погоде для города, с кешированием результатов.

        :param city_name: Название города.
        :return: Данные о погоде.
        """
        with self.lock:
            # Проверяем, есть ли данные в кеше и актуальны ли они
            if city_name in self.weather_data:
                last_update = self.weather_data[city_name]['datetime']
                if time.time() - last_update < 600:  # Данные считаются актуальными в течение 10 минут
                    return self.weather_data[city_name]

            # Если данных нет или они устарели, получаем новые
            weather = self._get_weather_data(city_name)
            self.weather_data[city_name] = weather
            # Храним данные не более чем для 10 городов
            if len(self.weather_data) > 10:
                self.weather_data.pop(next(iter(self.weather_data)))  # Удаляем самый старый элемент
            return weather

    def delete_weather_data(self, city_name):
        """
        Удаление данных о погоде для указанного города.

        :param city_name: Название города.
        """
        with self.lock:
            if city_name in self.weather_data:
                del self.weather_data[city_name]

    def polling_update(self):
        """
        Режим polling обновляет погоду для всех сохранённых городов.
        Работает только в режиме polling.
        """
        while self.mode == 'polling':
            with self.lock:
                for city_name in list(self.weather_data.keys()):
                    weather = self._get_weather_data(city_name)
                    self.weather_data[city_name] = weather
            time.sleep(600)  # Обновляем данные каждые 10 минут

    def start_polling(self):
        """
        Запуск режима polling в отдельном потоке.
        """
        if self.mode == 'polling':
            polling_thread = threading.Thread(target=self.polling_update, daemon=True)
            polling_thread.start()
