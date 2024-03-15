#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import traceback
from github import Github
import requests

# Configuration
move_path = "/tmp/starchecker/old/"
directory = "/tmp/starchecker/repos/"
token = ""


def clone_repository(repo_url, destination):
    try:
        subprocess.call(["git", "clone", repo_url, destination])
        print(f"Cloned repository: {repo_url}")
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to clone repository: {repo_url}")
        return False


def update_repository(directory):
    try:
        os.chdir(directory)
        subprocess.call(["git", "config", "pull.rebase", "true"])
        subprocess.call(["git", "checkout", "origin/master", "."])
        subprocess.call(["git", "reset", "--hard"])
        subprocess.call(["git", "pull"])
        print(f"Updated repository: {directory}")
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to update repository: {directory}")
        return False


def move_repository(source, destination):
    try:
        subprocess.call(["mv", source, destination])
        print(f"Moved repository from {source} to {destination}")
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to move repository from {source} to {destination}")
        return False


def check_git_repo_existence(repo_url):
    try:
        response = requests.head(repo_url)
        return response.status_code == 200
    except requests.RequestException:
        return False


try:
    # Authenticate with GitHub
    g = Github(token)

    # Get starred repositories
    starred_repos = g.get_user().get_starred()

    # Clone or update repositories
    for repo in starred_repos:
        repo_name = repo.name
        repo_directory = os.path.join(directory, repo_name)

        if not os.path.exists(repo_directory):
            if clone_repository(repo.clone_url, repo_directory):
                continue
        else:
            if update_repository(repo_directory):
                continue

        # Move repository if unable to clone/update
        move_repository(repo_directory, move_path)

except Exception as e:
    print(f"An error occurred: {e}")
    print(traceback.format_exc())
