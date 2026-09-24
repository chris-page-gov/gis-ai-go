"""Plain-English prerequisite failures before starting any runtime or build."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Local214LauncherTests(unittest.TestCase):
    def test_missing_and_wrong_prerequisites_stop_before_build(self) -> None:
        cases = [
            ({}, "Missing node"),
            ({"node": "exit 1", "pnpm": "exit 0", "uv": "exit 0"}, "Node.js 24.19.0"),
            ({"node": "exit 0", "pnpm": "printf '9.0.0\\n'", "uv": "exit 0"}, "pinned pnpm 10.33.2"),
            ({"node": "exit 0", "pnpm": "printf '10.33.2\\n'", "uv": "printf 'uv 0.1.0\\n'"}, "pinned uv 0.12.2"),
            ({"node": "exit 0", "pnpm": "printf '10.33.2\\n'",
              "uv": 'if [ "$1" = "--version" ]; then printf "uv 0.12.2\\n"; else exit 1; fi'}, "Prepare Python 3.12"),
            ({"node": "exit 0", "pnpm": "printf '10.33.2\\n'",
              "uv": 'if [ "$1" = "--version" ]; then printf "uv 0.12.2 (distribution build)\\n"; else exit 1; fi'}, "Prepare Python 3.12"),
        ]
        for commands, expected in cases:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory(prefix="local214-prerequisites-") as temporary:
                directory = Path(temporary)
                (directory / "dirname").symlink_to("/usr/bin/dirname")
                for name, body in commands.items():
                    command = directory / name
                    command.write_text(f"#!/bin/sh\n{body}\n")
                    command.chmod(0o755)
                result = subprocess.run(["/bin/sh", str(ROOT / "scripts/start-local-candidate")],
                                        cwd=ROOT, env={**os.environ, "PATH": temporary},
                                        capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 1)
                self.assertIn(expected, result.stderr)


if __name__ == "__main__":
    unittest.main()
