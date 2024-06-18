# See if there is any highly-rated alias. If yes, suggest it real time.
import argparse
from generate import generate_alias, get_head_freqs, rate_heads
from process_alias_input import process_alias_input
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
    parser.add_argument('existing_aliases', type=str,
                        help='The output of the `alias` command')
    parser.add_argument('--alias_len', type=int, default=3)
    args = parser.parse_args()
    logger.info(f"Ran with history of length {len(args.history)}")
    logger.info(f"Ran with alias length {args.alias_len}")
    logger.info(f"Ran with existing aliases of length {len(args.existing_aliases)}")
    return args.history, args.existing_aliases, args.alias_len


def find_best_alias(head_ratings, existing_aliases, alias_len):
    """Find the best alias from head_ratings that is not in existing_aliases

    Args:
        head_ratings: dict -- The ratings of the heads
        existing_aliases: tuple(set, set) -- The existing aliases' key and value
    """
    best_heads = sorted(
        head_ratings, key=lambda x: head_ratings[x], reverse=True)
    for head in best_heads:
        if head in existing_aliases[0]:
            logging.info(f"Head {head} already has an alias")
            continue
        alias = generate_alias(head, alias_len)
        logger.debug(f"Generated alias {alias} for head {head}")
        if alias in existing_aliases[1]:
            logging.info(f"Alias {alias} already exists. Generating a new one")
            alias = generate_alias(head, alias_len + 1)
        return (alias, head, head_ratings[head])
    return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    history, existing_aliases, alias_len = parse_arguments()
    existing_aliases = process_alias_input(existing_aliases)
    history = history.split("\n")
    logging.info(f"Got history of length {len(history)}")

    head_freqs = get_head_freqs(history)
    head_ratings = rate_heads(get_head_freqs(history), alias_len)
    best_alias = find_best_alias(head_ratings, existing_aliases, alias_len)
    pprint.pprint(best_alias);