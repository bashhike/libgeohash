## libgeohash

A python library for interacting with [geohashes](https://en.wikipedia.org/wiki/Geohash).  

The library is divided into 3 modules:
- __geohash_base__: Base functions for interacting with geohashes e.g. `encode`, `decode`, `neighbors`, `bbox` etc. 
- __distance_metrics__: Distance related functions e.g. `distance`, `dimensions` etc. 
- __geometry__: Functions for conversion of a polygon to a list of geohash and vice versa. e.g. `polygon_to_geohash`, `geohash_to_polygon`. Useful for approximating geographical regions with geohashes. Makes use of [shapely](https://pypi.org/project/Shapely/) library for geometric calculations.

### Installation

Linux and Mac users can install the package via pip. 

`$ pip install libgeohash`

### Usage

```python
>>> import libgeohash as gh

>>> gh.encode(57.64911, 10.40744, precision = 10)
'u4pruydqqv'

>>> gh.decode('u4pruydqqv', errors = True)
(57.64911264181137, 10.407437682151794, 2.682209014892578e-06, 5.364418029785156e-06)

>>> gh.neighbors('u4pruydqqv')
{'ne': 'u4pruydqrn', 'e': 'u4pruydqrj', 'n': 'u4pruydqqy', 'se': 'u4pruydqrh', 
'w': 'u4pruydqqt', 'sw': 'u4pruydqqs', 'nw': 'u4pruydqqw', 's': 'u4pruydqqu'}

# Returns dimensions of the bounding box referred by the geohash in meters. (width, height)
>>> gh.dimensions('u4pruyd')
(152.9, 152.4)

# Returns the great circle distance (Haversine) between two geohashes or coordinates. 
>>> gh.distance('u4pruyd', 'u4pruyg')
173.19066702376304

```

- For more functions and their usage, please refer to the doc strings. 

### Known issues
- Fails to approximate a polygon spanning across the [International Date Line](https://en.wikipedia.org/wiki/International_Date_Line) i.e. 180/-180 longitude. Shouldn't be much of a problem since there aren't any geographical entities that actually span across it due to nature of the line itself.  

If you happen to find any other bugs, please report them in the issues section. 