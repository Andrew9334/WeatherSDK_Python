import pytest
from weather_sdk.sdk import WeatherSDK
from weather_sdk.exceptions import WeatherSDKException

def test_get_weather():
    sdk = WeatherSDK(api_key="36f3011ccd5f433c43123f97049603cc", mode='on-demand')
    weather = sdk.get_weather("Москва")
    assert weather['name'] == 'Moscow'  # Ожидаем английское название города

def test_get_weather_invalid_city():
    sdk = WeatherSDK(api_key="36f3011ccd5f433c43123f97049603cc", mode='on-demand')
    with pytest.raises(WeatherSDKException):
        sdk.get_weather("InvalidCity")
