#!/usr/bin/env python3

from math import radians, cos, sin, asin, sqrt
from geohash_base import decode


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
	a = map(radians, a)
	b = map(radians, b)

	dlat = a[0] - b[0]
	dlon = a[1] - b[1]

	h = sin(dlat/2)**2 + cos(a[0]) * cos(b[0]) * sin(dlon/2)**2
	return 2 * r * asin(sqrt(h)) 