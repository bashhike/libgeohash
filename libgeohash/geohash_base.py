#!/usr/bin/env python3

# The 32 bit character set to be used in the geohash. 
_base32 = '0123456789bcdefghjkmnpqrstuvwxyz'

# Mapping of each base32 character to an integer. 
_basemap = {}
for i in range(32):
	_basemap[_base32[i]] = i



def decode(ghash, errors = False):
	"""
	Function to decode a geohash to lat, lon values. 
	errors: Flag to include or exclude error parameters from the return value. 
	"""
	lat_range = (-90.0, 90.0)
	lon_range = (-180.0, 180.0)
	index = 0

	for c in ghash:
		# The binary representation of the character. 
		c2i = _basemap[c]
		
		# Mask is used in order to extract the bit information from the integer. 
		for mask in [16, 8, 4, 2, 1]:
			if index%2:
				# Latitude when index is odd. 
				if mask & c2i:
					# 1 at the position of mask 
					lat_range = ((lat_range[0] + lat_range[1])/ 2, lat_range[1])
				else:
					lat_range = (lat_range[0], (lat_range[0] + lat_range[1])/ 2)
			else:
				# Longitude when index is even
				if mask & c2i:
					# 1 at the position of mask 
					lon_range = ((lon_range[0] + lon_range[1])/ 2, lon_range[1])
				else:
					lon_range = (lon_range[0], (lon_range[0] + lon_range[1])/ 2)
			index += 1

	if errors:
		return (
			(lat_range[0] + lat_range[1])/ 2, 
			(lon_range[0] + lon_range[1])/ 2, 
			(lat_range[1] - lat_range[0])/ 2, 
			(lon_range[1] - lon_range[0])/ 2)
	else:
		return ((lat_range[0] + lat_range[1])/ 2, (lon_range[0] + lon_range[1])/ 2)


def encode(lat, lon, precision = 12):
	"""
	Function to encode a given lat, lon pair to a geohash. 
	"""
	lat_range = (-90.0, 90.0)
	lon_range = (-180.0, 180.0)
	index = 0
	ghash = ''

	for i in range(precision):
		ch = 0
		for mask in [16, 8, 4, 2, 1]:
			if index%2:
				# Latitude in case of odd index. 
				mid_pt = (lat_range[0] + lat_range[1])/ 2
				if lat >= mid_pt:
					ch |= mask 
					lat_range = (mid_pt, lat_range[1])
				else:
					lat_range = (lat_range[0], mid_pt)
			else:
				# Longitude in case of even index.
				mid_pt = (lon_range[0] + lon_range[1])/ 2
				if lon >= mid_pt:
					ch |= mask 
					lon_range = (mid_pt, lon_range[1])
				else:
					lon_range = (lon_range[0], mid_pt)
			index += 1
		ghash += _base32[ch]
	return ghash


def bbox(ghash, coordinates = False):
	"""
	Returns the bounding box of the geohash. 
	coordinates: When this parameter is set True, Returns the bounding box as a 
	list of coordinates instead of a dictionary.
	"""
	lat, lon, lat_err, lon_err = decode(ghash, errors = True)
	bounds = {
	'n': lat + lat_err, 
	's': lat - lat_err, 
	'w': lon - lon_err, 
	'e': lon + lon_err
	}

	if coordinates:
		return [
		(bounds['s'], bounds['w']), 
		(bounds['n'], bounds['w']), 
		(bounds['n'], bounds['e']), 
		(bounds['s'], bounds['e'])
		]
	else:
		return bounds


def adjacent(ghash, direction):
	"""
	Return an adjacent geohash in the specified direction. 
	Returns None if the movement is invalid. 
	direction: n, s, e, w

	"""

	if ghash is None:
		return None

	# Based on https://github.com/davetroy/geohash-js
	neighbour = {
	    'n': ( 'p0r21436x8zb9dcf5h7kjnmqesgutwvy', 'bc01fg45238967deuvhjyznpkmstqrwx' ),
	    's': ( '14365h7k9dcfesgujnmqp0r2twvyx8zb', '238967debc01fg45kmstqrwxuvhjyznp' ),
	    'e': ( 'bc01fg45238967deuvhjyznpkmstqrwx', 'p0r21436x8zb9dcf5h7kjnmqesgutwvy' ),
	    'w': ( '238967debc01fg45kmstqrwxuvhjyznp', '14365h7k9dcfesgujnmqp0r2twvyx8zb' ),
	}
	border = {
	    'n': ( 'prxz',     'bcfguvyz' ),
	    's': ( '028b',     '0145hjnp' ),
	    'e': ( 'bcfguvyz', 'prxz'     ),
	    'w': ( '0145hjnp', '028b'     ),
	}

	# Check for crossover from north pole to south pole
	# Return Null/None in that case. 
	if len(ghash) == 1 and ghash in border['s'][1] and direction == 's':
		return None
	if len(ghash) == 1 and ghash in border['n'][1] and direction == 'n':
		return None

	lastch = ghash[-1]
	parent = ghash[:-1]
	gtype = len(ghash)%2

	# Check for edge cases that don't share a common prefix. 
	if lastch in border[direction][gtype] and parent != '':
		parent = adjacent(parent, direction)

	if parent is None:
		return None
	return parent + _base32[neighbour[direction][gtype].index(lastch)]


def neighbors(ghash):
	"""
	Returns all the neighbors of a given geohash.
	"""

	ret = {}
	ret['n'] = adjacent(ghash, 'n')
	ret['s'] = adjacent(ghash, 's')
	ret['e'] = adjacent(ghash, 'e')
	ret['w'] = adjacent(ghash, 'w')
	
	ret['ne'] = adjacent(ret['n'], 'e')
	ret['nw'] = adjacent(ret['n'], 'w')
	ret['se'] = adjacent(ret['s'], 'e')
	ret['sw'] = adjacent(ret['s'], 'w')

	return ret
	

def expand(ghash, n = 1):
	"""
	Expand (Include the neighbors) the given geohash recursively n times. 
	Useful for proximity search. 
	"""
	
	# Find n geohashes in the n and s direction and then expand to e,w from those. 
	# Northern geohashes in the odd positions and southern in the even positions. 
	expand_list = [ghash]
	for i in range(n):
		if i == 0:
			expand_list.append(adjacent(ghash, 'n'))
			expand_list.append(adjacent(ghash, 's'))
		else:
			expand_list.append(adjacent(expand_list[-2], 'n'))
			expand_list.append(adjacent(expand_list[-2], 's'))

	# Expand towards East and West for all elements in expand_list.
	expanded_ghash = []
	for ele in expand_list:
		if ele is not None:
			expanded_ghash.append(ele)
			for i in range(n):
				if i == 0:
					expanded_ghash.append(adjacent(ele, 'e'))
					expanded_ghash.append(adjacent(ele, 'w'))
				else:
					expanded_ghash.append(adjacent(expanded_ghash[-2], 'e'))
					expanded_ghash.append(adjacent(expanded_ghash[-2], 'w'))
	return expanded_ghash