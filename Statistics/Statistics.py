"""
Statistics class.
Here the program inspect a repository and store the statistics from each user.
"""
import Utilities.Parsers as Parsers
import os
from pprint import pprint
__author__ = "Michel Llorens"
__copyright__ = "Copyright 2016"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "mllorens@dcc.uchile.cl"


class Statistics:
    def __init__(self, repositories, semester):
        self.repositories = repositories
        self.semester = semester
        self.statistics = []

    def calculate(self):
        statistics = []
        print "calculating statistics per user\n"
        for repository in self.repositories:
            name = repository.get_name()
            print name
            team = Parsers.parse_users_from_json(name, self.semester)
            print ">commits"
            commits = repository.get_commits()
            commits_per_head = Parsers.parse_users_commits(team, commits)

            print ">issues"
            issues = repository.get_issues()
            issues_per_head = Parsers.parse_users_issues(team, issues)

            print ">comments"
            comments_commits = [commit.get_comments() for commit in commits]
            comments_issue = [issue.get_comments() for issue in issues]
            comments_per_head_c = Parsers.parse_users_comments(team, comments_commits)
            comments_per_head_i = Parsers.parse_users_comments(team, comments_issue)

            comments_per_head = merge_comments(comments_per_head_c, comments_per_head_i)

            stat = merge_lists(commits_per_head, issues_per_head, comments_per_head)

            pprint(stat)

            statistics.append([name, stat])

            print "\n"
        self.statistics = statistics

    def write_to_file(self):
        for repository in self.statistics:
            for element in repository:
                text = "" # TODO fill with parsers and write to file



def merge_comments(commits, issues):
    return_list = []
    size = len(commits)
    for i in range(size):
        comments = commits[i][1] + issues[i][1]
        return_list.append([commits[i][0], comments])
    return return_list


def merge_lists(commits, issues, comments):
    return_list = []
    size = len(commits)
    for i in range(size):
        return_list.append([commits[i][0], commits[i][1], issues[i][1], comments[i][1]])
    return return_list

