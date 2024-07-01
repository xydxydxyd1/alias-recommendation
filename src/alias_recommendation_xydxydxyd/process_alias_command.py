# Process inputs and outputs of alias command, including escaping single quotes.
import re
import logging
import argparse

logger = logging.getLogger(__name__)

# First capture group is the alias name, second is the alias value
alias_matcher = re.compile(r"^([a-zA-Z0-9_.-]+)=('?[^']*')?$")


def get_current_aliases(alias_keys, alias_vals):
    """Finds current aliases by executing `alias`

    Args:
        aliases (str): The output of the `alias` command

    Returns:
        tuple: A tuple containing two sets of strings. The first set contains
        the alias names, and the second set contains the alias values.
    """
    # Parse alias

    alias_keys = set(alias_keys.split("\n"))
    alias_vals = set(alias_vals.split("\n"))
    logger.debug(f"Aliases found: {alias_keys}")
    logger.debug(f"Corresponding to: {alias_vals}")
    return alias_keys, alias_vals


def generate_alias_cmd(alias_name, alias_val):
    alias_val = alias_val.replace("'", "\\'")
    return f"alias {alias_name}=$'{alias_val}'"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get the current aliases in use")
    parser.add_argument("alias_keys", type=str,
                        help="The output of the `alias` command")
    parser.add_argument("alias_vals", type=str,
                        help="The output of the `alias` command")
    args = parser.parse_args()
    aliases = get_current_aliases(args.alias_keys, args.alias_vals)
    print(aliases)
