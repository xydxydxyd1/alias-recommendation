# preexec ZSH hook for suggesting aliases

#rm ./suggest_real_time.log

local input_matcher="(^[^=]+)=(.+)$"


get_alias_keys() {
    alias_keys=""
    for k in "${(@k)aliases}"; do
        alias_keys="$alias_keys\n$k"
    done
    echo $alias_keys
}


get_alias_vals() {
    alias_vals=""
    for k in "${(@k)aliases}"; do
        alias_vals="$alias_vals\n${aliases[$k]}"
    done
    echo "$alias_vals"
    echo $alias_vals
}


suggest_alias() {
    local suggest_cmd='python3 ./suggest_real_time.py "$(history "-10" | cut -c 8-)" "$(alias)" --ignored_cmds "$IGNORED_ALIAS" --min_rating 25'
    local suggested_alias_cmd=$(eval $suggest_cmd)
    local output_matcher="^alias ([a-zA-Z0-9_]+)=\\$'(.*)'$"
    if [[ "$suggested_alias_cmd" =~ $output_matcher ]]; then
        local alias_name="${match[1]}"
        local alias_value="${match[2]}"
        echo "Suggested alias: $alias_name='$alias_value'"
        read "yn?Do you want to create this alias for this window? [y/n]"
        if ! [[ "$yn" =~ ^[Yy]$ ]]; then
            echo 'Alias not created and will not be suggested again.'
            export IGNORED_ALIAS="$alias_value\n$IGNORED_ALIAS"
            return
        fi
        echo "Creating $suggested_alias_cmd"
        eval $suggested_alias_cmd
    else
        echo "No good alias found."
        echo "Output of suggest_cmd: $suggested_alias_cmd"
    fi
}

# Add function to ZSH hook
#autoload -U add-zsh-hook
#add-zsh-hook preexec suggest_alias
