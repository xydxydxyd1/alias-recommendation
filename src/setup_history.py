# Run to set up history for zsh and bash
import os

MAX_HISTORY_SIZE = 1000     # Number of commands saved in each history file

def zsh_setup():
    """Sets up history for ZSH"""
    zshrc_path = os.path.expanduser("~/.zshrc")
    with open(zshrc_path, "a") as zshrc:
        zshrc.write(f'HISTSIZE={MAX_HISTORY_SIZE}\n')
        zshrc.write('SAVEHIST=${HISTSIZE}\n')
        zshrc.write('HISTFILE=~/.zsh_history\n')

def bash_setup():
    """Sets up history for BASH"""
    bashrc_path = os.path.expanduser("~/.bashrc")
    with open(bashrc_path, "a") as bashrc:
        bashrc.write(f'HISTSIZE={MAX_HISTORY_SIZE}\n')
        bashrc.write('HISTFILESIZE=${HISTSIZE}\n')
        bashrc.write('HISTFILE=~/.bash_history\n')

SHELL_SIGNATURES = {
    "zsh": {
        "paths": ["/bin/zsh", "/usr/bin/zsh"],
        "setup": zsh_setup
    },
    "bash": {
        "paths": ["/bin/bash", "/usr/bin/bash"],
        "setup": bash_setup
    }
}


def check_paths(paths):
    """Return true if one path exists, false otherwise"""
    for path in paths:
        print(f"Checking {path}")
        if os.path.exists(path):
            return True
    return False


def detect_shells():
    """Return list of detected shells on system, determined by
    SHELL_SIGNATURES"""
    detected_shells = []
    for shell, signatures in SHELL_SIGNATURES.items():
        if check_paths(signatures["paths"]):
            detected_shells.append(shell)
        else:
            print(f"Could not detect {shell}")
    return detected_shells


def setup_control(shell_name):
    """Prompts user for whether they want to execute setup. Return true
    if user wants to execute setup for shell of shell_name"""
    # Recommend addition to zshrc file
    print(f"We detected {shell_name}. Set it up for saving history in .{
          shell_name}_history? (y/n) ")
    choice = input()
    return choice == "y" or choice == "Y"


def setup():
    """Complete setup flow for SHELL_SIGNATURES"""
    detected_shells = detect_shells()
    for shell in detected_shells:
        if setup_control(shell):
            print(f"Setting up {shell} history")
            SHELL_SIGNATURES[shell]["setup"]()
        else:
            print(f"Skipping {shell} history setup")


if __name__ == "__main__":
    setup()
