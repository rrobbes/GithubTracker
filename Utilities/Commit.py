"""
Commit class.
Here the program store a Commit from Github with all of his information to easily access to it.
"""
import Parsers
__author__ = "Michel Llorens"
__copyright__ = "Copyright 2016"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "mllorens@dcc.uchile.cl"


class Commit:
    def __init__(self, commit):
        self.commit = commit
        self.author = commit.author.login if commit.author != None else commit.commit.author.name
        self.message = commit.commit.message
        self.url = commit.commit.html_url
        self.time = unicode(commit.commit.committer.date)
        self.comments = Parsers.parse_comments(commit.get_comments())

    def get_comments(self):
        return self.comments

    def count_comments(self):
        return len(self.comments)

