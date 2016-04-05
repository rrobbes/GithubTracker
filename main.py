"""
Main class of the GithubTracker project
"""
import getpass
from github import Github
import References.Semester as Repositories
import Utilities.Parsers as Parsers
__author__ = "Michel Llorens"
__copyright__ = "Copyright 2016"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "mllorens@dcc.uchile.cl"

print "Connecting to Github"
user = raw_input("Username: ")
password = getpass.getpass("Password: ")

manager = Github(user, password)

repositories = Parsers.parse_repositories(manager, Repositories.fall16)

# TODO Get statistics from repositories
print "done"

