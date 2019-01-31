import pyowm
from config import *

def filter_by_weather(location, recommended_places, use_weather, force_bad_weather):
    if force_bad_weather:
        return recommended_places[recommended_places.is_building == True]
    else:
        if use_weather:
            return filter_by_weather_api(location, recommended_places)
        else:
            return recommended_places

def filter_by_weather_api(location, recommended_places):

    # Step 0: Copy information to local variables
    lat = location['lat']
    lng = location['lng']

    # Step 1: Connect to Weather API
    # owm = pyowm.OWM(openWeatherMaps_api_key)
    owm = pyowm.OWM("9488b414d1e6b302c301939cd46806e3")
    observation_list = owm.weather_around_coords(lat, lng)
    if len(observation_list) > 0:
        # weather found for location
        observation = observation_list[0]
    else:
        print("No weather location found for the user's coordinates.")
        return None

    # Step 2: Evaluate weather information
    w = observation.get_weather()
    weather_code = w.get_weather_code()
    is_bad_weather = evaluate_weather_code(weather_code) # flag if weather does recommend activity outside

    # Step 3: Apply filter if badWeather
    if is_bad_weather:
        num_recommendations_previously = len(recommended_places.index)
        filtered_recommended_places = recommended_places[(recommended_places.is_building is True)]
        num_recommendations_after = len(filtered_recommended_places.index)
        print("Weather filtering: Weather is bad => filter ("+str(num_recommendations_previously)+"->"+str(num_recommendations_after)+")")
    else:
        print("Weather filtering: Weather is good => no filter")
        filtered_recommended_places = recommended_places

    return filtered_recommended_places

def evaluate_weather_code(weather_code):

    # all sorts of thunderstorm is classified as bad weather
    if weather_code >= 200 and weather_code <= 299:
        return True

    # all sorts of rain is classified as bad weather
    if weather_code >= 500 and weather_code <= 599:
        return True

    # all sorts of snow is classified as bad weather
    if weather_code >= 600 and weather_code <= 699:
        return True

    return False
