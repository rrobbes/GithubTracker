"""
Login class.
Class for login purpose
"""
import getpass
from github import Github
import Cons
__author__ = "Michel Llorens"
__copyright__ = "Copyright 2016"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "mllorens@dcc.uchile.cl"


class Login:

    def __init__(self, user=None):
        print "Welcome to the Github Tracker\n\nNow we attempt to connect to GitHub\n"
        if not user:
            user = raw_input("Username: ")
        password = getpass.getpass("Password: ")
        #password = 'aeiou58132154'
        self.user = Github(user, password)

    def get_user(self):
        return self.user

