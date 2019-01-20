import pyowm

def filterOnWeather(location, recommendedPlaces):

    # Step 0: Copy information to local variables
    lat = location['lat']
    lng = location['lng']

    # Step 1: Connect to Weather API
    owm = pyowm.OWM('d226204f5696750985009365ee253eb2')
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
    isBadWeather = evaluateWeatherCode(weather_code) # flag if weather does recommend activity outside

    # Step 3: Apply filter if badWeather
    if isBadWeather:
        noRecommendationPrev = len(recommendedPlaces.index)
        filtered_recommendedPlaces = recommendedPlaces[(recommendedPlaces.is_building == True)]
        noRecommendationsAfter = len(filtered_recommendedPlaces.index)
        print("Weather filtering: Weather is bad => filter ("+str(noRecommendationPrev)+"->"+str(noRecommendationsAfter)+")")
    else:
        print("Weather filtering: Weather is good => no filter")
        filtered_recommendedPlaces = recommendedPlaces

    return filtered_recommendedPlaces

def evaluateWeatherCode(weather_code):

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