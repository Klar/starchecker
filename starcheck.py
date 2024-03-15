#!/usr/bin/python
# -*- coding: utf-8 -*-

# Install
# sudo pip install PyGithub
# create github token with "read:user scope"

from github import Github
import subprocess
import traceback
import os
import requests

move_path = "/tmp/starchecker/old/"
directory = "/tmp/starchecker/repos/"
token = ""


def get_repo_url():
    try:
        # Run the command to get the repository URL
        result = subprocess.run(
            ["grep", "-m", "1", "url =", ".git/config"],
            capture_output=True,
            text=True,
            check=True,
        )
        # Extract and return the repository URL
        url = result.stdout.split()[2]
        return url
    except subprocess.CalledProcessError:
        # Handle error if .git/config file or 'url =' line not found
        return None


def check_git_repo_existence(repo_url):
    try:
        response = requests.head(repo_url)
        return response.status_code == 200
    except requests.RequestException:
        return False


try:
    g = Github(token)

    starred_repos = g.get_user().get_starred()

    for repo in starred_repos:
        os.chdir(directory)
        user_reponame = repo._full_name.value

        if not os.path.exists(repo._name.value):
            print("doing a clone of %(user_reponame)s" % locals())
            subprocess.call(
                ["git", "clone", user_reponame, directory + repo._name.value]
            )
            print("done: %(user_reponame)s" % locals())

    for repo in os.listdir(directory):
        os.chdir(directory + repo)
        repo_url = get_repo_url()
        if check_git_repo_existence(repo_url):
            # if True:
            print("Repository URL:", repo_url)
            subprocess.call(["git", "config", "pull.rebase", "true"])
            subprocess.call(["git", "checkout", "origin/master", "."])
            subprocess.call(["git", "reset", "--hard"])
            subprocess.call(["git", "pull"])
        else:
            print("Error: Repository URL not found.")
            subprocess.call(["mv", directory + repo, move_path])

except:
    print(str(traceback.format_exc()))
