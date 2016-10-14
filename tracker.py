#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main class of the GithubTracker project
"""
import Utilities.Login as Login
import References.Semester as semester
import time
from Models.GitHubRepository import GitHubRepository
import json

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

login = Login.Login()

manager = login.get_user()

print "Current time " + time.strftime("%X")

for project in semester.fall16_projects:
  #if project['project'] == 'logisim':
    print "Working on project:", project['project']
    commits_dict = {}
    issues_dict = {}
    comments_dict = {}
    for student in semester.fall16:
        if student['project'] == project['project']:
            commits_dict[student['student']['nombre']] = []
            issues_dict[student['student']['nombre']] = []
            comments_dict[student['student']['nombre']] = []
            for alias in student['student']['user']:
                commits_dict[alias] = []
                issues_dict[alias] = []
                comments_dict[alias] = []
    for repository in project['repos']:
        GitHubRepository(commits_dict, issues_dict, comments_dict, repository, manager)

    clean_duplicated(commits_dict)
    clean_duplicated(comments_dict)

    output_file = "Output/"+project['project']+".json"
    text = "{\"project\": \""+project['project']+"\", \"content\": ["
    text += json.dumps(commits_dict)
    text += ","
    text += json.dumps(issues_dict)
    text += ","
    text += json.dumps(comments_dict)
    text += "]}"
    fjs = open(output_file, "w+")
    fjs.write(text)
    fjs.close()

text = "var json_list = ["
project_text = {
    'semester': []
}
for project in semester.fall16_projects:
    project_name = project['project']
    project_text['semester'].append(project_name)

    inner_text = "["

    file_name = "Output/"+project_name+".json"
    f_json = open(file_name, "r")
    json_data = f_json.read()
    json_data = json.loads(json_data)['content']

    for student in semester.fall16:
        if student['project'] != project_name:
            continue
        student = student['student']
        student_text = {'project': project_name,
                        'nombre': student['nombre'],
                        'user': student['user'][0],
                        'commits': [],
                        'issues': [],
                        'comments': []}
        student_commits = json_data[0][student['nombre']]
        student_issues = json_data[1][student['nombre']]
        student_comments = json_data[2][student['nombre']]

        for commit in student_commits:
            student_text['commits'].append(commit)
        for issue in student_issues:
            student_text['issues'].append(issue)
        for comment in student_comments:
            student_text['comments'].append(comment)

        for alias in student['user']:
            student_commits = json_data[0][alias]
            student_issues = json_data[1][alias]
            student_comments = json_data[2][alias]

            for commit in student_commits:
                student_text['commits'].append(commit)
            for issue in student_issues:
                student_text['issues'].append(issue)
            for comment in student_comments:
                student_text['comments'].append(comment)

        student_text = json.dumps(student_text)
        inner_text += student_text
        inner_text += ","
    inner_text = inner_text[:-1] + "]"
    text += inner_text + ","
text = text[:-1] + "];"
project_text = json.dumps(project_text)
text += "\nvar projects_json = "
text += project_text
text += ";"

output_file = "Output/output.js"
fjs = open(output_file, "w+")
fjs.write(text)
fjs.close()

print "Current time " + time.strftime("%X")
print "done"
