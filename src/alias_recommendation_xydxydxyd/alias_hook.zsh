# preexec ZSH hook for suggesting aliases

get_alias_keys() {
    local alias_keys=""
    for k in "${(@k)aliases}"; do
        local alias_keys="$alias_keys\n$k"
    done
    echo "$alias_keys"
}


get_alias_vals() {
    local alias_vals=""
    for k in "${(@k)aliases}"; do
        local alias_vals="$alias_vals\n${aliases[$k]}"
    done
    echo "$alias_vals"
}


# Escape single quotes in alias value
escape_alias() {
    echo "$1" | sed "s/'/'\\\\''/g"
}


# Hook function to suggest alias
suggest_alias() {
    local suggest_cmd='suggest_real_time.py "$(history "-10" | cut -c 8-)" "$(get_alias_keys)" "$(get_alias_vals)" --ignored_cmds "$IGNORED_ALIAS" --min_rating 25'
    local py_output="$(eval $suggest_cmd)"
    local output_matcher="^alias ([a-zA-Z0-9_]+)=\\$'(.*)'$"
    if [[ -n "$py_output" ]]; then
        #echo "Output of suggest_cmd: $py_output"

        IFS=$'\n' local py_output=($(echo "$py_output"))
        local py_output=($py_output)
        local alias_name="${py_output[1]}"
        local alias_value="${py_output[2]}"
        local alias_cmd="alias $alias_name='$(escape_alias "$alias_value")'"

        echo "Suggested alias: $alias_cmd"
        read "yn?Do you want to create this alias for this window? [y/n]"
        if ! [[ "$yn" =~ ^[Yy]$ ]]; then
            echo 'Alias not created and will not be suggested again.'
            export IGNORED_ALIAS="$alias_value\n$IGNORED_ALIAS"
            return
        fi

        echo "Creating $alias_cmd"
        eval $alias_cmd
    #else
    #    echo "No good alias found."
    fi
}

# Add function to ZSH hook
autoload -U add-zsh-hook
add-zsh-hook preexec suggest_alias
