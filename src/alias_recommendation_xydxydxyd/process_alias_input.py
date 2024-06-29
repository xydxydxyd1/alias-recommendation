# Gets the current alias in use
import re
import logging
import argparse

logger = logging.getLogger(__name__)

# First capture group is the alias name, second is the alias value
alias_matcher = re.compile(r"^([a-zA-Z0-9_.-]+)='?([^']*)'?$")

def process_alias_input(aliases):
    """Finds current aliases by executing `alias`

    Args:
        aliases (str): The output of the `alias` command

    Returns:
        tuple: A tuple containing two sets of strings. The first set contains
        the alias names, and the second set contains the alias values.
    """
    # Parse alias
    alias_names = set()
    alias_vals = set()
    aliases = aliases.split("\n")
    for alias in aliases:
        match = alias_matcher.match(alias)
        if match:
            alias_names.add(match.group(1))
            alias_vals.add(match.group(2))
        else:
            logger.warn(f"Could not parse alias: {alias}")

    logger.info(f"Found {len(alias_names)} aliases")
    logger.debug(f"Aliases found: {alias_names}")
    logger.debug(f"Corresponding to: {alias_vals}")
    return alias_names, alias_vals

#if __name__ == "__main__":
#    parser = argparse.ArgumentParser(description="Get the current aliases in use")
#    parser.add_argument("aliases", type=str, help="The output of the `alias` command")
#    args = parser.parse_args()
#    aliases = process_alias_input(args.aliases)
#    print(aliases)
