#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main class of the GithubTracker project
"""
import time
import json
from Models.GitHubRepository import GitHubRepository

__author__ = "Michel Llorens"
__copyright__ = "Copyright 2016"
__license__ = "MIT"
__version__ = "1.5.0"
__email__ = "mllorens@dcc.uchile.cl"


def clean_duplicated(dictionary):
    for key, value in dictionary.iteritems():
        no_repeat = {c['url']: c for c in value}.values()
        value = sorted(no_repeat, key=lambda k: k['time'], reverse=True)
        dictionary[key] = value

def track(config, manager):
    print "Current time " + time.strftime("%X")

    for project in config['projects']:
        print "Working on project:", project['name']
        commits_dict = {}
        issues_dict = {}
        comments_dict = {}
        events_dict = {}
        for student in project['members']:
            commits_dict[student['name']] = []
            issues_dict[student['name']] = []
            comments_dict[student['name']] = []
            events_dict[student['name']] = []
            for alias in student['aliases']:
                commits_dict[alias] = []
                issues_dict[alias] = []
                comments_dict[alias] = []
                events_dict[alias] = []
        for repository in project['repos']:
            GitHubRepository(commits_dict, issues_dict, comments_dict, events_dict, repository, manager,config)

        clean_duplicated(commits_dict)
        clean_duplicated(comments_dict)
        clean_duplicated(events_dict)

        output_file = "Output/"+project['name']+".json"
        text = "{\"project\": \""+project['name']+"\", \"content\": ["
        text += json.dumps(commits_dict)
        text += ","
        text += json.dumps(issues_dict)
        text += ","
        text += json.dumps(comments_dict)
        text += ","
        text += json.dumps(events_dict)
        text += "]}"
        fjs = open(output_file, "w+")
        fjs.write(text)
        fjs.close()
    text = ""
    # text += "var json_list = # "
    text += "["
    project_text = {
        'config': []
    }
    for project in config['projects']:
        project_name = project['name']
        project_text['config'].append(project_name)

        inner_text = "["

        file_name = "Output/"+project_name+".json"
        f_json = open(file_name, "r")
        json_data = f_json.read()
        json_data = json.loads(json_data)['content']

        for student in project['members']:
            student_text = {'project': project_name,
                            'name': student['name'],
                            'user': student['aliases'][0],
                            'commits': [],
                            'issues': [],
                            'comments': [],
                            'events': []}
            student_commits = json_data[0][student['name']]
            student_issues = json_data[1][student['name']]
            student_comments = json_data[2][student['name']]
            student_events = json_data[3][student['name']]

            for commit in student_commits:
                student_text['commits'].append(commit)
            for issue in student_issues:
                student_text['issues'].append(issue)
            for comment in student_comments:
                student_text['comments'].append(comment)
            for event in student_events:
                student_text['events'].append(event)

            for alias in student['aliases']:
                student_commits = json_data[0][alias]
                student_issues = json_data[1][alias]
                student_comments = json_data[2][alias]
                student_events = json_data[3][alias]

                for commit in student_commits:
                    student_text['commits'].append(commit)
                for issue in student_issues:
                    student_text['issues'].append(issue)
                for comment in student_comments:
                    student_text['comments'].append(comment)
                for event in student_events:
                    student_text['events'].append(event)

            student_text = json.dumps(student_text)
            inner_text += student_text
            inner_text += ","
        inner_text = inner_text[:-1] + "]"
        text += inner_text + ","
    text = text[:-1] + "]"
    #text +=;
    #project_text = json.dumps(project_text)
    #text += "\nvar projects_json = "
    #text += project_text
    #text += ";"

    # output_file = "Output/output.js"
    output_file = "Output/output.json"
    fjs = open(output_file, "w+")
    fjs.write(text)
    fjs.close()

    print "Current time " + time.strftime("%X")
