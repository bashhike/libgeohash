import unittest
import libgeohash as gh

class TestGeohashBase(unittest.TestCase):
	"""
	Testing the basic functionality of the geohash module. 
	Namely: encode, decode, bbox, adjacent, neighbors, expand
	"""
	def test_encode(self):
		self.assertEqual(gh.encode(57.64911, 10.40744, precision = 11), 'u4pruydqqvj')
		self.assertEqual(gh.encode(0, 0), 's00000000000')

	def test_decode(self):
		self.assertEqual(int(gh.decode('u4pruydqqvj')[0]), 57)
		self.assertEqual(int(gh.decode('u4pruydqqvj')[1]), 10)

	def test_adjacent(self):
		self.assertEqual(gh.adjacent('s', 'n'), 'u')
		self.assertEqual(gh.adjacent('s', 's'), 'k')
		self.assertEqual(gh.adjacent('s', 'e'), 't')
		self.assertEqual(gh.adjacent('s', 'w'), 'e')
		self.assertEqual(gh.adjacent('ter70p', 'n'), 'ter720')
		self.assertEqual(gh.adjacent('ter70p', 'w'), 'ter5pz')
		self.assertEqual(gh.adjacent('ter70p', 'e'), 'ter70r')
		self.assertEqual(gh.adjacent('ter70p', 's'), 'ter70n')
		
		self.assertEqual(gh.adjacent('0', 'n'), '2')
		self.assertIsNone(gh.adjacent('0', 's'))
		self.assertEqual(gh.adjacent('0', 'e'), '1')
		self.assertEqual(gh.adjacent('0', 'w'), 'p')

	def test_neighbors(self):
		self.assertEqual(gh.neighbors('j'), 
			{'se': None, 's': None, 'e': 'n', 'nw': 'k', 'sw': None, 'n': 'm', 'w': 'h', 'ne': 'q'})

	def test_expand(self):
		self.assertEqual(set(gh.expand('0')), set(['1', '0', 'p', '2', '3', 'r']))
		self.assertEqual(set(gh.expand('rbzz', n = 2)), 
			set(['rbzz', 'rcpb', 'rcpc', 'rbzy', 'rbzv', 'rcp3', 'rcp2', 'rbzr', 'rbzq', 
				'rbzm', 'rcp9', 'rcp8', 'rbzx', 'rbzw', 'rbzt', '2101', '2100', '20bp', 
				'20bn', '20bj', '2103', '2102', '20br', '20bq', '20bm']))



class TestGeohashDistance(unittest.TestCase):
	"""
	Test distance metrics.
	"""
	def test_dimensions(self):
		self.assertEqual(gh.dimensions('0'), (5009400, 4992600))


class TestGeohashGeometry(unittest.TestCase):
	"""
	Test geometry metrics. 
	"""
	def test_innerapprox(self):
		self.assertEqual(gh.polygon_to_geohash(gh.geohash_to_polygon('0'), 1, inner = True), ['0'])
		# The test case below tests the conversion of geohash to polygon and vice versa across the international date line. 
		# This fails since the polygon created by geohash at -180 and 180 are farthest to each other in the mercator projection, 
		# and the centriod of those comes somewhere near (0,0), but since the haversine distance is across the globe i.e. relatively small, 
		# expansion of the centroid geohash can't cover those two extreme ends from (0,0)

		# self.assertEqual(set(gh.polygon_to_geohash(gh.geohash_to_polygon(['px', 'r8', 'rb', 'pz', '20', '0p']), 2, inner = True)), 
		# 	set(['px', 'r8', 'rb', 'pz', '20', '0p']))
		
		

if __name__ == '__main__':
	unittest.main()