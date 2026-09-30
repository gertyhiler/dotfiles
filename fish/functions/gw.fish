function gw --description 'Pick a Git worktree and change directory'
    if test (count $argv) -gt 1
        echo 'usage: gw [directory]' >&2
        return 2
    end
    set -l dir
    if test (count $argv) -eq 1
        set dir "$argv[1]"
        command git -C "$dir" rev-parse --git-dir >/dev/null 2>&1; or return 1
    else
        command git rev-parse --git-dir >/dev/null 2>&1; or return 1
        set dir (command git worktree list --porcelain -z | while read -lz field
            if string match -q 'worktree *' -- "$field"
                set -l parts (string split -m 1 ' ' -- "$field")
                printf '%s\0' "$parts[2]"
            end
        end | env FZF_DEFAULT_OPTS= FZF_DEFAULT_OPTS_FILE=/dev/null fzf --read0 --print0 --height=80% --layout=reverse --prompt='worktree> ' | string split0)
        test (count $dir) -eq 1; or return 1
    end
    test -n "$dir"; or return 1
    builtin cd -- "$dir"
end
