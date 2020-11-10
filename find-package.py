#!/usr/bin/env python3
import os
import json
import sys
from github import Github


def get_folders(conn, repo_name, pr_number):
    repo = conn.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    return [os.path.dirname(f.filename) for f in pr.get_files()]


def parse_folders(path_list, prefix="sam-", max_projects=2):
    results = set()
    for p in path_list:
        if prefix in p:
            folders = p.split("/")
            for folder in folders:
                if prefix in folder:
                    parent = p.split(folder)[0]
                    results.add("{}/{}".format(parent, folder))
                    break
    if len(results) == 0:
        raise Exception("Parse_Folders", "Could not find project folder")
    if len(results) > max_projects:
        raise ValueError(
            "Max_Projects:{}, Detected:{}".format(max_projects, len(result_dict))
        )
    return list(results)

def get_event(event_path):
    with open(event_path) as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    if os.environ.get('GITHUB_EVENT_NAME') != 'pull_request':
        raise Exception('EventMismatch:{}. Must be pull_request'.format(os.environ.get('GITHUB_EVENT_NAME')))

    event = get_event(os.environ.get('GITHUB_EVENT_PATH'))
    repo = event.get('GITHUB_REPOSITORY')
    pr_num = event.get('pull_request',{}).get('number')
    
    gh = Github(os.env.get("GITHUB_TOKEN"))
    pr_files = get_folders(gh,repo, pr_num)
    projects = parse_folders(pr_files, 'sam-',1)
    print(','.join(projects))



