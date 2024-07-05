# Setup
Run `src/install.zsh`

# Alias Recommendation

Uses saved history of commands to recommend aliases for frequently used
commands.

#### Algorithm

Rates each command's head (i.e. first n words) based on frequency and length.

# Usage

For one-time recommendations:
* `src/setup_history.py` - Setup history for bash and zsh
* `src/get_history.py` - Get history of commands
* `src/alias_recommendation.py` - Recommend aliases for frequently used commands

For constant recommendations:
* `src/alias_hook.zsh` - contains a function that suggests an alias based on
  past history

# Next steps
* Refine ignore system since right now, it may continue to (annoyingly)
  recommend shorter versions of ignored commands.
* Install and setup scripts
* Allow for editting of aliases before execution (kind of like git commit)
