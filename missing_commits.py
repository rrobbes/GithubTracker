import cd
import git
import csv

root = '/Users/rr/Desktop/cc4401/projects/2016-1/'

doom = 'mochadoom'
ripples = 'jswingRipples'
tera = 'TeraCity'
logi = 'logisim'

projects = {doom, ripples, tera, logi}

with open('missing_commits.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, quotechar='|')
	header = ['time','project','user','type','url','title','body','assigned','branch','branch_link','merge','add','del','hash']
	writer.writerow(header)
	for p in projects:
		cmd = "git log --pretty=%H --after=2016/04/01 --before=2016/04/28"
		hashes = cd.then_do(p, cmd)
		for hsh in hashes:
			cmd2 = "git log -1 --pretty='%ai;"+p+";%cn;commit;url/%H;;%s;;" + p + "/branch;fake_url;;;;%H' " + hsh
			result = cd.then_do(p, cmd2)
			for r in result:
				r = r.replace(',', '    ')
				l = r[:-1].split(';')
				writer.writerow(l)
			
			     

