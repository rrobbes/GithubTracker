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

__author__ = "Michel Llorens"
__copyright__ = "Copyright 2016"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "mllorens@dcc.uchile.cl"


class GitHubRepository:
    def __init__(self, commits, issues, comments, repository, manager,config):
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
        self.repository = repository_manager.get_repo(repository['name'])
        print unicode(repository_manager.login)
        print unicode(repository['name'])
        branches = self.repository.get_branches()

        #TODO GET COMMENTS https://developer.github.com/v3/repos/comments/

        allcommits = all_commits.get(config,repository)
        for commit in allcommits:
            author = commit["author"]
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

            if author in commits:
                commits[author].append(trimmedCommit)
            else:
                author = author.split(' ')
                for word in author:
                    if word in commits:
                        commits[word].append(trimmedCommit)
                        break
        #repository_issues = self.repository.get_issues(since=self.since)
        comments['default'] = []
        issues['default'] = []
        #print repository_issues
        for i in range(1,5):
            try:
                issue = self.repository.get_issue(i)
                print issue.html_url
                commit_comments = issue.get_comments()
                events = issue.get_events()
                for e in events:
                    print e.actor, e.event, e.created_at
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
                                    print "missed!"
                                    comments['default'].append(comment_dict)
                        assigned_candidate = issue.assignee.login if issue.assignee != None else ""
                        issue_dict = {'title': issue.title,
                                      'body': issue.body,
                                      'time': unicode(issue.created_at),
                                      'url': issue.html_url,
                                      'assigned': assigned_candidate}

                        author = unidecode(issue.assignee.login) if issue.assignee is not None else ""
                        if author in issues:
                            issues[author].append(issue_dict)
                        else:
                            author = author.split(' ')
                            for word in author:
                                if word in issues:
                                    issues[word].append(issue_dict)
                                    break
                                else:
                                    print "missed!"
                                    issues['default'].append(issue_dict)
            except Exception,e:
                print 'Ha ocurrido exception ',str(e)


def commit_is_merge(message):
    merge_words = ['Merge', 'branch', 'into']
    for word in merge_words:
        if word not in message:
            return unicode(False)
    return unicode(True)
