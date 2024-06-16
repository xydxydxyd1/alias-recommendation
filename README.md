# Alias Recommendation

Uses saved history of commands to recommend aliases for frequently used
commands.

#### Algorithm

Rates each command's head (i.e. first n words) based on frequency and length.

# Usage

* `src/setup_history.py` - Setup history for bash and zsh
* `src/get_history.py` - Get history of commands
* `src/alias_recommendation.py` - Recommend aliases for frequently used commands
