import cd

def get_change_log(repo):
	cmd = 'git log --date=local --pretty="format:%at" --name-status --reverse'
	return cd.then_do(repo, cmd)

def get_id_log(repo):
	cmd = 'git log --reverse --pretty="format:%H %P" '
	return cd.then_do(repo, cmd)

def get_backward_id_log(repo):
	cmd = 'git log --pretty="format:%an,%at,%H,%P" '
	return cd.then_do(repo, cmd)

def get_repo(url):
	cmd = 'git clone ' + url
	return cd.then_print('', cmd)

def checkout_commit(repo, commit_id):
	cmd = 'git checkout ' + commit_id
	return cd.then_do(repo, cmd)

def checkout_last_version(repo):
	return checkout_commit(repo, 'master')

def clean_slate(repo):
	return checkout_commit(repo, '-- .')

def is_merge(commit_and_parents):
	return len(commit_and_parents) > 2

def is_first(commit_and_parents):
	return len(commit_and_parents) == 1

def is_regular_commit(commit_and_parents):
	return len(commit_and_parents) == 2


def get_commit_list(repo):
	checkout_last_version(repo)
	for commit in get_id_log(repo):
		commit_ids = commit.split()
		if is_regular_commit(commit_ids):
			yield commit_ids[0], commit_ids[1]

def get_backward_commit_list(repo):
	checkout_last_version(repo)
	for commit in get_backward_id_log(repo):
		commit_info = commit.split(',')
		commit_ids = commit_info[2:-1]
		parents = commit_info[-1].split(' ')
		parents[-1] = parents[-1][:-1] #remove line break
		commit_ids += parents
		if is_regular_commit(commit_ids):
			yield commit_info


def go_to_commit(repo, commit_id):
	clean_slate(repo)
	checkout_commit(repo, commit_id)

def get_diffs(repo, commit_id, flags = '-U0 '):
	cmd = 'git show ' + flags + commit_id
	return cd.then_do(repo, cmd)

if __name__ == '__main__':
	url = 'https://github.com/cjdelisle/cjdns'
	url = 'https://github.com/edwinb/Idris-dev'
	url = 'https://github.com/Daenyth/Cockatrice'
	#get_repo(url)
	for c in get_backward_commit_list('Adaptive-Images'):
		print c
