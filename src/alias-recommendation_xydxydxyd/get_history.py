import os
import logging

logger = logging.getLogger(__name__)

def get_history():
    bash_history_path = os.path.expanduser("~/.bash_history")
    zsh_history_path = os.path.expanduser("~/.zsh_history")
    commands = []

    # Read commands from .bash_history
    if os.path.exists(bash_history_path):
        logger.info("Getting commands from bash_history")
        with open(bash_history_path, "r") as bash_history:
            commands.extend(bash_history.readlines())

    # Read commands from .zsh_history
    if os.path.exists(zsh_history_path):
        logger.info("Getting commands from zsh_history")
        with open(zsh_history_path, "r") as zsh_history:
            commands.extend(zsh_history.readlines())

    return [command.strip() for command in commands]


if __name__ == "__main__":
    print(get_history())
