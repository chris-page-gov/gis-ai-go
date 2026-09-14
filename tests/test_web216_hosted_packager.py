"""Run the offline packager regressions in canonical Python test discovery."""

from pathlib import Path
import subprocess
import unittest


class Web216HostedPackagerTests(unittest.TestCase):
    def test_offline_packager_regressions(self) -> None:
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            ["node", "--test", "tests/test_package_web216_hosted_runtime.mjs"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
