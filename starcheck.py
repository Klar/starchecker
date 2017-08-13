#!/usr/bin/python
# -*- coding: utf-8 -*-

# Install
# sudo pip install PyGithub

from github import Github
import subprocess
import traceback
import os

username = "myusername"
password = "mypassword"

try:
	g = Github(username, password)

	starred_repos = g.get_user().get_starred()
	
	for repo in starred_repos:
		user_reponame = repo._full_name.value
		if not os.path.exists(repo._name.value):
			print("doing a clone of %(user_reponame)s" % locals())
			repoclone = "https://github.com/%(user_reponame)s" % locals()
			subprocess.call(['git', 'clone', repoclone])

			print("done: %(user_reponame)s" % locals())

	print("updating repos...")
	repo_update = subprocess.call("ls | xargs -I{} git -C {} pull", shell=True)

except:
	print(str(traceback.format_exc()))
