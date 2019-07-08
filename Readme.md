## libgeohash

A python library for interacting with [geohashes](https://en.wikipedia.org/wiki/Geohash). 

### Usage

```python
>>> import libgeohash as gh

>>> gh.encode(57.64911, 10.40744, precision = 10)
'u4pruydqqv'

>>> gh.decode('u4pruydqqv', errors = True)
(57.64911264181137, 10.407437682151794, 2.682209014892578e-06, 5.364418029785156e-06)

>>> gh.neighbors('u4pruydqqv')
{'ne': 'u4pruydqrn', 'e': 'u4pruydqrj', 'n': 'u4pruydqqy', 'se': 'u4pruydqrh', 'w': 'u4pruydqqt', 'sw': 'u4pruydqqs', 'nw': 'u4pruydqqw', 's': 'u4pruydqqu'}

# Returns dimensions of the bounding box referred by the geohash in meters. (width, height)
>>> gh.dimensions('u4pruyd')
(152.9, 152.4)

# Returns the great circle distance (Haversine) between two geohashes or coordinates. 
>>> gh.distance('u4pruyd', 'u4pruyg')
173.19066702376304

```

- For more functions and their usage, please refer to the doc strings. 
