"""Verify retained PT.5 test logs/identities and write a new closeout receipt.

This records existing executions; it does not run a suite or reconcile resources.
Run from the example root with python3 -B. The destination must not exist.
"""
import ast
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from check_resource_evidence import historical_hashes, load, sha


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--final", action="store_true", help="record corrected frozen-provider run; preserve old closeout")
    args = parser.parse_args()
    directory = ROOT / "acceptance/resource-realization"
    destination = directory / ("closeout-final.json" if args.final else "closeout.json")
    focused_path = "installed-final/verified/receipt.json" if args.final else "installed-04/receipt.json"
    provider_log = "provider-final.stdout" if args.final else "provider-capture.stdout"
    fifo_log_path = "fifo-final.stderr" if args.final else "fifo-flow-emit.stderr"
    suite_log_path = "suite-final.stderr" if args.final else "example-suite.stderr"
    if destination.exists():
        raise RuntimeError("closeout destination must be new")
    assertions = []

    def check(name, actual, expected):
        assertions.append(dict(assertion=name, actual=actual, expected=expected,
                               passed=actual == expected))
        if actual != expected:
            raise AssertionError(assertions[-1])

    focused = load(directory / focused_path)
    check("focused unittest cases", focused["tests_run"], 20 if args.final else 18)
    check("focused failures", focused["failures"], 0)
    check("focused errors", focused["errors"], 0)
    check("focused skips", focused["skipped"], [])
    check("public acceptance", focused["public_api_acceptance"], "passed")
    check("all captured public command exits", all(command["exit"] == command["expected_exit"]
                                                   for command in focused["commands"]), True)
    check("tested script digest", sha(ROOT / "scripts/check_resource_evidence.py"), focused["script_sha256"])
    original = load(directory / "research.json")["historical_files_before"]
    current = historical_hashes()
    check("historical files preserved since first independent research", current, original)
    provider = load(directory / provider_log)
    check("captured provider receipt", focused["provider_receipt"], provider)
    for key, identity in focused["executable_ids"].items():
        check(key + " executable digest", sha(Path(identity["path"])), identity["sha256"])
    fifo_log = (directory / fifo_log_path).read_text()
    check("FIFO standalone test count", re.findall(r"Ran (\d+) tests", fifo_log), ["5"])
    check("FIFO unittest success", fifo_log.rstrip().endswith("OK"), True)
    syntax = ast.parse((ROOT / "scripts/test_flow_emit.py").read_text())
    fifo_tests = [node.name for cls in syntax.body if isinstance(cls, ast.ClassDef)
                  for node in cls.body if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]
    check("FIFO source test names", len(fifo_tests), 5)
    suite = (directory / suite_log_path).read_text()
    check("broader Python unittest group counts", re.findall(r"Ran (\d+) tests", suite), ["11", "24", "21"])
    check("broader unittest success groups", len(re.findall(r"^OK$", suite, re.MULTILINE)), 3)
    check("installed provider routing exercised", "test_named_installed_native_early_reference_and_request" in suite, True)
    for marker in ("PASS directed: edges=7330", "PASS seed=20261012 cycles=20000",
                   "PASS memory Flops Simulation", "PASS memory Flops Implementation",
                   "PASS memory Exact Simulation", "PASS policy:", "PASS wrapper directed:",
                   "PASS wrapper seed=20261012", "PASS resolution:", "PASS project catalog:",
                   "PASS bundle:", "synthesis: PASS RTL edges=11429",
                   "simulation: PASS RTL edges=11429",
                   "synthesis: PASS negative oracle rejected", "simulation: PASS negative oracle rejected"):
        check("broader suite outcome: " + marker, marker in suite, True)
    selections = {}
    for name in ("asic", "asic-prepare", "asic-sram", "asic-workbench"):
        pointer = ROOT / ".dev" / name / "current"
        check(name + " selection pointer predates initial research",
              pointer.lstat().st_mtime_ns < (directory / "research.json").stat().st_mtime_ns, True)
        selections[name] = dict(generation=str(pointer.resolve()), receipt_sha256=sha(pointer / "receipt.json"))
    if args.final:
        previous = load(directory / "closeout.json")
        check("normal provider selections unchanged since original acceptance", selections,
              previous["preserved_provider_selections"])
        old_artifacts = {path: entry["sha256"] for path, entry in previous["artifact_hashes"].items()
                         if path.startswith("installed-04/")}
        check("entire installed-04 capture preserved", {path: sha(directory / path) for path in old_artifacts}, old_artifacts)
        check("old provider immutable generation receipt preserved",
              load(Path(previous["provider_receipt"]["generation"]) / "receipt.json"), previous["provider_receipt"])
        check("corrected provider source capture differs from superseded capture",
              provider["snapshot_sha256"] != previous["provider_receipt"]["snapshot_sha256"], True)
    commands = [
        dict(command="opam exec --switch=5.2.0+ox -- python3 -B scripts/asic_dependency.py --store .dev/asic-pt5 refresh --source /home/wayne/devel/jane/hardcaml_asic --mode development --jobs 6",
             stdout="provider-capture.stdout", stderr="provider-capture.stderr", exit=0),
        dict(command="opam exec --switch=5.2.0+ox -- bash -c 'source .dev/asic-pt5/current/activate.sh && dune build --build-dir _build_pt5 -j6 @all'",
             stdout="example-build.stdout", stderr="example-build.stderr", exit=0),
        dict(command="opam exec --switch=5.2.0+ox -- bash -c 'source .dev/asic-pt5/current/activate.sh && dune build --build-dir _build_pt5 -j6 acceptance/resource-realization/installed_api.exe'",
             stdout="api-build.stdout", stderr="api-build.stderr", exit=0),
        dict(command="python3 -B scripts/test_flow_emit.py /home/wayne/devel/jane/hardcaml_asic_example/_build_pt5/default/bin/project.exe /home/wayne/devel/jane/hardcaml_asic_example",
             stdout="fifo-flow-emit.stdout", stderr="fifo-flow-emit.stderr", exit=0),
        dict(command='opam exec --switch=5.2.0+ox -- bash -c \'source .dev/asic-pt5/current/activate.sh && HARDCAML_ASIC_TEST_PROVIDER="$HARDCAML_ASIC_GENERATION/bin/hardcaml-asic-flow" dune runtest --build-dir _build_pt5 -j6 .\'',
             stdout="example-suite.stdout", stderr="example-suite.stderr", exit=0),
    ]
    if args.final:
        commands = [commands[0], commands[1], commands[3], commands[4]]
        for command, stdout, stderr in zip(commands,
                ("provider-final.stdout", "build-final.stdout", "fifo-final.stdout", "suite-final.stdout"),
                ("provider-final.stderr", "build-final.stderr", "fifo-final.stderr", "suite-final.stderr")):
            command.update(stdout=stdout, stderr=stderr)
        commands[-1]["command"] = commands[-1]["command"].replace("-j6 .", "-j6 --force .")
    artifact_hashes = {str(path.relative_to(directory)): dict(sha256=sha(path), bytes=path.stat().st_size)
                       for path in sorted(directory.rglob("*")) if path.is_file() and path != destination}
    receipt = dict(scope="PT.5 C installed-provider acceptance closeout; no physical EDA",
                   provider_receipt=provider, assertions=assertions,
                   focused_receipt=focused_path, focused_commands=len(focused["commands"]),
                   focused_exit_counts=dict(Counter(str(command["exit"]) for command in focused["commands"])),
                   commands=commands, fifo_tests_passed=fifo_tests,
                   broader_outcomes=[line for line in suite.splitlines() if "PASS" in line or line == "OK"],
                   preserved_provider_selections=selections, historical_file_count=len(current),
                   example_revision=(previous["example_revision"] if args.final else
                                     subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()),
                   source_and_executable_ids={str(path.relative_to(ROOT)): sha(path) for path in [
                       ROOT / "asic-dependency.json", ROOT / "bin/project.ml", ROOT / "bin/dune",
                       ROOT / "memory/memory_cli.ml", ROOT / "scripts/test_flow_emit.py",
                       ROOT / "scripts/asic_dependency.py", ROOT / "_build_pt5/default/bin/project.exe",
                       ROOT / "acceptance/resource-realization/installed_api.ml"]},
                   artifact_hashes=artifact_hashes,
                   constraints=dict(jobs=6, example_dune_serialized=True, physical_eda=False,
                                    provider_build="private captured source, distinct from ASIC checkout Dune"),
                   limitations=focused["unavailable"],
                   earlier_attempts={"installed-01": "fixture collect layout: project manifest not staged",
                                     "installed-02": "fixture archive output treated as tar instead of archive directory",
                                      "installed-03": "17 tests passed before additional tamper/area coverage"})
    if args.final:
        receipt.update(supersedes=dict(closeout="closeout.json", focused_receipt="installed-04/receipt.json",
                                       generation=previous["provider_receipt"]["generation"],
                                       source_sha256=previous["provider_receipt"]["snapshot_sha256"],
                                       reason="A/B independent-review corrections; old derived schema lacks resource_inventory"),
                       harness_adjustment=dict(receipt="installed-final/receipt.json",
                                               reason="undefined wrong-type module rejects before a complete unexpected-instance inventory"))
    with destination.open("x") as stream:
        json.dump(receipt, stream, indent=2)
        stream.write("\n")
    print(f"Closeout: {len(assertions)} recorded assertions passed; {len(current)} historical files preserved")
    print(f"Focused public commands: {len(focused['commands'])}; exit counts: {receipt['focused_exit_counts']}")


if __name__ == "__main__":
    main()
