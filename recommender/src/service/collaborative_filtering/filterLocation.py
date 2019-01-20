from math import sin, cos, sqrt, atan2, radians

def filterOnLocation(location, recommendedPlaces, acceptedDistanceInKm):

    # Step 0: Copy information to local variables
    lat = location['lat']
    lng = location['lng']
    output = []

    # Step 1: Interate through locations and calculate distance to user
    for i, place in recommendedPlaces.iterrows():
        locationPlace = {"lat": place.lat, "lng": place.long} # copy coordinates
        recommendedPlaces.loc[i,'distanceToUser'] = calcDistanceInKm(location, locationPlace)
            
    # Step 2: Select locations based on acceped distance
    filtered_recommendedPlaces = recommendedPlaces[(recommendedPlaces.distanceToUser <= acceptedDistanceInKm)]
    
    return filtered_recommendedPlaces


def calcDistanceInKm(locationUser, locationPlace):
    R = 6373.0

    lat1 = radians(locationUser['lat'])
    lon1 = radians(locationUser['lng'])
    lat2 = radians(locationPlace['lat'])
    lon2 = radians(locationPlace['lng'])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance
