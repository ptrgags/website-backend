#!/usr/bin/env python
import requests
import pprint
import re

URL_REPOS = "https://api.github.com/users/ptrgags/repos"
URL_TAGS = "https://api.github.com/repos/ptrgags/{}/tags"

def process_repo(repo):
    repo_data = {}
    repo_data['title'] = repo['name']
    repo_data['github_link'] = repo['html_url']
    repo_data['github_page'] = repo['homepage']

    try:
        description, years = re.split(' (?=\()', repo['description'])
    except ValueError:
        description = repo['description']
        years = ""

    repo_data['description'] = description
    repo_data['years'] = years[1:-1]
    return repo_data

def get_tag(repo_title):
    tags_url = URL_TAGS.format(repo_title)
    tags = requests.get(tags_url).json()
    if tags:
        return tags[0]['name']
    else:
        return ''

def fetch_repos(all_repos):
    repos = requests.get(URL_REPOS).json()
    for repo in repos:
        data = process_repo(repo)
        title = data['title']
        all_repos[title] = data

def fetch_tags(all_repos):
    titles = [all_repos[repo]['title'] for repo in all_repos]
    for title in titles:
        all_repos[title]['version_tag'] = get_tag(title)

if __name__ == '__main__':
    all_repos = {}
    fetch_repos(all_repos)
    fetch_tags(all_repos)
    pprint.pprint(all_repos)

