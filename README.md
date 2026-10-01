# Dotfiles

My everyday terminal configuration: Zsh on macOS, Fish on Linux, and a shared set of terminal tools.

One folder per application. Manual symlinks. No installer or platform framework.

## Applications

| Folder | Contents | Source setup |
| --- | --- | --- |
| `zsh/` | Zsh startup files and Powerlevel10k settings | Mac |
| `fish/` | Fish configuration, functions, completions and colors | Linux notebook |
| `ghostty/` | Fonts and cursor shaders | Mac |
| `git/` | Global ignore rules and an optional Git config include | Mac |
| `herdr/` | Agent panel preferences | Mac |
| `hunk/` | Usage note; no configuration to link yet | Mac |
| `projects/` | [Local/SSH project picker](https://github.com/gertyhiler/projects), pinned Git submodule | Shared |
| `nvim/` | [My Neovim configuration](https://github.com/gertyhiler/layzy-nvim), pinned as a Git submodule | Shared |
| `tmux/` | Key bindings, status line and plugin declarations | Mac |

## Requirements

Install only the applications you use. Dependencies are installed separately:

- Zsh: Oh My Zsh in `~/.oh-my-zsh`, Powerlevel10k in its custom themes directory, and the `zsh-syntax-highlighting` and `zsh-autosuggestions` custom plugins. The configuration also uses Homebrew and zoxide. The `colorize` plugin needs Pygments or Chroma. Bun, nvm, Cargo, Go, LM Studio and Obsidian paths reflect the source setup; their application files are not included.
- Fish: fnm for Node.js version management and pnpm for `pn`. `gwl` wraps `git worktree list`. `codex-gcommit` requires the separately configured `git-logical-commit` Codex profile and `git-logical-commits` skill. It explicitly bypasses commit hooks and checks; review its function before using it. Neither dependency is provided by this repository. The Copilot completion file is a generated snapshot.
- Ghostty: the configured FiraCode Nerd Font faces. Bundled cursor shaders retain their upstream license and README.
- tmux: a Nerd Font and TPM at `~/.tmux/plugins/tpm`. The configuration declares `tmux-sensible`. Clipboard bindings currently use macOS `pbcopy`; adapt those commands before using tmux on Linux.
- Neovim: follow the submodule's own README for dependencies.

macOS is the first target for the Zsh and terminal setup. Fish comes from the Linux setup. Configurations are shared where practical, but this repository does not claim identical behavior across operating systems.

## Get the files

Keep the checkout at `~/dotfiles` for the examples below. If cloning it, use `git clone --recurse-submodules <repository-url> ~/dotfiles`.

For an existing checkout:

```sh
cd ~/dotfiles
git submodule update --init --recursive
```

This only downloads the files. It does not activate any configuration.

## Link manually

Run these examples from **Zsh or Bash**. Select the applications you want. Before each `ln -s`, move the existing target to a backup outside this repository. The commands deliberately omit force flags and will fail if a target already exists.

For example, to back up a Zsh file before linking it:

```sh
mv "$HOME/.zshrc" "$HOME/.zshrc.backup-$(date +%Y%m%d-%H%M%S)"
ln -s "$HOME/dotfiles/zsh/.zshrc" "$HOME/.zshrc"
```

Keep the backup until you have opened a new shell and verified the result. To undo a link, remove only that symlink and move its backup back to the original path.

### Zsh

Back up each existing destination first:

```sh
ln -s "$HOME/dotfiles/zsh/.zshrc" "$HOME/.zshrc"
ln -s "$HOME/dotfiles/zsh/.zprofile" "$HOME/.zprofile"
ln -s "$HOME/dotfiles/zsh/.zshenv" "$HOME/.zshenv"
ln -s "$HOME/dotfiles/zsh/.p10k.zsh" "$HOME/.p10k.zsh"
```

### Fish

Link individual files so local Fish state remains outside Git. Back up matching destination files first. Existing unrelated functions and completions remain in place.

```sh
mkdir -p "$HOME/.config/fish/conf.d" "$HOME/.config/fish/functions" "$HOME/.config/fish/completions"
ln -s "$HOME/dotfiles/fish/config.fish" "$HOME/.config/fish/config.fish"
for group in conf.d functions completions; do
  for file in "$HOME/dotfiles/fish/$group/"*.fish; do
    ln -s "$file" "$HOME/.config/fish/$group/$(basename "$file")"
  done
done
```

Colors and key bindings are exported as regular configuration in `conf.d/appearance.fish`. The mutable `fish_variables` file and history are not included. The source setup's `~/.local/bin` path is configured in `config.fish`.

### Ghostty and Neovim

Back up the existing application directories before linking:

```sh
mkdir -p "$HOME/.config"
ln -s "$HOME/dotfiles/ghostty" "$HOME/.config/ghostty"
ln -s "$HOME/dotfiles/nvim" "$HOME/.config/nvim"
```

### tmux and Herdr

Link only configuration files; keep sessions and logs local. Back up existing target files first:

```sh
mkdir -p "$HOME/.config/tmux" "$HOME/.config/herdr"
ln -s "$HOME/dotfiles/tmux/tmux.conf" "$HOME/.config/tmux/tmux.conf"
ln -s "$HOME/dotfiles/herdr/config.toml" "$HOME/.config/herdr/config.toml"
```

### Git

Keep your identity, credentials, signing settings and machine-specific includes in your existing `~/.gitconfig`. Back up the existing ignore file before linking:

```sh
mkdir -p "$HOME/.config/git"
ln -s "$HOME/dotfiles/git/ignore" "$HOME/.config/git/ignore"
```

Git uses this ignore location by default unless `core.excludesFile` overrides it. To select it explicitly, add this include to `~/.gitconfig` once:

```ini
[include]
    path = ~/dotfiles/git/config
```

### Hunk

Nothing to link yet. See [hunk/README.md](hunk/README.md).

## Updating Neovim

The parent repository records an exact Neovim commit. It does not follow the latest upstream revision automatically.

After pulling dotfiles, run `git submodule update --init --recursive` to use its recorded revision. To intentionally select another version:

```sh
git -C ~/dotfiles/nvim fetch origin
git -C ~/dotfiles/nvim checkout <reviewed-commit-or-tag>
git -C ~/dotfiles add nvim
```

Review and commit the updated submodule pointer in dotfiles. If you edit Neovim itself, create a branch in that submodule, commit and publish its changes first, then update the parent pointer.

## What stays local

Credentials, shell history, logs, caches, sessions, generated Fish state and Git identity are not part of this repository. Avoid linking an application's entire state directory when a file-level link is enough.

## Projects and worktrees

`gwl` lists worktrees, `gw` picks one and changes directory, and `gwn` picks one
and opens Neovim. `gw /absolute/path` and `gwn /absolute/path` skip the picker.
These functions need Git and fzf, and work without the projects CLI.

Zsh: link `zsh/projects.zsh` to `~/.config/zsh/projects.zsh`; the tracked `.zshrc`
sources it. If keeping your own `.zshrc`, add that source line manually.
Fish: link `fish/functions/gw.fish`, `gwn.fish`, and `gwl.fish` individually into
`~/.config/fish/functions/`. Preserve unrelated machine configuration.

The separate `projects` submodule provides `p`: one local/SSH project picker
with recent history and optional Herdr opening. Initialize it, then link manually:

```sh
git submodule update --init projects
mkdir -p ~/.local/bin ~/.config/projects
ln -s "$HOME/dotfiles/projects/p" "$HOME/.local/bin/p"
```

Configure each machine using the submodule README. Machine names, SSH aliases,
project roots, cache and history stay local and are not committed. The standalone
shell functions can be reused with the documented `opener` configuration.

The Zsh worktree picker has a real-terminal regression test (requires Python 3,
Zsh, Git and fzf): `python3 -m unittest discover -s zsh/tests -v`.

The Zsh `projects.zsh` file also defines `p`; Fish users should link
`fish/functions/p.fish` into `~/.config/fish/functions/`. This wrapper keeps a
selected local directory in the calling shell after the editor exits. Reload
Zsh with `source ~/.config/zsh/projects.zsh` in existing terminals. The standalone
`command p` executable cannot change its parent shell directory.
