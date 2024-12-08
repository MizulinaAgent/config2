import os
import zlib
from datetime import datetime
import argparse
import subprocess


def read_git_object(repo_path, object_hash):
    object_path = os.path.join(repo_path, '.git', 'objects', object_hash[:2], object_hash[2:])
    try:
        with open(object_path, 'rb') as f:
            compressed_data = f.read()
            decompressed_data = zlib.decompress(compressed_data)
        return decompressed_data
    except FileNotFoundError:
        print(f"Объект {object_hash} не найден.")
        return None


def parse_commit_object(raw_data):
    data = raw_data.decode('utf-8')
    lines = data.split('\n')
    commit_info = {'tree': None, 'parents': [], 'author': None, 'date': None, 'message': ''}

    for line in lines:
        if line.startswith('tree'):
            commit_info['tree'] = line.split()[1]
        elif line.startswith('parent'):
            commit_info['parents'].append(line.split()[1])
        elif line.startswith('author'):
            commit_info['author'] = line.split('author ')[1]
        elif line.startswith('committer'):
            parts = line.split()
            commit_info['date'] = int(parts[-2])
        elif line.strip() == '':
            commit_info['message'] = '\n'.join(lines[lines.index(line) + 1:])
            break

    return commit_info


def get_branches(repo_path):
    refs_path = os.path.join(repo_path, '.git', 'refs', 'heads')
    branches = []
    for root, dirs, files in os.walk(refs_path):
        for file in files:
            branch = os.path.relpath(os.path.join(root, file), refs_path)
            branches.append(branch)
    return branches


def get_commit_history(repo_path, before_date):
    branches = get_branches(repo_path)
    all_commits = {}
    branch_heads = {}

    for branch in branches:
        head_ref_path = os.path.join(repo_path, '.git', 'refs', 'heads', branch)
        with open(head_ref_path, 'r') as f:
            branch_heads[branch] = f.read().strip()

    for branch, commit_hash in branch_heads.items():
        while commit_hash:
            if commit_hash in all_commits:
                break
            raw_data = read_git_object(repo_path, commit_hash)
            if raw_data is None:
                break
            commit_info = parse_commit_object(raw_data)
            commit_date = datetime.fromtimestamp(commit_info['date'])
            if before_date and commit_date >= before_date:
                commit_hash = commit_info['parents'][0] if commit_info['parents'] else None
                continue
            all_commits[commit_hash] = {
                'hash': commit_hash,
                'branch': branch,
                'date': commit_date,
                'author': commit_info['author'],
                'message': commit_info['message'],
                'parents': commit_info['parents'],
            }
            commit_hash = commit_info['parents'][0] if commit_info['parents'] else None

    return all_commits


def build_mermaid_graph(commits):
    branch_commits = {}
    for commit_hash, commit in commits.items():
        branch = commit['branch']
        if branch not in branch_commits:
            branch_commits[branch] = []
        branch_commits[branch].append(commit)

    mermaid_graph = "graph TD\n"

    for branch, branch_commits_list in branch_commits.items():
        mermaid_graph += f"  subgraph {branch}\n"
        mermaid_graph += f"    direction TB\n"
        for commit in branch_commits_list:
            commit_hash = commit['hash']
            commit_message = commit['message']
            mermaid_graph += f'    {commit_hash}["{commit_message}<br>({commit_hash[:7]})"]\n'
        mermaid_graph += "  end\n"

    for commit_hash, commit in commits.items():
        for parent_hash in commit['parents']:
            mermaid_graph += f"    {commit_hash} --> {parent_hash}\n"

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


def main():
    parser = argparse.ArgumentParser(description="Commit Dependency Graph Visualizer")
    parser.add_argument('--viz', required=True, help='Path to the graph visualization program (Mermaid CLI)')
    parser.add_argument('--repo', required=True, help='Path to the git repository to analyze')
    parser.add_argument('--date', required=True, help='Include commits before this date (YYYY-MM-DD)')

    args = parser.parse_args()

    if not os.path.exists(args.viz):
        print(f"Visualization program {args.viz} not found.")
        return

    if not os.path.exists(args.repo):
        print(f"Repository {args.repo} not found.")
        return

    try:
        before_date = datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print("Дата должна быть в формате YYYY-MM-DD.")
        return

    commits = get_commit_history(args.repo, before_date)
    if not commits:
        print("Нет подходящих коммитов до указанной даты.")
        return

    mermaid_graph = build_mermaid_graph(commits)
    mermaid_file = "graph.mmd"
    save_mermaid_file(mermaid_graph, mermaid_file)
    display_graph(mermaid_file, args.viz)


if __name__ == "__main__":
    main()
