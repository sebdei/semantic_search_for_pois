from math import sin, cos, sqrt, atan2, radians

def filter_by_location(location, recommended_places, accepted_distance_in_km):

    # Step 1: Interate through locations and calculate distance to user
    for i, place in recommended_places.iterrows():
        location_place = {"lat": place.lat, "lng": place.long} # copy coordinates
        recommended_places.loc[i, 'distance_to_user'] = distance_in_km(location, location_place)

    # Step 2: Select locations based on acceped distance
    filtered_recommended_places = recommended_places[(recommended_places.distance_to_user <= accepted_distance_in_km)]

    return filtered_recommended_places


def distance_in_km(location_user, location_place):
    R = 6373.0

    lat1 = radians(location_user['lat'])
    lon1 = radians(location_user['lng'])
    lat2 = radians(location_place['lat'])
    lon2 = radians(location_place['lng'])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance
