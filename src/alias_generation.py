import pprint
from get_history import get_history


def get_head_freqs(history_commands, min_head_len=4):
    """Get a map of all heads and their frequencies, ignoring heads shorter than
    min_head_len

    Heads are the first n words of a command, where n is any real number.
    """
    head_map = {}

    for command in history_commands:
        words = command.split()
        for i in range(1, len(words) + 1):
            head = " ".join(words[:i])
            if len(head) < min_head_len:
                continue
            if head not in head_map:
                head_map[head] = 1
            else:
                head_map[head] += 1
    return head_map


def rate_heads(head_map):
    """Rate heads based on frequency*length

    This is the rating used for suggesting aliases: Longer heads and more
    frequently used heads are rated higher. The higher the rating, the better
    the alias.
    """
    head_rating = {}

    for head, freq in head_map.items():
        head_rating[head] = freq * len(head)

    return head_rating


def generate_alias(command, alias_len=4):
    """Generate an alias for a command

    alias_len -- the length of the generated alias. If one cannot be generated,
    command is returned without whitespace.
    """
    words = command.split()
    # A list of integers representing the head of each word taken in the command
    # to be composed into an alias
    word_head_taken = [1]*len(words)
    total_len = len(words)
    while total_len < alias_len:
        for i in range(len(words)):
            if word_head_taken[i] < len(words):
                word_head_taken[i] += 1
                total_len += 1
                if total_len >= alias_len:
                    break
    word_heads = [words[i][:word_head_taken[i]] for i in range(len(words))]
    return "".join(word_heads)


def get_highest_rated_heads(head_ratings, num_heads=5):
    """Get the highest rated heads in head_ratings"""
    best_heads = sorted(
        head_ratings, key=lambda x: head_ratings[x], reverse=True)
    return best_heads[:num_heads]


def get_best_aliases_from_history(history_commands, num_aliases=5, alias_len=4):
    """Get a map of all commands and their suggested aliases

    alias_len -- the length of the generated alias. If one cannot be generated,
    command is returned without whitespace.
    """
    print("Getting head frequencies")
    head_map = get_head_freqs(history_commands)
    print("Rating heads")
    head_rating = rate_heads(head_map)
    print("Sorting heads by rating")
    best_heads = sorted(
        head_rating, key=lambda x: head_rating[x], reverse=True)
    print("Generating aliases")
    aliases = {}
    for command in best_heads:
        if len(aliases) >= num_aliases:
            break
        alias = generate_alias(command, alias_len)
        aliases[command] = alias
    return aliases

if __name__ == "__main__":
    print("Getting history commands")
    history_commands = get_history()

    #aliases = get_best_aliases_from_history(history_commands)
    #pprint.pprint(aliases)

    head_map = get_head_freqs(history_commands)
    head_rating = rate_heads(head_map)
    best_heads = get_highest_rated_heads(head_rating)
    pprint.pprint(best_heads)
