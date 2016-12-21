#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class GitHubRepository who receive, parse and associate the github information of every user in the semester.
Receive as init argument three dict (as reference) to append the data in outside vars, useful in case of multi
repositories.
"""
from unidecode import unidecode
from Utilities import Cons
from Utilities import all_commits


import sys
reload(sys)
sys.setdefaultencoding('latin-1')

__author__ = "Michel Llorens"
__copyright__ = "Copyright 2016"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "mllorens@dcc.uchile.cl"


class GitHubRepository:
    def __init__(self, commits, issues, comments, events, repository, manager,config):
        print "> Repository", repository['name']
        self.manager = manager
        self.since = Cons.sinceData
        print self.since
        candidates = manager.search_users(repository['root'])
        repository_manager = None
        for candidate in candidates:
            if candidate.login == repository['root']:
                repository_manager = candidate
                break
        print unicode(repository['name'])
	for c in candidates:
		print c
        self.repository = repository_manager.get_repo(repository['name'])
        print unicode(repository_manager.login)
        print unicode(repository['name'])
        branches = self.repository.get_branches()

        #TODO GET COMMENTS https://developer.github.com/v3/repos/comments/

        allcommits = all_commits.get(config,repository)
        for commit in allcommits:
            author = unicode(commit["author"],"utf-8")
            trimmedCommit ={
               'commit_id': commit["commit_id"],
               'message': commit["message"],
               'time': commit["time"],
               'url': commit["url"],
               'branch': commit["branch"],
               'branch_link': commit["branch_link"],
               'additions': commit['additions'],
               'deletions': commit['deletions'],
               'is_merge': commit["is_merge"]}

            #print "author", author
            if author in commits:
                commits[author].append(trimmedCommit)
            else:
                for word in author.split(' '):
                    if word in commits:
                        commits[word].append(trimmedCommit)
                        break
		    print "oooooooooooooaaaps", author
                    print  type(author)
		    print  commit["commit_id"]
                    print "versus"
                    for k in commits.keys():
                        print "    ", k, "  ", str(k)
                    print "==========="

	allcommits = all_commits.get(config,repository, wiki=True)
        for commit in allcommits:
            author = commit["author"]
            trimmedCommit ={
               'commit_id': commit["commit_id"],
               'message': commit["message"],
               'time': commit["time"],
               'url': commit["url"],
               'branch': "wiki",
               'branch_link': commit["branch_link"],
               'additions': commit['additions'],
               'deletions': commit['deletions'],
               'is_merge': commit["is_merge"]}

            if author in commits:
                commits[author].append(trimmedCommit)
            else:
                author = author.split(' ')
                for word in author:
                    if word in commits:
                        commits[word].append(trimmedCommit)
                        break
        #
        #repository_issues = self.repository.get_issues(since=self.since)
        comments['default'] = []
        issues['default'] = []
        #print repository_issues
        first = True
        second = True
        i = 0
        while first or second:
            try:
                i = i + 1
                issue = self.repository.get_issue(i)
                print issue.html_url
                commit_comments = issue.get_comments()
                issue_events = issue.get_events()
                n = 0
                for e in issue_events:
                    event_dict = {'body': e.event,
                            'time': unicode(e.created_at),
                            'url': issue.html_url}
                    author = unidecode(e.actor.login)
                    print e.actor.login, e.event, e.created_at
                    if author in events:
                        print "adding"
                        events[author].append(event_dict)
                    else:
                        author = author.split(' ')
                        for word in author:
                            if word in events:
                                    events[word].append(event_dict)
                                    break
                            else:
                                    print author
                                    print "events missed!"
                                    print events
                                    events['default'].append(event_dict)
                    n += 1

                for comment in commit_comments:
                        comment_dict = {'body': comment.body,
                                        'url': comment.html_url,
                                        'time': unicode(comment.created_at)}
                        author = unidecode(comment.user.login)
                        if author in comments:
                            comments[author].append(comment_dict)
                        else:
                            author = author.split(' ')
                            for word in author:
                                if word in comments:
                                    comments[word].append(comment_dict)
                                    break
                                else:
                                    print author
                                    print "comments missed!"
                                    comments['default'].append(comment_dict)

                assigned_candidate = issue.assignee.login if issue.assignee != None else "None"
                issue_dict = {'title': issue.title + "(" + str(n) + " events)",
                                      'body': issue.body,
                                      'time': unicode(issue.created_at),
                                      'url': issue.html_url,
                                      'assigned': assigned_candidate}

                author = issue.user.login
                if author in issues:
                        issues[author].append(issue_dict)
                else:
                        author = author.split(' ')
                        for word in author:
                                if word in issues:
                                    issues[word].append(issue_dict)
                                    break
                                else:
                                    print author
                                    print "issues missed!"
                                    issues['default'].append(issue_dict)
            except Exception,e:
                print "miss?"
                print e
                if first: 
                    first = False
                elif second:
                    second = False


def commit_is_merge(message):
    merge_words = ['Merge', 'branch', 'into']
    for word in merge_words:
        if word not in message:
            return unicode(False)
    return unicode(True)
