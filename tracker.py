#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main class of the GithubTracker project
"""
import Utilities.Login as Login
import References.Semester as semester
import time
from pprint import pprint
from Models.GitHubRepository import GitHubRepository

__author__ = "Michel Llorens"
__copyright__ = "Copyright 2016"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "mllorens@dcc.uchile.cl"


login = Login.Login()

manager = login.get_user()

print "Current time " + time.strftime("%X")

for project in semester.fall16_projects:
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
        pprint(commits_dict)

print "Current time " + time.strftime("%X")
print "done"

