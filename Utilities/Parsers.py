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
    repositories = []
    for name, name_repo in projects.items():
        users = manager.search_users(name)
        user = None
        for u in users:
            if u.login == name:
                user = u
                break
        repo = user.get_repo(name_repo)
        repositories.append(Repository.Repository(repo))
    return repositories


