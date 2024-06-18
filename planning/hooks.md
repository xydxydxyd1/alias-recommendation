# Integrating into ZSH with hooks

Currently, the project is capable of taking a list of histories and generating a
list of aliases once. This document will focus on how to integrate it such that
it meets the following criteria:

1. Can *update* with new commands efficiently
2. *Remembers* recommended aliases
3. New algorithm for recommending aliases real-time
4. Integrate with commandline (notably ZSH hooks)

In contrast to the new requirements, we no longer need to generate multiple
aliases, instead focusing on the top one.

## Update efficiency

Currently, the algorithm rates all commands in the history one single time, then
sort it and generate aliases for the top n commands. Now, we want to be able to
udpate the list but only need the top one command.

I will change the data structure from a list to a priority
queue, due to our need to efficiently input new commands and get the highest
rated one.

Python provides the PriorityQueue class in the queue module linked below. A
wrapper class will be used to store the command and its rating upon
construction.

* `queue`: https://docs.python.org/3/library/queue.html#queue.PriorityQueue

## Remembering current aliases

The `alias` command shows all aliases currently in use. We simply need to parse
it, making sure that we don't accidentally override any alias, both in name and
in value.

This algorithm should also be incorporated into the previous iteration such that
no repeated aliases are recommended.
