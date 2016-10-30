import csv

from Utilities import cd


def get(config):
    with open(config["exportName"], 'a') as csvfile:
		root = config['root']
		writer = csv.writer(csvfile, quotechar='|')
		#header = ['time', 'project', 'user', 'type', 'url', 'title', 'body', 'assigned', 'branch', 'branch_link',
		#		  'merge', 'add', 'del', 'hash']
		#writer.writerow(header)
		for project in config['projects']:
			for repo in project['repos']:
				p = root + "/" + repo["name"]
				cd.then_print(p, "git checkout")
				cd.then_print(p, "git update")
				cmd = "git log --pretty=%H --after=2016/04/01 --before=2016/04/28"
				hashes = cd.then_do(p, cmd)
				for hsh in hashes:
					cmd2 = "git log -1 --pretty='%ai;" + p + ";%cn;commit;url/%H;;%s;;" + p + "/branch;fake_url;;;;%H' " + hsh
					result = cd.then_do(p, cmd2)
					for r in result:
						r = r.replace(',', '    ')
						l = r[:-1].split(';')
						writer.writerow(l)
