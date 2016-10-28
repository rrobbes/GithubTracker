#--------------------------------------------------ROW METRICS using header --------------------------------------------------------

# determine if the commit made it to the master branch
# git branch -r --contains 4d0520e3539
from Utilities import Cons
from Utilities import cd


def is_merged(row):
	project = row['project']
	branch = row['branch']
	cmt_hash = row['commitHash']
	cmd = "git branch --contains " + cmt_hash
	p = Cons.root + "/" + project #TODO facil de romper el nombre por defecto nombre carpeta == nombre repo siempre???
	result = cd.then_do(p, cmd)
	for line in result:
		if line.endswith('master\n'):
			return True
	return False


# number of words in the diff / chars?
# git diff -U0 --word-diff=porcelain 7c79 7c79^
# also use .gitattributes
def diffchars(row):
	added, deleted = diff(row)
	return sum(map(len, added)), sum(map(len, deleted))

# diff in the commit
def diff(row):
	project = row['project']
	branch = row['branch']
	cmt_hash = row['commitHash']
	cmd = "git diff -U0 --word-diff=porcelain " + cmt_hash + "^ " + cmt_hash + " *.java"
	p = Cons.root + "/" + project  # TODO facil de romper el nombre por defecto nombre carpeta == nombre repo siempre???
	result = cd.then_do(p, cmd)
	added = []
	deleted = []
	for line in result:
		if line.startswith('+') and not line.startswith('+++'):
			added.append(line[1:-1])
		else:
			if line.startswith('-') and not line.startswith('---'):
				deleted.append(line[1:-1])
	return added, deleted

# number of words/chars in comments/commit messages
# different metric for issue definition?
def nchar_text(row):
	return len(row['body'])

# number of files in commit
# use to filter binaries?
# git diff --name-only 56d558b86 56d558b86^
def nfiles(row):
	project = row['project']
	branch = row['branch']
	cmt_hash = row['commitHash']
	cmd = "git diff --name-only " + cmt_hash
	p = Cons.root + "/" + project  # TODO facil de romper el nombre por defecto nombre carpeta == nombre repo siempre???
	result = cd.then_do(p, cmd)
	nfiles = 0
	for line in result:
		nfiles += 1
	return nfiles

# number of files in commit
# use to filter binaries?
# git diff --name-only 56d558b86 56d558b86^
def njavafiles(row):
	project = row['project']
	branch = row['branch']
	cmt_hash = row['commitHash']
	cmd = "git diff --name-only " + cmt_hash
	p = Cons.root + "/" + project  # TODO facil de romper el nombre por defecto nombre carpeta == nombre repo siempre???
	result = cd.then_do(p, cmd)
	nfiles = 0
	for line in result:
		if line.endswith('java\n'):
			nfiles += 1
	return nfiles


# determines if the commit has refactoring activity
# based on keyword
def refactor(row):
	return 'refactor' in row['body']

# determines if the commit has bug fixing activity
# based on keyword
def bugfix(row):
	return 'fix' in row['body']

# -------------------------------------------------- Metrics of the old xtraxtrametrics -------------------------------------------
def add_minus_del(row):
    return (row['additions'] - row['deletions'])

def total_contrib(row):
    return (add_minus_del(row) + (len(row['body']) / 5.0))
