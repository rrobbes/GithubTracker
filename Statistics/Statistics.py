"""
Statistics class.
Here the program inspect a repository and store the statistics from each user.
"""
import Utilities.Parsers as Parsers
import json
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

            statistics.append([name, stat])

            print "\n"
        self.statistics = statistics

    def write_to_file(self):
        print "Saving to file"
        to_write = "var json_list = ["
        for repository in self.statistics:
            l = list()
            name = repository[0]
            elements = repository[1]
            for element in elements:
                person = element[0]
                p = {}
                commit_list = []
                issues_list = []
                comment_list = []
                p['nombre'] = person['nombre']
                p['user'] = person['user']
                p['github_link'] = 'https://github.com/'+person['user']
                p['project'] = name
                for commit in element[1]:
                    commit_list.append(Parsers.parse_commit_to_json(commit))
                p['commits'] = commit_list
                for issue in element[2]:
                    issues_list.append(Parsers.parse_issue_to_json(issue))
                p['issues'] = issues_list
                for comment in element[3]:
                    comment_list.append(Parsers.parse_comment_to_json(comment))
                p['comments'] = comment_list
                l.append(p)
            encoded_text = json.dumps(l)
            to_write += encoded_text+','
        to_write = to_write[:-1]+'];'
        projects = []
        d = {}
        for repository in self.statistics:
            projects.append(repository[0])
        d['semester'] = projects
        encoded_text = json.dumps(d)
        to_write += '\nvar projects_json = '+encoded_text+';'
        js_filename = "cc4401/js/output.js"
        fjs = open(js_filename, "w+")
        fjs.write(to_write)
        fjs.close()


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
