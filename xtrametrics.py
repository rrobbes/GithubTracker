import cd
import git
import csv


root = '/Users/rr/Desktop/cc4401/projects/2016-1/'

doom = 'mochadoom'
ripples = 'jswingRipples'
eclipse = 'eclipsePlugin'
netbeans = 'netBeansPlugin'
tera = 'TeraCity'
logi = 'logisim'

repomapping = { 'Matias Haeussler': doom, 'Francisco Clavero': ripples, 'Manuel Olguin': ripples, 'Rodrigo Delgado': ripples, 'Francisco Pulgar': tera, 'Diego Madariaga': logi,
'Natalia Vidal': ripples, 'Cristian Guzman': eclipse, 'Sergio Penafiel': logi, 'Mario Garrido': ripples, 'Javier Zambra': doom, 'Eduardo Riveros': tera, 'Nicolas Bravo': tera,
'Paula Rios': tera, 'Andres Ferrada': tera, 'Nicolas Java': doom, 'Ismael Alvarez': logi, 'Joaquin Torres': doom, 'Paolo Curotto': logi, 'Franco Sepulveda': tera, 'Javier Diaz': logi,
'Jaime Capponi': doom, 'Gabriel Dintrans': logi, 'Juan Rojas': tera, 'Nicolas Caracci': doom, 'Victor Molina': netbeans, 'Fabian Souto': doom, 'Braulio Lopez': doom, 'Pablo Gomez': doom,
'Vicente Rotman': logi, 'Bastian Ermann': tera, 'Patricio Taiba': doom, 'Emilio Aburto': ripples, 'Rodrigo Vera': doom} #?


# map user to git repo on disk
def gitfor(user):
	pass

# determine if the commit made it to the master branch
# git branch -r --contains 4d0520e3539
def is_merged(commit):
	projectbranch = commit[8].split('/')
	project = projectbranch[0]
	branch = projectbranch[1]
	cmt_hash = commit[-1]
	cmd = "git branch --contains " + cmt_hash
	result = cd.then_do(project, cmd)
	for line in result:
		if line.endswith('master\n'):
			return True
	return False


# number of words in the diff / chars?
# git diff -U0 --word-diff=porcelain 7c79 7c79^
# also use .gitattributes
def diffchars(commit):
	added, deleted = diff(commit)
	#print "added = ", added
	#print "deleted = ", deleted
	return sum(map(len, added)), sum(map(len, deleted))

# diff in the commit
def diff(commit):
	projectbranch = commit[8].split('/')
	project = projectbranch[0]
	branch = projectbranch[1]
	cmt_hash = commit[-1]
	cmd = "git diff -U0 --word-diff=porcelain " + cmt_hash + "^ " + cmt_hash + " *.java"
	result = cd.then_do(project, cmd)
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
def nchars(text):
	return len(text)

def nchar_text(event):
	return nchars(event[6])

# number of files in commit
# use to filter binaries?
# git diff --name-only 56d558b86 56d558b86^
def nfiles(commit):
	projectbranch = commit[8].split('/')
	project = projectbranch[0]
	branch = projectbranch[1]
	cmt_hash = commit[-1]
	cmd = "git diff --name-only " + cmt_hash + "^ " + cmt_hash
	result = cd.then_do(project, cmd)
	nfiles = 0
	for line in result:
		nfiles += 1
	return nfiles

# number of files in commit
# use to filter binaries?
# git diff --name-only 56d558b86 56d558b86^
def njavafiles(commit):
	projectbranch = commit[8].split('/')
	project = projectbranch[0]
	branch = projectbranch[1]
	cmt_hash = commit[-1]
	cmd = "git diff --name-only " + cmt_hash + " " + cmt_hash + "^" 
	result = cd.then_do(project, cmd)
	nfiles = 0
	for line in result:
		if line.endswith('java\n'):
			nfiles += 1
	return nfiles

def is_merge(commit):
	projectbranch = commit[8].split('/')
        project = projectbranch[0]
	branch = projectbranch[1]
	cmt_hash = commit[-1]
	cmd = "git log --pretty=%P -n 1 " + cmt_hash  
	result = cd.then_do(project, cmd)
	for line in result:
		return len(line.split()) > 1


# determines if the commit has refactoring activity
# based on keyword
def refactor(commit):
	return 'refactor' in commit[6]

# determines if the commit has bug fixing activity
# based on keyword
def bugfix(commit):
	return 'fix' in commit[6]


#with open('/Users/rr/Dropbox/cc4401/GithubTracker/out_final_maybe_test.csv') as data_file: 
#with open('/Users/rr/Dropbox/cc4401/GithubTracker/out_final_maybe.csv') as data_file: 

def get(config):
    with open(config["exportName"]) as data_file:
        with open('out_missing.csv', 'w') as csvfile:
            reader = csv.reader(data_file, quotechar='|')
            writer = csv.writer(csvfile, quotechar='|')
            for line in reader:
                merge = ""
                is_merge_cmt = ""
                files = ""
                jfiles = ""
                add_char = ""
                del_char = ""
                add_minus_del = ""
                refac = ""
                bugfx = ""
                msglen = ""
                if line[3] == 'commit':
                    commit = line
                    projectbranch = commit[8].split('/')
                    print projectbranch
                    project = projectbranch[0]
                    branch = projectbranch[1]
                    cmt_hash = commit[-1]
                    print cmt_hash
                    merge = is_merged(commit)
                    is_merge_cmt = is_merge(commit)
                    files = nfiles(commit)
                    jfiles = njavafiles(commit)
                    add_char, del_char = diffchars(commit)
                    add_minus_del = add_char - del_char
                    refac = refactor(commit)
                    bugfx = bugfix(commit)
                    #print project, cmt_hash, nfiles(commit)
                    #print project, cmt_hash, diffchars(commit)
                    #if not is_merged(commit):
                    #	print project, cmt_hash
                    #if refactor(commit) or bugfix(commit):
                    #	print commit[6], cmt_hash
                msglen = nchar_text(line)
                line.extend([merge,is_merge_cmt, files,jfiles,add_char,del_char, add_minus_del, refac, bugfx, msglen])
                writer.writerow(line)


