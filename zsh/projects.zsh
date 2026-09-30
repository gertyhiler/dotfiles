# Standalone worktree navigation. No projects CLI dependency.
unalias gw gwl gwn 2>/dev/null
function gwl() {
  command git worktree list "$@"
}
function gw() {
  local dir field
  local -a worktrees
  if (( $# > 1 )); then
    print -u2 'usage: gw [directory]'
    return 2
  fi
  if (( $# == 1 )); then
    dir=$1
    command git -C "$dir" rev-parse --git-dir >/dev/null 2>&1 || return 1
  else
    command git rev-parse --git-dir >/dev/null 2>&1 || return 1
    while IFS= read -r -d '' field; do
      [[ $field == 'worktree '* ]] && worktrees+=("${field#worktree }")
    done < <(command git worktree list --porcelain -z)
    (( ${#worktrees} )) || return 1
    dir=$(
      printf '%s\0' "${worktrees[@]}" |
        FZF_DEFAULT_OPTS='' FZF_DEFAULT_OPTS_FILE=/dev/null command fzf --read0 --print0 --height=80% --layout=reverse --prompt='worktree> '
    ) || return 1
    dir=${dir%$'\0'}
  fi
  [[ -n $dir ]] || return 1
  builtin cd -- "$dir"
}
function gwn() {
  gw "$@" && command nvim .
}
