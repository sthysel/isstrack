#! /usr/bin/env python3.4

import certifi
import requests
import time
from math import asin, cos, radians, sin, sqrt

import requests.packages.urllib3 as urllib3
urllib3.disable_warnings()

url = "https://api.wheretheiss.at/v1/satellites/25544"

# lat, long
home_pos = (45.686, -121.566)


def get_iis_position():
    #  res = requests.get(url, verify=certifi.where()).json()
    res = requests.get(url, verify=False).json()
    iss_pos = (res['latitude'], res['longitude'])
    dist = get_spherical_distance(home_pos, iss_pos)
    return dist


def get_spherical_distance(pos1, pos2, radius=6373):
    """ Returns distance on sphere between points given as (latitude, longitude) in degrees. """

    lat1 = radians(pos1[0])
    lat2 = radians(pos2[0])
    dLat = lat2 - lat1
    dLon = radians(pos2[1]) - radians(pos1[1])
    a = sin(dLat / 2.0) ** 2 + cos(lat1) * cos(lat2) * sin(dLon / 2.0) ** 2
    return 2 * asin(min(1, sqrt(a))) * radius


while True:
    print(get_iis_position())
    time.sleep(5)
