#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tinyurl
import csv

result = []
cache = {}

def shorten(url):
	if url in cache:
		return cache[url]
	else:
		short = tinyurl.create_one(url)
		cache[url] = short
		return short


with open('/Users/rr/Dropbox/cc4401/GithubTracker/out1000.csv') as data_file: 
	reader = csv.reader(data_file, quotechar='|')
	i = 0
	for line in reader:
		if i:
			url = line[4]
			line[4] = shorten(url)
			print '.'
			if line[3] == 'commit':
				urlwords = url.split('/')
				the_hash = urlwords[-1]
				line.append(the_hash)
				branch = line[8]
				branchlink = line[9]
				line[9] = shorten(branchlink)
				repo = urlwords[4]
				line[8] = repo + '/' + branch
			else:
				line.append("")
		else:
			line.append('hash')
		result.append(line)
		i += 1

with open('out_final_maybe.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, quotechar='|')
	for r in result:
		writer.writerow(r)
