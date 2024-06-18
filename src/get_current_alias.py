# Gets the current alias in use
import os
import re
import logging
import pprint

logger = logging.getLogger(__name__)

# First capture group is the alias name, second is the alias value
alias_matcher = re.compile(r"^([a-zA-Z0-9_.-]+)=([']?)([^']*)'$")

def get_current_alias(aliases):
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

    logger.info(f"Found number of aliases: {len(alias_names)}")
    return alias_names, alias_vals

if __name__ == "__main__":
