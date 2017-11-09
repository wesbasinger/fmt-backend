from time import time

# geolocation_dict will be formed as such
# {
#     "latitude" : latitude,
#     "longitude" : longitude,
#     "timestamp" : timestamp
# }

CENTER_LATITUDE = 32.6030983
CENTER_LONGITUDE = -96.865876

TOLERANCE = 0.00974111382

def check_geolocation(geolocation_dict):

    now = time()

    distance_from_center = (
        (float(geolocation_dict['latitude']) - CENTER_LATITUDE)**2 +
        (float(geolocation_dict['longitude']) - CENTER_LONGITUDE)**2)**0.5

    print("Server timestamp: ", now)
    print("geolocation timestamp: ", geolocation_dict['timestamp'])

    mod_geo_timestamp = float(geolocation_dict['timestamp'])/1000

    if ((now - mod_geo_timestamp) > 60):

        return {
            "error" : True,
            "message" : "Timestamp is not valid.  Please refresh page and try again"
        }

    elif distance_from_center > TOLERANCE:

        return {
            "error" : True,
            "message" : "Must be closer to Cedar Valley Theater."
        }

    else:

        return {
            "error": False,
            "message" : "Coordinates and timestamp verified."
        }
