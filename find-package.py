#!/usr/bin/env python3
import os
from github import Github

conn = Github(os.env.get('GITHUB_SECRET'))

def get_files(pr_hash):
