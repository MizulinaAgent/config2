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

def build_mermaid_graph(commits):

    mermaid_graph = "graph TD\n"

    for i, commit in enumerate(commits):
        commit_hash = commit[0]
        commit_message = commit[1]
        files_folders = commit[2]
        files_folders_str = "<br>".join(files_folders)
        mermaid_graph += f'    {commit_hash}["{commit_message}<br>"]\n'

        if i > 0:
            previous_commit_hash = commits[i - 1][0]
            mermaid_graph += f'    {commit_hash} --> {previous_commit_hash}\n'

    return mermaid_graph

def save_mermaid_file(mermaid_graph, output_path):

    with open(output_path, 'w', encoding="utf-8") as f:
        f.write(mermaid_graph)

def display_graph(mermaid_path, mermaid_tool_path):

    png_file = "graph.png"
    cmd = [mermaid_tool_path, "-i", mermaid_path, "-o", png_file]
    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("Ошибка при генерации изображения графа.")
    else:
        print(f"Граф сохранён в {png_file}. Открываю...")
        os.startfile(png_file) if os.name == "nt" else subprocess.run(["xdg-open", png_file])