import requests
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

def get_api_key(file_path="API_KEY.txt"):
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading API key from file: {e}")
        return None

@require_http_methods(["GET", "POST"])
def index(request):
    api_key = get_api_key()
    if not api_key:
        return render(request, "error.html", {"message": "API key is missing or invalid."})

    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

    if request.method == "POST":
        city1 = request.POST.get('city1', None)
        city2 = request.POST.get('city2', None)

        weather_data1 = fetch_weather(city1, api_key, current_weather_url) if city1 else None
        weather_data2 = fetch_weather(city2, api_key, current_weather_url) if city2 else None

        context = {
            'weather_data1': weather_data1,
            'weather_data2': weather_data2,
        }

        return render(request, "index.html", context)

    return render(request, "index.html")

def fetch_weather(city, api_key, current_weather_url):
    try:
        print(f"Fetching weather for {city}")
        response = requests.get(current_weather_url.format(city, api_key))
        response.raise_for_status()
        weather_data_json = response.json()

        if 'coord' not in weather_data_json:
            raise ValueError(f"Invalid response from weather API: {weather_data_json}")

        weather_data = {
            "city": city,
            "temperature": round(weather_data_json['main']['temp'] - 273.15, 2),
            "description": weather_data_json['weather'][0]['description'],
            "icon": weather_data_json['weather'][0]['icon']
        }

        return weather_data

    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching weather data: {e}")
        return None
