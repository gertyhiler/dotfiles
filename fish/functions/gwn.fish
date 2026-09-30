function gwn --description 'Pick a Git worktree and open Neovim'
    gw $argv; and command nvim .
end
