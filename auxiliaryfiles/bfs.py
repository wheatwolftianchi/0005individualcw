import math
earthRadius = 3958.8
latself = 51.4857358
latstation = 51.5031466
lonself = -0.1238299
lonstation = -0.1132592

EARTH_REDIUS = 6378.137

def rad(d):
    return d * math.pi / 180.0

def getDistance(lat1, lng1, lat2, lng2):
    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1 - radLat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b/2), 2)))
    s = s * EARTH_REDIUS
    return s

C = math.sin(latstation)*math.sin(latself) + math.cos(latstation)*math.cos(latself)*math.cos(lonstation - lonself)
print(getDistance(latself,lonself,latstation,lonstation))