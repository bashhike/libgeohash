#!/usr/bin/env python3

from math import radians, cos, sin, asin, sqrt
from .geohash_base import decode, bbox

# Cell dimensions in meters at the equator based on length of geohash.
_cell_dimensions = {
	1: (5009400, 4992600), 
	2: (1252300, 624100), 
	3: (156500, 156000), 
	4: (39100, 19500), 
	5: (4900, 4900), 
	6: (1200, 609.4), 
	7: (152.9, 152.4), 
	8: (38.2, 19), 
	9: (4.8, 4.8), 
	10: (1.2, 0.595), 
	11: (0.149, 0.149), 
	12: (0.037, 0.019)
}

def distance(a, b, coordinates = False):
	"""
	Function to calculate the distance between a pair of geohashes or coordinates. 
	Makes use of the haversine distance formula in order to calculate the distances. 
	"""
	if coordinates:
		return haversine_dist(a, b)
	else:
		return haversine_dist(decode(a), decode(b))


def haversine_dist(a, b):
	"""
	Function to calculate the haversine distance between two coordinates. 
	a, b are tuples containing lat,lon pairs. 
	"""
	# Mean radius of earth in m.
	r = 6371008.8

	# Convert the coordinates into radians. 
	a = (radians(a[0]), radians(a[1]))
	b = (radians(b[0]), radians(b[1]))

	dlat = a[0] - b[0]
	dlon = a[1] - b[1]

	h = sin(dlat/2)**2 + cos(a[0]) * cos(b[0]) * sin(dlon/2)**2
	return 2 * r * asin(sqrt(h)) 


def dimensions(ghash, actual = False):
	"""
	Returns the dimensions of the rectangle denoted by the geohash
	as a tuple (width, height). The unit is meters.

	actual: When True, returns  the actual size of the bounding box created 
	by the geohash as opposed to the metric based upon geohash length. 
	"""
	if actual:
		bounds = bbox(ghash)
		if abs(bounds['s']) < abs(bounds['n']):
			width = distance((bounds['s'], bounds['w']), (bounds['s'], bounds['e']), coordinates = True)
		else:
			width = distance((bounds['n'], bounds['w']), (bounds['n'], bounds['e']), coordinates = True)
		height = distance((bounds['s'], bounds['w']), (bounds['n'], bounds['w']), coordinates = True)
		return (width, height)
	else:
		return _cell_dimensions[len(ghash)]