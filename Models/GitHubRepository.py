#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class GitHubRepository who receive, parse and associate the github information of every user in the semester.
Receive as init argument three dict (as reference) to append the data in outside vars, useful in case of multi
repositories.
"""
from unidecode import unidecode
from Utilities import Cons
__author__ = "Michel Llorens"
__copyright__ = "Copyright 2016"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "mllorens@dcc.uchile.cl"


class GitHubRepository:
    def __init__(self, commits, issues, comments, repository, manager):
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
        """for branch in branches:
	  #hack!!
	  if False:
            name_branch = branch.name
            sha = branch.commit.sha
            print "> Branch", name_branch

            repository_commits = self.repository.get_commits(sha=sha, since=self.since)

            for commit in repository_commits:
                commit_comments = commit.get_comments()
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

                is_merge = commit_is_merge(commit.commit.message)
                commit_dict = {'message': commit.commit.message,
                               'time': unicode(commit.commit.committer.date),
                               'url': commit.commit.html_url,
                               'branch': name_branch,
                               'branch_link': 'https://github.com/'+unicode(repository_manager.login)+'/'+unicode(repository[1])+'/commits/'+name_branch,
                               'additions': str(commit.stats.additions),
                               'deletions': str(commit.stats.deletions),
                               'is_merge': is_merge}
                author = unidecode(commit.author.login if commit.author != None else commit.commit.author.name)

                if author in commits:
                    commits[author].append(commit_dict)
                else:
                    author = author.split(' ')
                    for word in author:
                        if word in commits:
                            commits[word].append(commit_dict)
                            break
        """
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
	    except:
		 print 'error ...'
	


def commit_is_merge(message):
    merge_words = ['Merge', 'branch', 'into']
    for word in merge_words:
        if word not in message:
            return unicode(False)
    return unicode(True)
