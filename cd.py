import os

def workdir():
	wd = '/Desktop/cc4401/projects/2016-1/'
	rr = '/Users/rr'
	rrobbes = '/Users/rrobbes'
	if os.path.isdir(rr): return rr + wd
	else: return rrobbes + wd

def subdir(subdir):
	wd = workdir()
	sub = wd + '/' + subdir
	if not os.path.exists(sub):
		os.makedirs(sub)
	return sub + '/'

def cdRepo(work_dir, repo):
	path = 'cd ' + work_dir + '/' + repo
	return path

def cdAndDo(repo, command):
	path = cdRepo(workdir(), repo)
	cmd = path + ';' + command
	stream = os.popen(cmd)
	return stream

def then_do(repo, command):
	return cdAndDo(repo, command)

def cdAndPrint(repo, command):
	for l in cdAndDo(repo, command): print l

def then_print(repo, command):
	return cdAndPrint(repo, command)

