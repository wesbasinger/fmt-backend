from time import time
from datetime import datetime, timedelta, timezone


# geolocation_dict will be formed as such
# {
#     "latitude" : latitude,
#     "longitude" : longitude,
#     "timestamp" : timestamp
# }

CENTER_LATITUDE = 32.625484
CENTER_LONGITUDE = -96.763224

TOLERANCE = 0.00974111382

def check_geolocation(geolocation_dict, work_from_home=False):

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

    elif (distance_from_center > TOLERANCE) and not work_from_home:

        return {
            "error" : True,
            "message" : "Must be closer to Cedar Valley Theater."
        }

    else:

        return {
            "error": False,
            "message" : "Coordinates and timestamp verified."
        }

def make_datestamp(js_timestamp, is_JS=True):

    if is_JS:

        python_timestamp = float(js_timestamp) / 1000

    else:

        python_timestamp = js_timestamp

    dt = datetime.fromtimestamp(python_timestamp)

    utc_offset = timedelta(hours=6) #6 hours accounts for non DST

    modifed_time = dt - utc_offset

    return modifed_time.strftime('%Y-%m-%d %H:%M:%S')


def get_rounded_hours(timestamp):

    # feed this function a js timestamp

	now = time()

    # float(timestamp)/1000 changes js timestamp to python timestame
	elapsed_seconds = now - float(timestamp)/1000

	return round(elapsed_seconds / 3600, 1)
