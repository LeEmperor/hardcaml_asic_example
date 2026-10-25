"""EDA-less CLI integration tests; reads source/Git, never mutates the checkout.

Usage: python3 -B scripts/test_flow_emit.py /absolute/project.exe /source/checkout
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


EXE, SOURCE = (Path(p).resolve(strict=True) for p in sys.argv[1:3])
sys.argv[1:] = []


class FlowEmitTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="flow-emit-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.results = self.root / "results"
        self.bin = self.root / "bin"
        self.bin.mkdir()
        # Git is the sole external dependency of source capture. No provider or
        # EDA executable is on PATH; TOOLCHAIN deliberately names a missing path.
        (self.bin / "git").symlink_to(shutil.which("git"))
        self.env = dict(os.environ, PATH=str(self.bin),
                        TOOLCHAIN=str(self.root / "nonexistent-toolchain"))
        for key in list(self.env):
            if key.startswith("GIT_"):
                del self.env[key]

    def invoke(self, command, *args, status=0, root_option="--source-root"):
        result = subprocess.run(
            [str(EXE), "flow", command, root_option, str(SOURCE),
             "--endpoint", "synthesis", "--json", *args],
            cwd=self.root, env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, status, (args, result.stdout, result.stderr))
        return json.loads(result.stdout) if status == 0 else result

    def emit(self, *args, **kwargs):
        return self.invoke("emit", "--results-root", "results", *args, **kwargs)

    def assert_contract(self, response, plan):
        self.assertEqual(type(response["schema_version"]), int)
        self.assertEqual(response["schema_version"], 1)
        self.assertEqual(response["kind"], "bundle_emission")
        self.assertEqual(type(response["reused"]), bool)
        self.assertEqual(response["plan"], plan)
        for key in ("bundle_identity", "plan_identity"):
            self.assertEqual(response[key], plan[key])
            self.assertRegex(response[key], r"^[0-9a-f]{64}$")
        output = Path(response["output_dir"])
        self.assertTrue(output.is_absolute())
        self.assertEqual(output.parent, self.results / "bundles")
        self.assertEqual(json.loads((output / "manifest.json").read_text()),
                         json.loads(plan["bundle_manifest"]))
        # Publication only: no launchspec, workspace, checkpoint or attempt store.
        self.assertEqual(sorted(p.name for p in self.results.iterdir()), ["bundles"])

    def test_deterministic_publication_and_reuse_without_provider_or_tools(self):
        plan = self.invoke("plan")
        self.assertFalse(self.results.exists())
        first = self.emit("--expected-plan-identity", plan["plan_identity"])
        self.assert_contract(first, plan)
        self.assertFalse(first["reused"])
        second = self.emit(root_option="--project-root")
        self.assert_contract(second, plan)
        self.assertEqual(second, dict(first, reused=True))

    def test_selected_profile_and_repeatable_overrides(self):
        selection = ["--flow", "standard", "--profile", "synth_delay"]
        profile = self.invoke("plan", *selection)
        overridden = [*selection, "--set", "SYNTH_STRATEGY=AREA 0",
                      "--set", "SYNTH_ABC_BUFFERING=true"]
        plan = self.invoke("plan", *overridden)
        response = self.emit(*overridden, "--expected-plan-identity", plan["plan_identity"])
        self.assert_contract(response, plan)
        self.assertEqual(plan["methodology"]["snapshot"]["selected"],
                         {"flow": "standard", "profile": "synth_delay"})
        self.assertNotEqual(profile["plan_identity"], plan["plan_identity"])
        config = json.loads(plan["configuration_bytes"])
        self.assertEqual(config["SYNTH_STRATEGY"], "AREA 0")
        self.assertIs(config["SYNTH_ABC_BUFFERING"], True)
        for parameter in plan["methodology"]["effective_parameters"]:
            self.assertEqual(parameter["winning"]["owner"]["kind"], "request")
            self.assertEqual(parameter["overridden"][0]["owner"]["kind"], "profile")
        baseline = self.invoke("plan")
        self.assertEqual(baseline["methodology"]["snapshot"]["selected"]["profile"], "balanced")
        self.assertEqual(self.invoke("plan", "--flow", "standard"), baseline)

    def test_mismatch_before_publication(self):
        plan = self.invoke("plan")
        for args in (("--expected-plan-identity", "0" * 64),
                     ("--flow", "standard", "--profile", "synth_delay",
                      "--expected-plan-identity", plan["plan_identity"])):
            result = self.emit(*args, status=1)
            self.assertIn("identity", result.stderr.lower())
            self.assertFalse(self.results.exists())

    def test_invalid_inputs_before_publication(self):
        cases = [(["--expected-plan-identity", "bad"], 2),
                 (["--flow", "missing"], 1),
                 (["--profile", "balanced"], 2),
                 (["--flow", "standard", "--profile", "missing"], 1),
                 (["--set", "SYNTH_ABC_BUFFERING=1"], 2),
                 (["--set", "SYNTH_STRATEGY=invalid"], 2),
                 (["--set", "SYNTH_ABC_BUFFERING=true", "--set", "SYNTH_ABC_BUFFERING=false"], 2)]
        for args, status in cases:
            with self.subTest(args=args):
                self.emit(*args, status=status)
                self.assertFalse(self.results.exists())
        for option in ("--provider", "--toolchain", "--support-tools", "--pdk-root", "--python",
                       "--timeout", "--workspace", "--bundle", "--output-dir"):
            self.emit(option, "nonexistent", status=2)
            self.assertFalse(self.results.exists())

    def test_provider_and_tool_traps_are_never_launched(self):
        log = self.root / "launched"
        for name in ("hardcaml-asic-flow", "yosys", "openroad", "librelane", "python", "python3"):
            trap = self.bin / name
            trap.write_text(f"#!/bin/sh\nprintf '%s\\n' '{name}' >> '{log}'\nexit 99\n")
            trap.chmod(0o755)
        self.emit()
        self.assertFalse(log.exists())
        self.assertEqual(sorted(p.name for p in self.results.iterdir()), ["bundles"])


if __name__ == "__main__":
    unittest.main()
