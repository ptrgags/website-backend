#!/usr/bin/env python
import requests
import json
import re
import sys

URL_REPOS = "https://api.github.com/users/ptrgags/repos"
URL_TAGS = "https://api.github.com/repos/ptrgags/{}/tags"

def process_repo(repo):
    '''
    Process a single repo dict from the GitHub JSON
    and reformat it into a dict of what I need
    for my website.

    repo -- the repo dict
    '''
    repo_data = {}
    
    #Github link and page
    repo_data['github_link'] = repo['html_url']
    repo_data['github_page'] = repo['homepage']

    #Title. My website needs to be reformatted to 'website'
    #to prevent problems in JavaScript due to the '.'s
    title = repo['name']
    if title == 'ptrgags.github.io':
        title = 'website'
    repo_data['title'] = title

    #Split the description into description and years
    try:
        description, years = re.split(' (?=\()', repo['description'])
    except ValueError:
        description = repo['description']
        years = ""
    repo_data['description'] = description
    repo_data['years'] = years[1:-1]

    return repo_data

def get_tag(repo_title, auth):
    '''
    Get the most recent tag and return its
    name.

    repo_title -- the repo to get a tag for
    auth -- tuple (username, OAuth Token)

    returns the most recent tag's name or
    '' if it doesn't exist
    '''
    
    #My website gets special treatment
    if repo_title == 'website':
        repo_title = 'ptrgags.github.io'

    tags_url = URL_TAGS.format(repo_title)
    tags = requests.get(tags_url, auth=auth).json()
    if tags:
        return tags[0]['name']
    else:
        return ''

def fetch_repos(all_repos, auth):
    '''
    Fetch repos via the GitHub API in JSON format
    and reformat it into a dict

    all_repos -- the dict to store the data we want
    '''
    repos = requests.get(URL_REPOS, auth=auth).json()
    for repo in repos:
        data = process_repo(repo)
        title = data['title']
        all_repos[title] = data

def fetch_tags(all_repos, auth):
    '''
    update the dict of repo data with tag information

    all_repos -- dict to store the data
    auth -- tuple (username, OAuth Token)
    '''
    titles = [all_repos[repo]['title'] for repo in all_repos]
    for title in titles:
        all_repos[title]['version_tag'] = get_tag(title, auth)

if __name__ == '__main__':
    #Get OAuth token from command line arguments.
    token = sys.argv[1]
    auth = ('ptrgags', token)

    #Fetch data and store in all_repos
    all_repos = {}
    fetch_repos(all_repos, auth)
    fetch_tags(all_repos, auth)

    #Dump the dict to stdout in JSON format. In my case,
    #I redirect the output to a .json file and then
    #serve the file to the client website however I choose.
    print json.dumps(all_repos, sort_keys=True)
