import os
import subprocess
import sys
from pathlib import Path


def test_docs_examples_run():
    repo = Path(__file__).resolve().parents[4]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo / "python")
    env["LD_LIBRARY_PATH"] = os.pathsep.join([
        "/tmp/nimblephysics-deps/usr/lib/x86_64-linux-gnu",
        "/tmp/nimblephysics-deps/draco-root/usr/lib/x86_64-linux-gnu",
        "/tmp/nimblephysics-deps/minizip-root/usr/lib/x86_64-linux-gnu",
        "/tmp/nimblephysics-deps/ezc3d-install/lib/ezc3d",
        env.get("LD_LIBRARY_PATH", ""),
    ]).strip(os.pathsep)

    examples = [
        repo / "python" / "new_examples" / "docs_quick_start.py",
        repo / "python" / "new_examples" / "docs_optimization.py",
    ]
    for example in examples:
        subprocess.check_call([sys.executable, str(example)], cwd=repo, env=env)
