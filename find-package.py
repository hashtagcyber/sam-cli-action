#!/usr/bin/env python3
import os
from github import Github

conn = Github(os.env.get('GITHUB_SECRET'))

def get_folders(repo_name, pr_number):
    repo = conn.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    return [os.path.dirname(f.filename) for f in pr.get_files()]

def parse_folders(path_list, prefix='sam-', max_projects=2):
    results = set()
    for p in path_list:
        if prefix in p:
            folders = p.split('/')
            for folder in folders:
                if prefix in folder:
                    parent = p.split(folder)[0]
                    results.add('{}/{}'.format(parent,folder))
                    break
    if len(results) == 0:
        raise Exception('Parse_Folders','Could not find project folder')
    if len(results) > max_projects:
        raise ValueError('Max_Projects:{}, Detected:{}'.format(max_projects, len(result_dict)))
    return list(results)
