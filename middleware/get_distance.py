
import math

MOSCO_COORDINATES = [37.620312, 55.729747]
x2 = MOSCO_COORDINATES[0]
y2 = MOSCO_COORDINATES[1]
R = 6373.0


def get_distance_to_mscow_ring(x1, y1):
    """calculate the distance between the input coordinates and Mosco Road"""
    # Those variables respresent the longituide and the latitude
    lat1 = math.radians(x1)
    lon1 = math.radians(y1)
    lat2 = math.radians(x2)
    lon2 = math.radians(y2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance
