# Weather SDK for OpenWeather API

Этот SDK позволяет легко взаимодействовать с OpenWeather API для получения данных о погоде для указанного города.

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/yourusername/weather-sdk.git
    cd weather-sdk
    ```

2. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

3. Установите SDK как пакет:
    ```bash
    python setup.py install
    ```

## Использование

### Инициализация SDK

Для работы с SDK вам нужно получить ключ API от OpenWeather и передать его при инициализации:

```python
from weather_sdk.sdk import WeatherSDK
```

# Инициализация SDK с вашим API-ключом
```python
sdk = WeatherSDK(api_key="your_openweather_api_key", mode='on-demand')
```

## Режимы работы
* On-demand: Погода обновляется только по запросу. Если данные уже были получены и актуальны (менее 10 минут), SDK возвращает их из кеша.
* Polling: Погода обновляется для всех сохранённых городов каждые 10 минут, чтобы обеспечить мгновенный доступ к актуальной информации.

## Обработка ошибок
SDK выбрасывает следующие исключения:

* WeatherAPIException: Ошибки API (например, неверный ключ API).
* NetworkErrorException: Проблемы с сетью.
* InvalidCityException: Город не найден в OpenWeather.

## Удаление данных
Для удаления данных о погоде для конкретного города используйте метод delete_weather_data:
```bash
sdk.delete_weather_data("Москва")
```

## Запуск тестов
Для запуска тестов используйте pytest. Перед запуском тестов убедитесь, что у вас установлен pytest и все зависимости:
```bash
pip install -r requirements.txt
pytest
```
