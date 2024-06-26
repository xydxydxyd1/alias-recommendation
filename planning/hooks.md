# Integrating into ZSH with hooks

Currently, the project is capable of taking a list of histories and generating a
list of aliases once. This document will focus on how to integrate it such that
it meets the following criteria:

2. *Remembers* recommended aliases and commands
3. New algorithm for recommending aliases real-time
4. Integrate with commandline (notably ZSH hooks)

In contrast to the new requirements, we no longer need to generate multiple
aliases, instead focusing on the top one.

## Stateful program

It is possible to make the program stateless by making it comptue all histories
again every command. However, that is a bit expensive especially with a large
history number. Here is the comparison.

Stateful:
* O(nlgn) run time to append new history and find best alias

Stateless:
* Simple
* O(n) run time to append history and find best alias with respect to history
  size.

We are definitely using stateless program

## Remembering current aliases

The `alias` command shows all aliases currently in use. We simply need to parse
it, making sure that we don't accidentally override any alias, both in name and
in value.

This algorithm should also be incorporated into the previous iteration such that
no repeated aliases are recommended.

## Remembering current histories

The simplest way to keep track of current histories is to use the `history`
command.

`history -p` in ZSH will clear all histories. Then, we can call `history` to get
the current history.

# Archived

## Update efficiency -- no longer needed due to statelessness

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

