#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unidecode import unidecode
from Utilities import Cons
__author__ = "Michel Llorens"
__copyright__ = "Copyright 2016"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "mllorens@dcc.uchile.cl"


class GitHubRepository:
    def __init__(self, commits, issues, comments, repository, manager):
        print "> Repository", repository[1]

        self.manager = manager
        self.since = Cons.sinceData

        candidates = manager.search_users(repository[0])
        repository_manager = None
        for candidate in candidates:
            if candidate.login == repository[0]:
                repository_manager = candidate
                break
        self.repository = repository_manager.get_repo(repository[1])

        branches = self.repository.get_branches()
        for branch in branches:
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
                        print author
                        author = author.split(' ')
                        for word in author:
                            if word in comments:
                                comments[word].append(comment_dict)
                                print "Founded!"
                                break

                is_merge = commit_is_merge(commit.commit.message)
                commit_dict = {'message': commit.commit.message,
                               'time': unicode(commit.commit.committer.date),
                               'url': commit.commit.html_url,
                               'branch': name_branch,
                               'branch_link': 'https://github.com/Michotastico/GithubTracker/commits/'+name_branch,
                               'additions': str(commit.stats.additions),
                               'deletions': str(commit.stats.deletions),
                               'is_merge': is_merge}
                author = unidecode(commit.author.login if commit.author != None else commit.commit.author.name)

                if author in commits:
                    commits[author].append(commit_dict)
                else:
                    print author
                    author = author.split(' ')
                    for word in author:
                        if word in commits:
                            commits[word].append(commit_dict)
                            print "Founded!"
                            break

            repository_issues = self.repository.get_issues(since=self.since)
            for issue in repository_issues:
                commit_comments = issue.get_comments()
                for comment in commit_comments:
                    comment_dict = {'body': comment.body,
                                    'url': comment.html_url,
                                    'time': unicode(comment.created_at)}
                    author = comment.user.login
                    if author in comments:
                        comments[author].append(comment_dict)
                    else:
                        print author
                        author = author.split(' ')
                        for word in author:
                            if word in comments:
                                comments[word].append(comment_dict)
                                print "Founded!"
                                break

                assigned_candidate = issue.assignee.login if issue.assignee != None else ""
                issue_dict = {'title': issue.title,
                              'body': issue.body,
                              'time': unicode(issue.created_at),
                              'url': issue.html_url,
                              'assigned': assigned_candidate}

                author = issue.assignee.login if issue.assignee is not None else ""
                if author in issues:
                    issues[author].append(issue_dict)
                else:
                    print author
                    author = author.split(' ')
                    for word in author:
                        if word in issues:
                            issues[word].append(issue_dict)
                            print "Founded!"
                            break


def commit_is_merge(message):
    merge_words = ['Merge', 'branch', 'into']
    for word in merge_words:
        if word not in message:
            return unicode(False)
    return unicode(True)
