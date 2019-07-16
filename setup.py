from setuptools import setup, find_packages

def readme():
    with open('Readme.md') as f:
        return f.read()

setup(
  name = 'libgeohash', 
  packages = find_packages(), 
  version = '0.1.1', 
  license='MIT', 
  description = 'Python library for interacting with geohashes.', 
  long_description = readme(), 
  long_description_content_type = 'text/markdown', 
  author = 'Abhishek Pandey', 
  author_email = 'ashp.pandey916@gmail.com', 
  url = 'https://github.com/bashhike/libgeohash', 
  download_url = 'https://github.com/bashhike/libgeohash/archive/0.1.tar.gz', 
  keywords = ['geohash', 'polygon to geohash', 'shapely', 'geohashes'], 
  install_requires=['shapely'], 
  classifiers=[
    'Development Status :: 3 - Alpha', 
    'Intended Audience :: Developers',   
    'Topic :: Software Development :: Libraries :: Python Modules', 
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.4', 
    'Programming Language :: Python :: 3.5', 
    'Programming Language :: Python :: 3.6', 
  ],
)
