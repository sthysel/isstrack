#! /usr/bin/env python3.4

"""
International Space Station Tracker

Usage:
    %PNAME% [-l <lat,lon>] [-w] [-p <interval>] [-h] [-u <url>]

Options:
    -l <location> --location=<location>  Observation Location [default: 45.686,-121.566]
    -u <url> --url=<url>  The ISS position API URL [default: https://api.wheretheiss.at/v1/satellites/25544]
    -w --watch  Continue watching
    -p <interval> --interval=<interval>  The poll interval [default: 5]
    -h --help
"""

import certifi
import requests
import time
import docopt
from math import asin, cos, radians, sin, sqrt

import requests.packages.urllib3 as urllib3
urllib3.disable_warnings()

VERSION = "0.0.1"


def get_iis_position(url, home_pos):
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


def get_observer_location(loc):
    lat, lon = loc.split(',')
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        print("Location {} is not a valif lat,long point".format(loc))
        exit(1)

    return (lat, lon)


if __name__ == '__main__':
    doc = __doc__.replace('%PNAME%', __file__)
    args = docopt.docopt(doc, version=VERSION)
    url = args['--url']
    home_pos = get_observer_location(args['--location'])
    sleep_interval = int(args['--interval'])
    watch = args['--watch']

    print(get_iis_position(url, home_pos))
    while watch:
        time.sleep(sleep_interval)
        print(get_iis_position(url, home_pos))
