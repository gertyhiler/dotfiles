if set -q SSH_CONNECTION; and status is-login; and not status is-interactive
    # VS Code Remote-SSH sends a POSIX shell bootstrap script over ssh -T.
    # Hand non-interactive SSH login sessions to bash so fish does not parse it.
    exec /usr/bin/bash -s
end

set -gx PATH $HOME/.local/bin $PATH
