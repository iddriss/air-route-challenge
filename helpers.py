'''
Author
---------
Iddriss Raaj (2022)

Summary
--------
Helper functions
'''
import math


def haverSine(radius, long1, lat1, long2, lat2):
    radlat1 = math.radians(lat1)
    radlat2 = math.radians(lat2)
    avgLat = math.radians((lat2-lat1)/2)
    avgLong = math.radians((long2-long1)/2)
    h1 = (math.sin(avgLat))**2
    h2 = math.cos(radlat1) * math.cos(radlat2)*(math.sin(avgLong))**2
    h = h1+h2
    sqrtH = math.sqrt(h)
    d = 2*radius*math.asin(sqrtH)

    return d


def extractAirportID(airportList):
    IDs = []

    for airport in airportList:
        IDs.append(airport[0])
        IDs.append(airport[4])
        IDs.append(airport[5])


    return IDs