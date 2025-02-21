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

# Инициализация SDK с вашим API-ключом
sdk = WeatherSDK(api_key="your_openweather_api_key", mode='on-demand')

