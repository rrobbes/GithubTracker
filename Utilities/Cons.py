"""
Cons file.
File for global constants.
"""
import datetime
import json
__author__ = "Michel Llorens"
__copyright__ = "Copyright 2016"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "mllorens@dcc.uchile.cl"

weeks = 20

config = json.load(open('config.json'))
root = config['root']

sinceData = datetime.datetime.now() - datetime.timedelta(weeks=weeks)
