# preexec ZSH hook for suggesting aliases

suggest_alias() {
    suggest_cmd='python3 ./suggest_real_time.py "$(history "-50" | cut -c 8-)" "$(alias)" --ignored_cmds "$IGNORED_ALIAS"'
    suggested_alias_cmd=$(eval $suggest_cmd)
    matcher="^alias ([a-zA-Z0-9_]+)='(.*)'$"
    if [[ "$suggested_alias_cmd" =~ $matcher ]]; then
        alias_name="${match[1]}"
        alias_value="${match[2]}"
        echo "Suggested alias: $alias_name='$alias_value'"
        read "yn?Do you want to create this alias for this window? [y/n]"
        if ! [[ "$yn" =~ ^[Yy]$ ]]; then
            echo 'Alias not created and will not be suggested again.'
            export IGNORED_ALIAS="$alias_value\n$IGNORED_ALIAS"
            return
        fi
        echo "Creating alias $alias_name='$alias_value'"
        eval $suggested_alias_cmd
    else
        echo "No good alias found."
    fi
}
