import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]

class ShellIntegrationTests(unittest.TestCase):
    def test_caller_directory_survives_editor_and_cancellation(self):
        for shell in ('zsh', 'fish'):
            if not shutil.which(shell):
                continue
            with self.subTest(shell=shell), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp).resolve()
                target = root / 'project with spaces\nand newline'
                target.mkdir()
                cli = root / 'p'
                cli.write_text('''#!/usr/bin/env python3
import os,sys
from pathlib import Path
a=sys.argv[1:]
if '--shell-result' in a:
    if 'cancel' not in a:
        Path(a[a.index('--shell-result')+1]).write_bytes(os.fsencode(os.environ['TARGET'])+b'\\0')
elif '--open-local' in a:
    assert os.getcwd()==os.environ['TARGET']
    Path(os.environ['MARKER']).write_text('editor ran')
''')
                cli.chmod(0o755)
                source = ROOT / ('zsh/projects.zsh' if shell == 'zsh' else 'fish/functions/p.fish')
                script = 'source "$SOURCE"; p; pwd > "$AFTER"; p cancel; pwd > "$CANCEL"'
                env = dict(os.environ, PATH=str(root)+':'+os.environ['PATH'], TARGET=str(target),
                           SOURCE=str(source), MARKER=str(root/'marker'), AFTER=str(root/'after'), CANCEL=str(root/'cancel'))
                subprocess.run([shell, '-f' if shell=='zsh' else '--no-config', '-c', script], env=env, cwd=root, check=True)
                self.assertEqual((root/'after').read_text(), str(target)+'\n')
                self.assertEqual((root/'cancel').read_text(), str(target)+'\n')
                self.assertEqual((root/'marker').read_text(), 'editor ran')

if __name__ == '__main__':
    unittest.main()
