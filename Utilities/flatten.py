#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import unicodecsv as csv
import string

"""
flat takes a list of dict (see reports) and output a csv with the data.
name = is the filename of the output
headerOrder = is the list of keys to use in the csv (added in the same order of the list)
data = the list of dicts.

Output example:

h1,h2,h3,h4 \n
d11,d12,d13,d14 \n
d21,d22,d23,d24 \n
....

"""
def flat(name,headerOrder,data):
    with open(name, 'w') as csvfile:
        writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_ALL, dialect='excel', encoding='utf-8') #TODO replacec None values
        writer.writerow(headerOrder)
        for row in data:
            sortedByHeaderOrder = [row[key] for key in headerOrder]
            writer.writerow(sortedByHeaderOrder)