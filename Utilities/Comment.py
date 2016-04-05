"""
Comment class.
Here the program store a Comment from Github with all of his information to easily access to it.
"""
__author__ = "Michel Llorens"
__copyright__ = "Copyright 2016"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "mllorens@dcc.uchile.cl"


class Comment:
    def __init__(self, comment):
        self.comment = comment
        self.body = comment.body
        self.url = comment.html_url
        self.author = comment.user.login
        self.time = comment.created_at
