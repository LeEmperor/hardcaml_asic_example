"""Cheap actual CLI checks: no Git, emission, or EDA needed."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    executable = Path(sys.argv[1]).resolve(strict=True)
    with tempfile.TemporaryDirectory(prefix="project-cli-") as directory:
        root = Path(directory)
        output = root / "must-not-exist"
        env = dict(os.environ, PATH="", GIT_DIR=str(root / "no-git"))

        def check(args, status):
            result = subprocess.run([str(executable), *args], cwd=root, env=env,
                                    capture_output=True, text=True)
            assert result.returncode == status, (args, result)
            assert list(root.iterdir()) == [], (args, "unexpected filesystem output")
            return result

        description = check(["describe"], 0).stdout
        for fact in ("controlled_fifo_specimen", "tt_um_controlled_fifo", "clk",
                     "timing", "pinout", "policy", "source_inputs"):
            assert fact in description, (fact, description)
        for args in ([], ["unknown"], ["describe", "extra"], ["emit"],
                     ["emit", "--source-root", str(root)],
                     ["emit", "--output-dir", str(output)],
                     ["describe", "--output-dir", str(output)],
                     ["emit", "--source-root", str(root), "--output-dir", str(output), "--bogus"],
                     ["--source-root", str(root), "--output-dir", str(output)]):
            result = check(args, 2)
            assert "project" in result.stderr and "Bundle emission failed" not in result.stderr
        for args in (["--help"], ["emit", "--help"]):
            assert "project" in check(args, 0).stdout
    print("PASS CLI: declaration-only description without Git/PATH; help and invalid commands; no output created")


if __name__ == "__main__":
    main()
