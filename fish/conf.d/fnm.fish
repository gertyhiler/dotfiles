# Initialize fnm only in interactive shells where it is installed.
if status is-interactive
    fish_add_path --global "$HOME/.local/share/fnm"
    if command -q fnm
        fnm env --use-on-cd --shell fish | source
    end
end
