import os
import re

def get_history():
    bash_history_path = os.path.expanduser("~/.bash_history")
    zsh_history_path = os.path.expanduser("~/.zsh_history")
    commands = []

    # Read commands from .bash_history
    if os.path.exists(bash_history_path):
        with open(bash_history_path, "r") as bash_history:
            commands.extend(re.findall(r'^\s*(.+?)\s*$', bash_history.read(), re.MULTILINE))

    # Read commands from .zsh_history
    if os.path.exists(zsh_history_path):
        with open(zsh_history_path, "r") as zsh_history:
            commands.extend(re.findall(r'^\s*:\s*0:\s*;\s*(.+?)\s*$', zsh_history.read(), re.MULTILINE))

    return commands

if __name__ == "__main__":
    print(get_history())
