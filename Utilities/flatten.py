#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import csv
import string
import os


def add_commit(p, u, cmt,header):
    # row = ['COMMIT'+cmt['time'], p, u, 'commit', cmt['url'], '', cmt['message'], '', cmt['branch'], cmt['branch_link'],   TODO CRITICO QUE HACER CON ADD Y DEL
    #        cmt['is_merge'] == 'True', int(cmt['additions']), int(cmt['deletions'])]
    row = ['COMMIT' + cmt['time'], p, u, 'commit', cmt['url'], '', cmt['message'], '', cmt['branch'],
           cmt['branch_link'],
           cmt['is_merge'] == 'True', 0, 0]
    header.append(row)

def add_comment(p, u, cmt,header):
    row = ['COMMENT'+cmt['time'], p, u, 'comment', cmt['url'], '', cmt['body'], '', '', '', '', '', '']
    header.append(row)

def add_issue(p, u, cmt,header):
    row = ['ISSUE'+cmt['time'], p, u, 'issue', cmt['url'], cmt['title'], cmt['body'], cmt['assigned'], '', '', '', '', '']
    header.append(row)

def flat(config):
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding('utf8')

    header = [
        ['time', 'project', 'user', 'type', 'url', 'title', 'body', 'assigned', 'branch', 'branch_link', 'merge', 'add',
         'del']]

    jsonfile = 'Output/output.json'
    if os.path.isfile(jsonfile):
        with open(jsonfile) as data_file:
            data = json.load(data_file)

        for project in data:
            for user in project:
                u = user['name']
                p = user['project']
                for commit in user['commits']:
                    add_commit(p, u, commit,header)
                for comment in user['comments']:
                    add_comment(p, u, comment,header)
                for bug in user['issues']:
                    add_issue(p, u, bug,header)
                print

    for r in header:
        body = r[6]
        body = string.replace(body, ',', ';')
        body = string.replace(body, '\n', '   ')
        body = string.replace(body, '\r', '   ')
        r[6] = body
        title = r[5]
        title = string.replace(title, ',', ';')
        title = string.replace(title, '\n', '   ')
        title = string.replace(title, '\r', '   ')
        r[5] = title

    with open(config["exportName"], 'w') as csvfile:
        writer = csv.writer(csvfile, quotechar='|')
        for r in header:
            writer.writerow(r)
