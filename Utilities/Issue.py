"""
Issue class.
Here the program store an Issue from Github with all of his information to easily access to it.
"""
import Parsers
__author__ = "Michel Llorens"
__copyright__ = "Copyright 2016"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "mllorens@dcc.uchile.cl"


class Issue:
    def __init__(self, issue):
        self.issue = issue
        self.author = issue.user.login
        self.crated_time = issue.created_at
        self.url = issue.html_url
        self.title = issue.title
        self.body = issue.body
        self.state = issue.state
        self.comments = Parsers.parse_comments(issue.get_comments())
        self.assigned_to = issue.assignee.login if issue.assignee != None else None
        self.labels = []

    def get_comments(self):
        return self.comments

    def parse_labels(self, labels):
        for l in labels:
            self.labels.append(l.name)

    def count_comments(self):
        return len(self.comments)
