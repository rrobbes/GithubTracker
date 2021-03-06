import csv

from Utilities import Cons
from Utilities import cd
import json

from Utilities.flatten import flat
from metrics.rowFunctions import is_merged,diffchars,nchar_text,nfiles,njavafiles,refactor,bugfix

"""
Generate report with all the commits, issues, comments, events of the projects defined in config
The data is stored as a list of dicts (SEE header)
the final report has a few other columns that are calculated by funtions in rowMetricList
"""

output_csv = "Output/OutEventReport.csv"
output_file = "Output/OutEventReport.json"

header = ['time', 'project', 'user', 'type', 'url', 'title', 'body', 'assigned', 'branch', 'branch_link', 'additions',
	 'deletions','commitHash']

"""
return dict with all the fields in header as None
"""
def defaultDict():
	d={}
	for elem in header:
		d.setdefault(elem)
	return d


#-------------------------------------Pre processing -------------------------------------------------

def formatCommit(p, u, commit):
	dictO = defaultDict()

	dictO['time'] = commit['time']
	dictO['project'] = p
	dictO['user'] = u
	dictO['type'] = commit_wiki(commit) #'COMMIT'
	dictO['url'] = commit['url']

	dictO['body'] = commit['message']
	dictO['branch'] = commit['branch']
	dictO['branch_link'] = commit['branch_link']
	dictO['additions'] = int(commit['additions'])
	dictO['deletions'] = int(commit['deletions'])

	dictO['commitHash'] = commit['url'].split('/')[-1]
	return dictO


def add_comment(p, u, comment):
	dictO = defaultDict()
	dictO['time'] = comment['time']
	dictO['project'] = p
	dictO['user'] = u
	dictO['type'] = 'COMMENT'
	dictO['url'] = comment['url']

	dictO['body'] = comment['body']
	return dictO

def add_event(p, u, event):
	dictO = defaultDict()
	dictO['time'] = event['time']
	dictO['project'] = p
	dictO['user'] = u
	dictO['type'] = 'EVENT'
	dictO['url'] = event['url']

	dictO['body'] = event['body']
	return dictO


def add_issue(p, u, issue):
	dictO = defaultDict()
	dictO['time'] = issue['time']
	dictO['project'] = p
	dictO['user'] = u
	dictO['type'] = issue_pull(issue)
	dictO['url'] = issue['url']

	dictO['title'] = issue['title']
	dictO['body'] = issue['body']
	dictO['assigned'] = issue['assigned']
	return dictO

def issue_pull(issue):
    #https://github.com/JSwingRipples2016/jswingripples/pull/25
    if '/pull/' in issue['url']:
        return 'PULL'
    else: return 'ISSUE'

def commit_wiki(commit):
    if commit['branch'] == 'wiki':
        return 'WIKI'
    else: return 'COMMIT'

def preprocessing(data):
	print "Inicio de preproceso de datos"
	tabla = []
	for project in data:
		for user in project:
			u = user['name']
			p = user['project']
			for commit in user['commits']:
				tabla.append(formatCommit(p, u, commit))
			for comment in user['comments']:
				tabla.append(add_comment(p, u, comment))
			for event in user['events']:
				tabla.append(add_event(p, u, event))
			for bug in user['issues']:
				tabla.append(add_issue(p, u, bug))
	return tabla

#----------------------------------------------Create the report -------------------------------------------------------

def applyMetrics(data,functions,preFun):
	print "Inicio de proceso de calculo de metricas"
	for row in data:
		for h, fun in functions:
			row[h] = preFun(fun, row)
	return data

def get(config):
	#Open config file
	with open('Output/output.json') as data_file:
		data = json.load(data_file)

	tabla = preprocessing(data)

	#In this case all the metrics are for commits so a kind of filter is needed
	#if the type of the row is commit calculate else return None value
	filtroCommit = lambda f,r : f(r) if r['type'] == 'COMMIT' and not (r['branch'] == 'wiki') else None

	# lista headerName : Rowfuntion
	#TODO the base data for the rowFunctions could change (diferent data for diferent reports)
	rowMetricList = [
		("is_merged", is_merged)
		, ("diffChars", diffchars)
		, ('BodyLength', nchar_text)
		, ('nfiles', nfiles)
		, ('njavafiles', njavafiles)
		, ('refactor', refactor)
		, ('bugfix', bugfix)
			  ]

	#Apply the defined functions and add to dict as new columns
	tabla = applyMetrics(tabla, rowMetricList, filtroCommit)

	#Save to json
        print "saving json"
	with  open(output_file, "w") as toWrite:
		toWrite.write(json.dumps(tabla))

	#Save to csv
        print "saving csv"
	headerExt = header + [columnName for (columnName,fun) in rowMetricList]
	flat(output_csv, headerExt, tabla)

        #split to sub-csvs
        print "splitting per user"
        tablas = {}
        for row in tabla:
            user = row['user']
            if user not in tablas:
                tablas[user] = []
            tablas[user].append(row)
        for user, rows in tablas.iteritems():
            output = "Output/" + user + ".csv" 
            print output
            flat(output, headerExt, rows)

