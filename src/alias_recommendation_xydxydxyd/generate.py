import pprint
import logging
from get_history import get_history
import argparse
import shlex

logger = logging.getLogger(__name__)


def get_head_freqs(history_commands, min_head_len=4):
    """Get a map of all heads and their frequencies, ignoring heads shorter than
    min_head_len

    Heads are the first n words of a command, where n is any real number.
    """
    head_map = {}

    for command in history_commands:
        words = shlex.split(command)
        for i in range(1, len(words) + 1):
            head = shlex.join(words[:i])
            logger.debug(f"Processing head {head}")
            if len(head) < min_head_len:
                logger.debug(f"Skipping head {head} because it is too short")
                continue
            #logger.debug(f"Found head {head}")
            if head not in head_map:
                head_map[head] = 1
            else:
                head_map[head] += 1
    logger.info(f"Found {len(head_map)} heads")
    return head_map


def rate_heads(head_freqs, alias_len=4, ignored_cmds=None):
    """Rate heads based on frequency*length

    This is the rating used for suggesting aliases: Longer heads and more
    frequently used heads are rated higher. The higher the rating, the better
    the alias.

    Returns a map of heads to their ratings
    """
    head_rating = {}

    for head, freq in head_freqs.items():
        if ignored_cmds and head in ignored_cmds:
            logger.debug(f"Skipping head {head} because it is in ignored_cmds")
            continue
        # The -2 is to give a penalty to longer but infrequent heads
        head_rating[head] = (freq - 2) * (len(head) - alias_len)

    return head_rating


def generate_alias(command, alias_len=4):
    """Generate an alias for a command

    alias_len -- the length of the generated alias. If one cannot be generated,
    command is returned without whitespace.
    """
    words = command.split()
    words = ["".join(filter(str.isalnum, word)) for word in words]

    # List of beginning characters of each word to be used in the alias
    word_heads = ["" for _ in range(len(words))]
    current_alias_len = 0
    out_of_characters = False
    current_character_index = 0
    while current_alias_len < alias_len and not out_of_characters:
        out_of_characters = True
        for word_index, word in enumerate(words):
            if current_character_index < len(word):
                out_of_characters = False
                word_heads[word_index] += word[current_character_index]
                current_alias_len += 1
                if current_alias_len >= alias_len:
                    break
        current_character_index += 1
    return "".join(word_heads)


def get_highest_rated_heads(head_ratings, num_heads=5):
    """Get the highest rated heads in head_ratings"""
    best_heads = sorted(
        head_ratings, key=lambda x: head_ratings[x], reverse=True)
    return best_heads[:num_heads]


def get_best_aliases(history_commands, num_aliases=5, alias_len=4):
    """Get a map of all commands and their suggested aliases

    alias_len -- the length of the generated alias. If one cannot be generated,
    command is returned without whitespace.
    """
    logger.info("Getting head frequencies")
    head_map = get_head_freqs(history_commands)
    logger.info("Rating heads")
    head_rating = rate_heads(head_map, alias_len)
    logger.info("Sorting heads by rating")
    best_heads = sorted(
        head_rating, key=lambda x: head_rating[x], reverse=True)
    logger.info("Generating aliases")
    aliases = {}
    for command in best_heads:
        if len(aliases) >= num_aliases:
            break
        alias = generate_alias(command, alias_len)
        aliases[command] = alias
    return aliases

if __name__ == "__main__":
    # Get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_aliases", type=int, default=5)
    parser.add_argument("--alias_len", type=int, default=2)
    args = parser.parse_args()

    logger.info("Getting history commands")
    history_commands = get_history()

    aliases = get_best_aliases(history_commands, args.num_aliases,
                               args.alias_len)
    pprint.pprint(aliases)

    # head_map = get_head_freqs(history_commands)
    # head_rating = rate_heads(head_map)
    # best_heads = get_highest_rated_heads(head_rating)
    # pprint.pprint(best_heads)
