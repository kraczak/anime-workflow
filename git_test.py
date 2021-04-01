import os
import subprocess
from typing import List

import tqdm


class cd:
    def __init__(self, new_path: str):
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        if not os.path.exists(self.new_path):
            os.makedirs(self.new_path)
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)


def run_command(commands: List[str], stdout: int = subprocess.DEVNULL) -> subprocess.CompletedProcess:
    response = subprocess.run(commands, stdout=stdout)
    return response


def save_file(name, txt):
    with open(name, 'w') as f:
        f.write(txt)


lorem = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."

user = 'kraczak'
name = 'temat'
repo = f'https://github.com/{user}/{name}'

run_command(["git", "clone", repo])
n = 3000
k = 5
with cd('temat'):
    for i in tqdm.tqdm(range(2655, 3500)):
        run_command(['git', 'checkout', '-b', f'test_{i}'])

        for j in range(k):
            save_file(f'test_{i}.txt', lorem)
        run_command(['echo', lorem, '>' f'test_{i}.txt'])
        run_command(["git", "add", "."])
        run_command(["git", "commit", "-m", f"Added test_{i} project files"])
        run_command(["git", "push", "-u", "origin", "HEAD"])
        run_command(['git', 'checkout', f'master'])

if __name__ == '__main__':
    pass
