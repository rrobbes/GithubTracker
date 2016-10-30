import cd
import git
import csv
import re


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
				cd.then_print(p,"git checkout")
				cd.then_print(p,"git update")
				cmd = "git log --all --pretty=format:'%n%H%n%ai%n%s%n%an%ae' --numstat"
				commits = cd.then_do(p, cmd).split("\n");
				int i=1; # Primera linea siempre es un enter
                while (i<len(commits)):
                    commit = commits[i]
                    i += 1
                    date = commits[i]
                    i += 1
                    summary = commits[i]
                    i += 1
                    statnum=0
                    add=0
                    rem=0
                    while (len(commits[i]) != 1):
                        commitline = commits[i]
                        addrm = re.findall(r'\d+',commitline)
                        statnum += 1
                        add += addrm[0]
                        rm += addrm[1]
                        i += 1
                    while (i < len(commits) and len(commits[i] ==1)):
                        i += 1 #Saltar los enters, a veces hay uno y otras dos

                    # el cursor debería estar posicionado en el próximo caso,
                    # o en ninguno si es el último
    				for r in result:
    					r = r.replace(',', '    ')
    					l = r[:-1].split(';')
    					writer.writerow(l)


