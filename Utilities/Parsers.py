"""
File with static functions to parse data.
"""
import Comment
import Repository
__author__ = "Michel Llorens"
__copyright__ = "Copyright 2016"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "mllorens@dcc.uchile.cl"


def parse_comments(page_list):
    return_list = []
    for c in page_list:
        return_list.append(Comment.Comment(c))
    return return_list


def parse_repositories(manager, projects):
    print "Parsing repositories"
    repositories = []
    for owner, repo in projects.items():
        users = manager.search_users(owner)
        user = None
        for u in users:
            if u.login == owner:
                user = u
                break
        repository = user.get_repo(repo)
        repositories.append(Repository.Repository(repository))
    return repositories


def parse_users_from_json(repository, semester):
    users = []
    for item in semester:
        element = item.items()[0]
        if element[0] == repository:
            users.append(element[1])

    return users


def parse_users_commits(users, commits):
    specific_data = []
    for user in users:
        data = [commit for commit in commits if user["user"] in commit.author or user["nombre"] in commit.author]
        specific_data.append([user, data])
    return specific_data


def parse_users_issues(users, issues):
    specific_data = []
    for user in users:
        data = [issue for issue in issues if user["user"] in issue.author]
        specific_data.append([user, data])
    return specific_data

