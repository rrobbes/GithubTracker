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

            pprint(stat)

            statistics.append([name, stat])

            print "\n"
        self.statistics = statistics

    def write_to_file(self):
        print "Saving to file"
        for repository in self.statistics:
            text = "{"
            name = repository[0]
            elements = repository[1]
            for element in elements:
                person = element[0]
                text += "{'nombre':'"+person["nombre"]+"', 'user':'"+person["user"]+"', 'project':'"+name+"', 'commits':["
                for commit in element[1]:
                    text += Parsers.parse_commit_to_json(commit)+","
                if len(element[1]) == 0:
                    text += "'null' "
                text = text[:-1] + "], 'issues':["
                for issue in element[2]:
                    text += Parsers.parse_issue_to_json(issue)+","
                if len(element[2]) == 0:
                    text += "'null' "
                text = text[:-1] + "], 'comments':["
                for comment in element[3]:
                    text += Parsers.parse_comment_to_json(comment)+","
                if len(element[3]) == 0:
                    text += "'null' "
                text = text[:-1] + "]},"
            text = text[:-1] +"}"

            filename = "Jsons/"+name+".json"
            fo = open(filename, "w+")
            encoded_text = json.dumps(text)
            fo.write(encoded_text)
            fo.close()
        filename = "Jsons/semester.json"
        fo = open(filename, "w+")
        text = "{'semester':["
        for repository in self.statistics:
            text += "'"+repository[0]+"',"
        text = text[:-1]+"]}"
        encoded_text = json.dumps(text)
        fo.write(encoded_text)
        fo.close()


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

