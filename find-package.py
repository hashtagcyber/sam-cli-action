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
                    if len(parent) > 0:
                        results.add("{}/{}".format(parent, folder))
                    else:
                        results.add(folder)
                    break
    if len(results) == 0:
        raise Exception("Parse_Folders", "Could not find project folder")
    if len(results) > max_projects:
        raise ValueError(
            "Max_Projects:{}, Detected:{}\n{}".format(
                max_projects, len(results), ",".join(results)
            )
        )
    return list(results)


def get_event(event_path):
    with open(event_path) as f:
        data = json.load(f)
    return data


def process_pr():
    event = get_event(os.environ.get("GITHUB_EVENT_PATH"))
    repo = os.environ.get("GITHUB_REPOSITORY")
    pr_num = event.get("pull_request", {}).get("number")

    gh = Github(os.environ.get("GITHUB_TOKEN"))
    pr_files = get_folders(gh, repo, pr_num)
    projects = parse_folders(pr_files, "sam-", 1)
    print(",".join(projects))


def process_merge():
    event = get_event(os.environ.get("GITHUB_EVENT_PATH"))
    repo = os.environ.get("GITHUB_REPOSITORY")
    commit_sha = event.get("commits", [{}])[0].get("id")

    gh = Github(os.environ.get("GITHUB_TOKEN"))
    gh_repo = gh.get_repo(repo)
    commit = gh_repo.get_commit(commit_sha)
    pr_num = max([p.number for p in commit.get_pulls()])

    pr_files = get_folders(gh, repo, pr_num)
    projects = parse_folders(pr_files, "sam-", 1)
    print(",".join(projects))


if __name__ == "__main__":
    event_name = os.environ.get("GITHUB_EVENT_NAME")
    if event_name == "pull_request":
        process_pr()
    elif event_name == "push":
        process_merge()
    else:
        raise Exception(
            "UnsupportedEvent:{}. Must be pull_request or push".format(
                os.environ.get("GITHUB_EVENT_NAME")
            )
        )
