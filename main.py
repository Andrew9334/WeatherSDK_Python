from weather_sdk.sdk import WeatherSDK

# Инициализация SDK с вашим API-ключом
sdk = WeatherSDK(api_key="36f3011ccd5f433c43123f97049603cc", mode='on-demand')

# Получение данных о погоде для города
city = "Москва"
weather_data = sdk.get_weather(city)
print(weather_data)
