#!/usr/bin/python
# -*- coding: utf-8 -*-

# Install
# sudo pip install PyGithub

from github import Github
import subprocess
import traceback
import os

directory = "/var/data/scripts/starchecker/repos/"
username = ""
password = ""

try:
	g = Github(username, password)

	starred_repos = g.get_user().get_starred()
	for repo in starred_repos:
		user_reponame = repo._full_name.value
		if not os.path.exists(repo._name.value):
			print("doing a clone of %(user_reponame)s" % locals())
			repoclone = "https://github.com/%(user_reponame)s" % locals()
			subprocess.call(['git', 'clone', repoclone, directory + repo._name.value])

			print("done: %(user_reponame)s" % locals())

	print("updating repos...")
	for repo in os.listdir(directory):
		print repo + ":"
		os.chdir(directory + repo)
		subprocess.call(['git', 'pull'])
except:
	print(str(traceback.format_exc()))
