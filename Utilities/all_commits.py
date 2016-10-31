#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cd
import re


def get(config,repo):
    all_commits = []
    root = config['root']
    #header = ['time', 'project', 'user', 'type', 'url', 'title', 'body', 'assigned', 'branch', 'branch_link',
    #		  'merge', 'add', 'del', 'hash']
    #writer.writerow(header)
    p = root + "/" + repo["name"]
    branches = cd.then_do(p,"git branch -r -v --no-abbrev")
    for rawbranch in branches:
        branchlist = rawbranch.split(" ")
        cbranch = ""
        chash = ""
        counter = 0
        for elem in branchlist:
            if counter == 2:
                break
            if elem != "" and elem != "->":
                if counter == 0:
                    cbranch = elem
                elif counter == 1:
                    chash = elem
                counter += 1
        branch = "/".join(cbranch.split("/")[1:]).strip() # Quito el origin
        branchurl = u"https://www.github.com/" + repo["root"] + u"/" + repo["name"] + u"/commits/" + unicode(branch,"utf-8")
        cd.then_print(p,"git checkout "+branch)
        cd.then_print(p,"git pull")
        cmd = u"git log " + chash + u" --after='" + config["startDate"] + u"' --before='" + config["endDate"] + "' --pretty=format:'%n%H%n%ai%n%s%n%an%n%ae' --numstat"
        commits = cd.then_do(p, cmd)
        i=1; # Primera linea siempre es un enter
        while (i<len(commits)):
            commit = commits[i]
            i += 1
            date = commits[i].split(" ")
            time = date[0]+" "+date[1]
            i += 1
            summary = commits[i]
            i += 1
            merge = False
            if "merge" in summary.lower():
                merge = True
            author = commits[i]
            i += 1
            email = commits[i]
            i += 1
            url = u"https://www.github.com/"+repo["root"]+u"/"+repo["name"]+u"/commit/"+commit
            statnum=0
            add=0
            rem=0
            while (i < len(commits) and commits[i]!=""):
                commitline = commits[i]
                i += 1
                addrm = re.findall(r'\d+',commitline)
                while (len(addrm)<2):
                    addrm.append("0")
                statnum += 1
                add += int(addrm[0])
                rem += int(addrm[1])
            while (i < len(commits) and len(commits[i]) != 10):
                i += 1 #Saltar los enters, a veces hay uno y otras dos

            # el cursor debería estar posicionado en el próximo caso,
            # o en ninguno si es el último
            r = {
            "commit_id":commit,
            "repository":repo["name"],
            "author": author,
            "message": summary,
            "time": time,
            "url": url,
            "branch": repo["name"]+"/"+unicode(branch,"utf-8"),
            "branch_link":branchurl,
            "additions": add,
            "deletions": rem,
            "is_merge": merge,
            }
            all_commits.append(r)
    return all_commits

