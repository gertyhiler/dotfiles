function p --description 'Choose a project, change directory and open it'
    if set -q PROJECTS_CONFIG; and test -n "$PROJECTS_CONFIG"; and not string match -q '/*' -- "$PROJECTS_CONFIG"
        set -fx PROJECTS_CONFIG "$PWD/$PROJECTS_CONFIG"
    end
    set -l result (mktemp)
    or return 1
    command p --shell-result "$result" $argv
    set -l code $status
    if test $code -eq 0; and test -s "$result"
        set -l dir
        read -lz dir < "$result"
        command rm -f -- "$result"
        builtin cd -- "$dir"; or return
        command p --open-local "$dir" --backend direct
        return $status
    end
    command rm -f -- "$result"
    return $code
end
