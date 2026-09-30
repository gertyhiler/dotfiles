"""Exercise gw with real terminal job control and fzf (macOS/Linux)."""
import fcntl
import os
from pathlib import Path
import pty
import select
import shlex
import shutil
import signal
import struct
import subprocess
import tempfile
import termios
import time
import unittest


@unittest.skipUnless(shutil.which('zsh') and shutil.which('fzf'), 'requires zsh and fzf')
class InteractiveWorktreeTest(unittest.TestCase):
    def test_select_and_cancel(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            repo, tree = root/'repo', root/'selected worktree'
            env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
            env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1', TERM='xterm-256color')
            def git(*args):
                subprocess.run(['git', *map(str, args)], check=True, env=env, capture_output=True)
            git('init', '-b', 'main', repo)
            git('-C', repo, '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                'commit', '--allow-empty', '-m', 'fixture')
            git('-C', repo, 'worktree', 'add', '-b', 'selected', tree)
            pid, fd = pty.fork()
            if pid == 0:
                os.chdir(repo)
                os.execvpe('zsh', ['zsh', '-f'], env)
            try:
                fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack('HHHH', 24, 120, 0, 0))
                def wait_for(marker):
                    output = b''
                    until = time.monotonic() + 10
                    while marker not in output and time.monotonic() < until:
                        if select.select([fd], [], [], .1)[0]:
                            chunk = os.read(fd, 65536)
                            output += chunk
                            if b'\x1b[6n' in chunk:
                                os.write(fd, b'\x1b[1;1R')
                    self.assertIn(marker, output, repr(output[-2000:]))
                source = Path(__file__).resolve().parents[1]/'projects.zsh'
                os.write(fd, ('source '+shlex.quote(str(source))+"; gw; printf '\\nDONE:%s\\n' \"$PWD\"\n").encode())
                wait_for(b'worktree>')
                os.write(fd, b'selected worktree$')
                time.sleep(.2)
                os.write(fd, b'\r')
                wait_for(('DONE:'+str(tree)).encode())
                os.write(fd, b"gw; printf '\\nCANCEL:%s:%s\\n' \"$?\" \"$PWD\"\n")
                wait_for(b'worktree>')
                os.write(fd, b'\x1b')
                wait_for(('CANCEL:1:'+str(tree)).encode())
            finally:
                os.killpg(pid, signal.SIGKILL)
                os.close(fd)
                os.waitpid(pid, 0)


if __name__ == '__main__':
    unittest.main()
