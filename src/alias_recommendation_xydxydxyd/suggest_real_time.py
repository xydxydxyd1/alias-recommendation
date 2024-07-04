#!/usr/bin/env python3
# See if there is any highly-rated alias. If yes, print out the suggestion
import argparse
from generate import recommend_alias
from alias_io import get_current_aliases, generate_alias_cmd
import logging
import pprint

logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse inputs for the suggest_real_time.py script.

    Returns:
        history: str -- The history of commands considered for alias
        existing_aliases: str -- The output of the `alias
    """
    parser = argparse.ArgumentParser(
        description='See if there is any highly-rated alias. If yes, suggest it real time.')
    parser.add_argument('history', type=str,
                        help='The history of commands considered for alias')
    parser.add_argument('existing_aliases_keys', type=str,
                        help='Newline separated')
    parser.add_argument('existing_aliases_vals', type=str,
                        help='Newline separated')
    parser.add_argument('--ignored_cmds', type=str, default="",
                        help='A newline-delimited list of all commands to never make aliases for.')
    parser.add_argument('--alias_len', type=int, default=3)
    parser.add_argument('--min_rating', type=int, default=100)
    args = parser.parse_args()
    logger.info(f"Ran with history of length {len(args.history)}")
    logger.info(f"Ran with alias length {args.alias_len}")
    logger.info(f"Ran with ignored commands of length {
                len(args.ignored_cmds)}")
    return args


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename='suggest_real_time.log')

    logger.info("Parsing arguments")
    args = parse_arguments()
    existing_aliases = get_current_aliases(args.existing_aliases_keys,
                                                args.existing_aliases_vals)
    args.history = args.history.split("\n")
    args.ignored_cmds = args.ignored_cmds.split("\\n")
    args.ignored_cmds = set(args.ignored_cmds)

    # Argument debug
    logger.debug("ARGUMENTS:")
    logger.debug(f"Ignored commands: {pprint.pformat(args.ignored_cmds)}")
    logger.debug(f"History: {pprint.pformat(args.history)}")
    logger.debug(f"Existing aliases: {pprint.pformat(existing_aliases)}")
    logger.debug(f"Alias length: {args.alias_len}")

    logger.info("Recommending alias")
    recommended_alias = recommend_alias(args.history, existing_aliases,
                                        args.alias_len, args.min_rating,
                                        args.ignored_cmds)

    # Output
    if recommended_alias is None:
        logger.info("No good alias found")
        exit(0)
    logger.info(f"Recommended alias: {recommended_alias}")
    # Output in newline format for ZSH parsing
    print(f"{recommended_alias[0]}\n{recommended_alias[1]}")
