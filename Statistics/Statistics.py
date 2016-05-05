"""
Statistics class.
Here the program inspect a repository and store the statistics from each user.
"""
import Utilities.Parsers as Parsers
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

    def calculate(self):
        print "calculating statistics per user"
        for repository in self.repositories:
            name = repository.get_name()
            print name
            team = Parsers.parse_users_from_json(name, self.semester)
            commits = repository.get_commits()
            commits_per_head = Parsers.parse_users_commits(team, commits)
            pprint(commits_per_head)
            issues = repository.get_issues()
            issues_per_head = Parsers.parse_users_issues(team, issues)
            pprint(issues_per_head)

