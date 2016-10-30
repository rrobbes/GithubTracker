#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
                branches = cd.then_do(p,"git branch -r").split("\n");
                for cbranch in branches:
                    branch = "/".join(cbranch.split("/")[1:]) # Quito el origin
                    branchurl = "https://www.github.com/"+repo["root"]+"/"+repo["name"]+"/commits/"+branch
                    cd.then_print(p,"git checkout "+branch)
                    cd.then_print(p,"git pull")
                    cmd = "git log "+branch+" --pretty=format:'%n%H%n%ai%n%s%n%an%ae' --numstat"
                    commits = cd.then_do(p, cmd).split("\n");
                    i=1; # Primera linea siempre es un enter
                    while (i<len(commits)):
                        commit = commits[i]
                        i += 1
                        date = commits[i].split[" "]
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
                        url = "https://www.github.com/"+repo["root"]+"/"+repo["name"]+"/commit/"+commit
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
                        r = [time,repo["name"],author,"commit",url,"",summary,"",branch,branchurl,merge,add,rem,commit]
                        writer.writerow(l)


