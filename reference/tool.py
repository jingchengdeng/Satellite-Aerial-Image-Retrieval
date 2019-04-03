#!/usr/bin/python

import math, mpmath, json
from urllib import request, error

EARTH_RADIUS = 6378137

#Spherical Mercator projection to x and y
def toSphMercator(lat, lon):
    y = math.log(math.tan(math.radians(lat)) + mpmath.sec(math.radians(lat)))* EARTH_RADIUS
    x = math.radians(lon) * EARTH_RADIUS
    return y,x

#Convert x and y to longitude and latitude (degree)
def toLatLon(y, x):
    lat = math.degrees(math.atan(mpmath.sinh(y/EARTH_RADIUS)))
    lon = math.degrees(x/EARTH_RADIUS)
    return lat,lon

#Convert to tile coordinatesx
def toTileCoords(lat, lon, zoom):
    xAxisLen = math.pi * EARTH_RADIUS * 2
    tilesPerRow = math.pow(2, zoom)
    
    (lat,lon) = toSphMercator(lat,lon)
    
    normalizedLat = xAxisLen/2 - lat
    normalizedLon = xAxisLen/2 + lon

    y = normalizedLat * tilesPerRow/ xAxisLen
    x = normalizedLon * tilesPerRow/ xAxisLen
    return (int(math.floor(y)),int(math.floor(x)))


def fetchJson(url):
    try:
        return json.loads(
            request.urlopen(url).read()
        )
    except error.URLError as e:
        if hasattr(e, "reason"):
            logging.error("Failed to reach the server: %s" % e.reason)
        elif hasattr(e, "code"):
            logging.error("Server error: %s" % e.code)
        sys.exit(-1)
    except:
        logging.error("JSON error")

