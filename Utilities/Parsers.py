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
    for project in projects:
        parsed_repo = {'project': project['project'],
                       'repos': []}
        repos = project['repos']
        for repo in repos:
            users = manager.search_users(repo[0])
            user = None
            for u in users:
                if u.login == repo[0]:
                    user = u
                    break
            repository = user.get_repo(repo[1])
            parsed_repo['repos'].append(Repository.Repository(repository))
        repositories.append(parsed_repo)
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
        data = [commit for commit in commits if commit.author in user["user"] or commit.author in user["nombre"]]
        specific_data.append([user, data])
    return specific_data


def parse_users_issues(users, issues):
    specific_data = []
    for user in users:
        data = [issue for issue in issues if issue.author in user["user"]]
        specific_data.append([user, data])
    return specific_data


def parse_users_comments(users, comments):
    specific_data = []
    for user in users:
        data = []
        for list_comment in comments:
            if len(list_comment) == 0:
                continue
            for l in list_comment:
                data += [comment for comment in l if comment.author in user["user"]]
        specific_data.append([user, data])
    return specific_data


def parse_commit_to_json(commit):
    branch_link = 'https://github.com/Michotastico/GithubTracker/commits/'+commit.branch
    is_merge = commit_is_merge(commit.message)
    d = {'message': commit.message, 'time': commit.time, 'url': commit.url, 'branch': commit.branch,
         'branch_link': branch_link, 'additions': commit.additions, 'deletions': commit.deletions,
         'is_merge': is_merge}
    return d


def parse_issue_to_json(issue):
    d = {'title': issue.title, 'body': issue.body, 'time': issue.crated_time, 'url': issue.url,
         'assigned': issue.assigned_to}
    return d


def parse_comment_to_json(comment):
    d = {'comment': comment.body, 'time': comment.time, 'url': comment.url}
    return d


def commit_is_merge(message):
    merge_words = ['Merge', 'branch', 'of', 'into']
    for word in merge_words:
        if word not in message:
            return unicode(False)
    return unicode(True)
