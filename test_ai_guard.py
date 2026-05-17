import tempfile
from pathlib import Path
from scripts.quality.ai_code_guard import scan_file

def test_detect_eval():
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.py') as f:
        f.write("x = eval('1 + 1')\n")
        temp_path = Path(f.name)
    try:
        issues = scan_file(temp_path)
        assert any('eval' in issue for issue in issues)
    finally:
        temp_path.unlink()

def test_detect_subprocess_shell():
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.py') as f:
        f.write("import subprocess\nsubprocess.run('ls', shell=True)\n")
        temp_path = Path(f.name)
    try:
        issues = scan_file(temp_path)
        assert any('shell=True' in issue for issue in issues)
    finally:
        temp_path.unlink()