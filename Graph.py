import subprocess
import os
import argparse
from datetime import datetime


def get_commit_history(repo_path, before_date):

    date_str = before_date.strftime("%Y-%m-%dT%H:%M:%S")
    cmd = [
        "git", "-C", repo_path, "log", "--pretty=format:%H %s", "--name-only",
        f"--before={date_str}"
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, encoding="utf-8")

    if result.returncode != 0:
        print("Ошибка получения истории коммитов.")
        return []

    commit_data = []
    raw_commits = result.stdout.strip().split("\n\n")
    for raw_commit in raw_commits:
        lines = raw_commit.strip().split("\n")
        if not lines or len(lines[0].strip()) == 0:
            continue

        commit_line = lines[0].split(maxsplit=1)
        if not commit_line:
            continue

        commit_hash = commit_line[0]
        commit_message = commit_line[1] if len(commit_line) > 1 else ""

        if len(lines) < 2:
            files = []
        else:
            files = sorted(set(lines[1:]))

        commit_data.append((commit_hash, commit_message, files))

    return commit_data