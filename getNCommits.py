#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from Utilities.Cons import user,passw
#Basado en https://gist.github.com/JeffPaine/3145490
#http://stackoverflow.com/questions/9179828/github-api-retrieve-all-commits-for-all-branches-for-a-repo


"""
Get all commits given Repo, branch and a since date. It will query 250 commmits for request and stop
when it reach the last page of the result. The pages of the result are in the header['link']
"""
def queryAllCommitsBranch(requester,owner,repo,branch,stopAt=None):
    url = 'https://api.github.com/repos/%s/%s/commits' % (owner, repo)
    # The sha is the hash of a commit, also if you put the branch name return all commits for that branch
    par = {'sha': branch, 'per_page' : 150}
    if stopAt != None:
        par['since'] = str(stopAt)

    allCommits = []
    currentUrl = url
    (page,maxPage,tries) = (1,2,0)

    while (page <= maxPage):
        r2 = requests.get(currentUrl,params=par,auth=(user, passw))
        status = r2.status_code
        if page == 1:
            maxPage = 1 if len(r2.links) == 0 else int(r2.links['last']['url'].split('=')[-1])
        if status == 200:
            print 'Successfully returned info page ',page,' of ',maxPage
            allCommits += r2.json()
            page +=1
            currentUrl = None if not r2.links.has_key('next') else r2.links['next']['url']
            tries=0
        else:
            print 'Could not get ',owner,' ',repo,' info. Status : ',status
            tries += 1
            if tries > 10:
                raise Exception(tries,' tries have passed couldnt get info')
    print "Returning ",len(allCommits)," elements"
    return allCommits