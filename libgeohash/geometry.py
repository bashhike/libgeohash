from .geohash_base import encode, bbox, expand
from .distance_metrics import distance, dimensions

from math import sqrt
from shapely.geometry import Polygon
from shapely.ops import unary_union	

# Note: (lat, lon) are essentially in the (y, x) format in the cartesian plane.
# shapely works with/assumes coordinates in (x,y) format so need to take care of that. 

def diagonal(a):
	"""
	Returns the length of a diagonal of a rectangle, 
	given a tuple containing length of the sides. 
	"""
	return sqrt(a[0]**2 + a[1]**2)


def geohash_to_polygon(ghashes):
	"""
	Converts a list of geohashes to a shapely polygon.
	"""
	polygons = []
	for ghash in ghashes:
		# bbox returns a tuple of lat, lon pairs which essentially is (y, x) in cartesian plane. 
		# Converting it into (x, y) before passing to shapely. 
		bounds = [ele[::-1] for ele in bbox(ghash, coordinates = True)]
		polygons.append(Polygon(bounds)) 
	
	# No need to do unary_union operation if there's only one geohash. 
	if len(ghashes) == 1:
		return polygons[0]
	else:
		return unary_union(polygons)


def polygon_to_geohash(poly, precision, inner = False):
	"""
	Approximate a shapely polygon using a list of geohashes. 
	
	precision: Defines the size/precision of geohashes used to approximate the polygon.
	inner: Dictates whether only the geohashes inside the polygon are to considered or 
	the ones intersecting it are too. 
	"""

	centroid = poly.centroid
	envelope = poly.envelope
	
	# Bounds returns the bounds for bottom left and top right corners of the bbox. 
	bounds = poly.bounds
	diagonal_dist = distance((bounds[1], bounds[0]), (bounds[3], bounds[2]), coordinates = True)

	center_ghash = encode(centroid.y, centroid.x, precision)

	# Adding 2, 1 for ceiling and 1 extra just in case 
	# (Should take care of cases when ghash and the actual boundary just graze through)
	num_expansions = int(diagonal_dist//diagonal(dimensions(center_ghash))) + 2

	
	polygon_bbox_ghashes = expand(center_ghash, n = num_expansions)

	# Sets to collect the geohashes outside and inside the polygon. 
	outside = set()
	inside = set()

	for ghash in polygon_bbox_ghashes:
		ghash_poly = geohash_to_polygon([ghash])
		check_envelope = envelope.contains(ghash_poly) if inner else envelope.intersects(ghash_poly)

		if check_envelope:
			if inner:
				if poly.contains(ghash_poly):
					inside.add(ghash)
				else:
					outside.add(ghash)
			else:
				if poly.intersects(ghash_poly):
					inside.add(ghash)
				else:
					outside.add(ghash)
		else:
			outside.add(ghash)

	return list(inside)