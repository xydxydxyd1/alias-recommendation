# Functions for finding good aliases
import re
import logging

logger = logging.getLogger(__name__)


def split_command(command):
    matcher = r'''(?:[^\s"']+|"[^"\\]*(?:\\.[^"\\]*)*"|'[^'\\]*(?:\\.[^'\\]*)*')+'''
    return re.findall(matcher, command)


def get_head_freqs(history_commands, min_head_len=4):
    """Get a map of all heads and their frequencies, ignoring heads shorter than
    min_head_len

    Heads are the first n words of a command, where n is any real number.
    """
    logger.debug(f"get_head_freqs: Got {history_commands}")
    head_map = {}

    for command in history_commands:
        tokens = []
        tokens = split_command(command)
        logger.debug(f"Processing command {tokens}")
        for i in range(1, len(tokens) + 1):
            head = " ".join(tokens[:i])
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


# Handles ignored_heads since to avoid some costs later on
def rate_heads(head_freqs, alias_len=4, ignored_heads=None):
    """Rate heads based on frequency*length

    This is the rating used for suggesting aliases: Longer heads and more
    frequently used heads are rated higher. The higher the rating, the better
    the alias.

    Returns a map of heads to their ratings
    """
    logger.debug(f"rate_heads: Ignored commands: {ignored_heads}")
    head_rating = {}

    for head, freq in head_freqs.items():
        logger.debug(f"Rating head {head}")
        if ignored_heads and head in ignored_heads:
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


def find_best_alias(head_ratings, existing_aliases, alias_len):
    """Find the best alias from head_ratings that is not in existing_aliases

    Args:
        head_ratings: dict -- The ratings of the heads
        existing_aliases: tuple(set, set) -- The existing aliases' key and value
    """
    logger.debug(f"find_best_alias: Got existing aliases {existing_aliases}")
    best_heads = sorted(
        head_ratings, key=lambda x: head_ratings[x], reverse=True)
    for head in best_heads:
        if head in existing_aliases[1]:
            logger.info(f"Head {head} already has an alias. Skipping it")
            continue
        alias = generate_alias(head, alias_len)
        logger.debug(f"Generated alias {alias} for head {head}")
        if alias in existing_aliases[0]:
            logging.info(f"Alias {alias} already exists. Generating a new one")
            alias = generate_alias(head, alias_len + 1)
        return (alias, head, head_ratings[head])
    return None


# Top level function for recommending an alias
def recommend_alias(history, existing_aliases, alias_len, min_rating, ignored_cmds):
    """Recommend a a good alias. Returns None if no good alias are found"""
    head_ratings = rate_heads(get_head_freqs(history), alias_len, ignored_cmds)
    best_alias = find_best_alias(head_ratings, existing_aliases, alias_len)
    if best_alias is None or best_alias[2] < min_rating:
        logger.info("No good alias found")
        return None
    logger.info(f"Recommending alias: {best_alias}")

    return best_alias
