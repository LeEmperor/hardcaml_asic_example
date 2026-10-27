#!/usr/bin/env python3
"""PT.5 retained-evidence oracle and installed public-provider acceptance.

Run standalone: python3 -B scripts/check_resource_evidence.py --research-only
    --receipt acceptance/resource-realization/research.json
The optional receipt must be new. This is a unittest receipt, not resource_evidence.
For public acceptance supply --provider, --consumer (installed_api.exe), --memory,
and a new --output-dir beneath acceptance/resource-realization. Public responses,
mutation digests and test outcomes are retained there. No EDA, provider discovery,
historical writes, or Dune operations are performed by this script.
"""
import argparse
from collections import Counter
import copy
from decimal import Decimal
import hashlib
import io
import json
from pathlib import Path
import re
import os
import shutil
import subprocess
import sys
import tempfile
import tarfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRAM = ROOT / "acceptance/sram"
SYNTH = SRAM / "8b48d7d0-functional"
PHYSICAL = SRAM / "physical-p4"
TOP = "tt_um_program_memory"
MACRO = "RM_IHPSG13_1P_256x16_c2_bm_bist"
INSTANCE = "hc_resource_7_program"
CASES = (
    (SYNTH, "manifest.json", "8b48d7d0818d494f8a9c45000c2bcbbd",
     "4fe842a7c07b94ae9e8e0546210c9273d019fccdca2d5cbf84311948bde64d09", "synthesis"),
    (PHYSICAL, "bundle/manifest.json", "be961b2c95f74c81ad6af81ca4d2b269",
     "fa38d9064dffdf2ec1578c79c2e8890eba81bf704af460e85fcc6031b707d53c", "full"),
)


def load(path):
    return json.loads(path.read_text())


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def historical_hashes():
    return {str(path.relative_to(ROOT)): sha(path)
            for root in (SYNTH, PHYSICAL)
            for path in sorted(root.rglob("*")) if path.is_file()}


def mapped_mutation(original, kind):
    """Mutate a decoded disposable copy, never a historical path or manifest.

    The unchanged stat count intentionally tests that aggregate counts cannot hide
    identity/type errors. On resume, feed each fixture to B's public inspector;
    these constructors alone DO NOT establish required-macro rejection.
    """
    mutated = copy.deepcopy(original)
    cells = mutated["modules"][TOP]["cells"]
    if kind == "missing":
        del cells[INSTANCE]
    elif kind == "extra":
        cells[INSTANCE + "_extra"] = copy.deepcopy(cells[INSTANCE])
    elif kind == "renamed":
        cells[INSTANCE + "_renamed"] = cells.pop(INSTANCE)
    elif kind == "wrong_type":
        cells[INSTANCE]["type"] = "RM_IHPSG13_1P_wrong_type"
    elif kind == "empty":
        cells.clear()
    else:
        raise ValueError(kind)
    return mutated


class RetainedResearch(unittest.TestCase):
    def test_historical_checksum_inventories(self):
        for root, *_ in CASES:
            entries = load(root / "checksums.json")
            self.assertEqual(len(entries), len({entry["path"] for entry in entries}))
            for entry in entries:
                with self.subTest(root=root.name, artifact=entry["path"]):
                    path = (root / entry["path"]).resolve()
                    self.assertTrue(path.is_relative_to(root.resolve()))
                    self.assertEqual(sha(path), entry["sha256"])

    def test_run_bundle_identity_and_real_completed_stage(self):
        for root, manifest_path, run_id, identity, stage in CASES:
            with self.subTest(run=run_id):
                manifest = load(root / manifest_path)
                payload = {key: value for key, value in manifest.items() if key != "identity"}
                digest = hashlib.sha256(json.dumps(payload, separators=(",", ":"),
                                                  ensure_ascii=False).encode()).hexdigest()
                self.assertEqual(digest, identity)
                self.assertEqual(manifest["identity"], identity)
                run = load(root / "run.json")
                self.assertEqual((run["run_id"], run["build_identity"], run["completed_stage"],
                                  run["status"]), (run_id, identity, stage, "completed"))
                self.assertNotIn("resource_snapshot", manifest)
                macro, = manifest["macro_contract"]["macros"]
                self.assertEqual((macro["resource"], macro["module"], macro["instance"]),
                                 ("program", MACRO, INSTANCE))

    def test_synthesis_instance_inventory_and_standard_cell_count(self):
        for root, *_ in CASES:
            with self.subTest(root=root.name):
                cells = load(root / "mapped.json")["modules"][TOP]["cells"]
                types = Counter(cell["type"] for cell in cells.values())
                self.assertEqual({name: cell["type"] for name, cell in cells.items()
                                  if not cell["type"].startswith("sg13cmos5l_")},
                                 {INSTANCE: MACRO})
                self.assertEqual((len(cells), types[MACRO], len(cells) - types[MACRO]),
                                 (176, 1, 175))
                self.assertEqual(types["sg13cmos5l_dfrbpq_1"], 16)
        stat = load(SYNTH / "stat.json")["design"]
        self.assertEqual(stat["num_cells"], 176)
        self.assertEqual(dict(types), stat["num_cells_by_type"])

    def test_synthesis_area_inclusion_and_liberty_binding(self):
        stat = load(SYNTH / "stat.json")["design"]
        log = (SYNTH / "synthesis.log").read_text()
        self.assertIn("Area for cell type \\" + MACRO + " is unknown!", log)
        liberty = (SYNTH / "models" / (MACRO + "_typ_1p20V_25C.lib")).read_text()
        self.assertEqual(re.findall(r"cell\s*\(\s*(\w+)\s*\)", liberty), [MACRO])
        area, = re.findall(r"\barea\s*:\s*([0-9.]+)\s*;", liberty)
        self.assertEqual(Decimal(area), Decimal("28127.104"))
        self.assertEqual(Decimal(str(stat["area"])), Decimal("2182.7232"))
        self.assertEqual(Decimal(str(stat["area"])) + Decimal(area), Decimal("30309.8272"))
        self.assertEqual(Decimal(str(stat["sequential_area"])), Decimal("783.8208"))

    def test_final_netlist_counts_and_combinational_delay_cells(self):
        final = PHYSICAL / "flow/final/nl" / (TOP + ".nl.v")
        self.assertEqual(sha(final), sha(PHYSICAL / "mapped.v"))
        instances = re.findall(r"^\s*(RM_\w+|sg13cmos5l_\w+)\s+(\S+)\s*\(",
                               final.read_text(), re.MULTILINE)
        types = Counter(cell for cell, _ in instances)
        self.assertEqual([(cell, name) for cell, name in instances if cell.startswith("RM_")],
                         [(MACRO, INSTANCE)])
        self.assertEqual(len(instances), 68929)
        self.assertEqual(dict(types), load(PHYSICAL / "summary.json")["final_cell_types"])
        self.assertEqual(types["sg13cmos5l_dfrbpq_1"], 16)
        self.assertEqual(types["sg13cmos5l_dlygate4sd3_1"], 81)
        self.assertEqual(sum(count for cell, count in types.items()
                             if re.match(r"sg13cmos5l_(?:s?df|dl(?!ygate)|latch)", cell)), 16)

    def test_physical_area_and_count_scopes(self):
        metrics = load(PHYSICAL / "metrics.json")
        self.assertEqual(metrics["design__instance__count"], 68929)
        self.assertEqual(metrics["design__instance__count__stdcell"], 389)
        self.assertEqual(metrics["design__instance__count__class:fill_cell"], 68539)
        self.assertEqual(metrics["design__instance__count__macros"], 1)
        self.assertEqual(389 + 68539 + 1, metrics["design__instance__count"])
        self.assertEqual(metrics["design__instance__area__stdcell"], 4793.64)
        self.assertEqual(metrics["design__instance__area"], 899576)
        self.assertEqual(metrics["design__instance__area__class:fill_cell"], 866655)
        result = load(PHYSICAL / "results.json")
        self.assertEqual(result["metrics"]["mapped_area"]["stage"], "Yosys.Synthesis")
        self.assertEqual(result["metrics"]["final_standard_cell_area"]["value"], 4793.64)

    def test_physical_artifact_hashes_and_original_verdicts(self):
        result = load(PHYSICAL / "results.json")
        physical = load(PHYSICAL / "physical-checks.json")
        self.assertEqual(result["physical_evidence"], physical)
        self.assertEqual(physical["status"], "pass")
        self.assertEqual(physical["magic_raw_count"], 3)
        self.assertEqual(physical["lvs_scope"], "abstract_macro_boundary_with_schematic_cdl")
        self.assertEqual(physical["internal_device_lvs"], "not_verified")
        self.assertEqual(sha(PHYSICAL / "final.gds"), physical["gds_sha256"])
        for relative, digest in physical["artifacts"].items():
            with self.subTest(artifact=relative):
                self.assertEqual(sha(PHYSICAL / "flow" / relative), digest)
        for check in result["checks"].values():
            self.assertEqual(check["status"], "pass")
        postcheck, = result["postchecks"]
        self.assertEqual(postcheck["checks"], {"gate_level": "pass", "precheck": "pass"})
        self.assertEqual(postcheck["run_id"], CASES[1][2])
        self.assertEqual(postcheck["build_identity"], CASES[1][3])

    def test_disposable_mutation_constructors_only(self):
        original = load(SYNTH / "mapped.json")
        baseline = copy.deepcopy(original)
        with tempfile.TemporaryDirectory(prefix="pt5-resource-") as temporary:
            for kind, expected_count in (("missing", 175), ("extra", 177), ("renamed", 176),
                                         ("wrong_type", 176), ("empty", 0)):
                with self.subTest(mutation=kind):
                    path = Path(temporary) / (kind + ".json")
                    path.write_text(json.dumps(mapped_mutation(original, kind)))
                    mutated = load(path)
                    cells = mutated["modules"][TOP]["cells"]
                    self.assertNotEqual(mutated, original)
                    self.assertEqual(len(cells), expected_count)
                    if kind in ("missing", "renamed", "empty"):
                        self.assertNotIn(INSTANCE, cells)
                    elif kind == "extra":
                        self.assertEqual(cells[INSTANCE + "_extra"], cells[INSTANCE])
                    else:
                        self.assertNotEqual(cells[INSTANCE]["type"], MACRO)
        self.assertEqual(original, baseline)


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, separators=(",", ":"), ensure_ascii=False) + "\n")


class PublicAcceptance(unittest.TestCase):
    """Only the installed ASIC provider supplies reconciliation and verdicts."""
    commands = []
    mutations = []

    def fixture(self, source):
        temporary = tempfile.TemporaryDirectory(prefix="pt5-copy-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name) / "run"
        shutil.copytree(source, root)
        return root

    def invoke(self, executable, *args, code=0):
        command = [str(executable), *(str(arg) for arg in args)]
        # No PDK/tool discovery is possible, including accidental subprocess EDA.
        env = dict(os.environ, PATH="/nonexistent/pt5-no-tools", TOOLCHAIN="/nonexistent/pt5")
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
        stem = f"{len(self.commands):03d}"
        stdout, stderr = self.output / (stem + ".stdout"), self.output / (stem + ".stderr")
        stdout.write_text(result.stdout)
        stderr.write_text(result.stderr)
        self.commands.append(dict(command=command, exit=result.returncode, expected_exit=code,
                                  stdout=stdout.name, stderr=stderr.name, test=self.id()))
        self.assertEqual(result.returncode, code, (command, result.stdout, result.stderr))
        return json.loads(result.stdout) if result.stdout.strip() else None

    def inspect(self, root, code=0):
        return self.invoke(self.provider, "resources-inspect", root, "--json", code=code)

    def api(self, operation, path, *args, code=0):
        return self.invoke(self.consumer, operation, path, *args, code=code)

    def refs(self, evidence, root):
        advertised = {ref["path"]: ref["sha256"] for ref in evidence["evidence_refs"]}
        self.assertEqual(len(advertised), len(evidence["evidence_refs"]))
        for relative, digest in advertised.items():
            path = (root / relative).resolve()
            self.assertTrue(path.is_relative_to(root.resolve()))
            self.assertEqual(sha(path), digest)
        def walk(value):
            if isinstance(value, dict):
                if {"path", "sha256", "format", "scope"} <= value.keys():
                    self.assertEqual(advertised[value["path"]], value["sha256"])
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)
        walk(evidence)

    def measurement(self, observation, key, value, unit):
        metric = observation["measurements"][key]
        self.assertEqual(metric["value"], value)
        self.assertEqual(metric["unit"], unit)
        self.assertEqual(metric["stage"], observation["stage"])
        self.assertTrue(metric["scope"])
        self.assertTrue(metric["definition"])
        if value is None:
            self.assertTrue(metric["unavailable_reason"])
        else:
            self.assertIsNone(metric["unavailable_reason"])
            self.assertTrue(metric["evidence_refs"])

    def assert_required_failure(self, evidence, stage, status):
        observation, = [o for o in evidence["observations"] if o["stage"] == stage]
        self.assertEqual(observation["resources"][0]["status"], status)
        self.assertEqual(observation["status"], "fail")
        check, = [c for c in evidence["check_outcomes"] if c["stage"] == stage]
        self.assertEqual(check, dict(stage=stage, status="fail", required=True))
        return observation

    def record_mutation(self, root, source, label, paths):
        self.mutations.append(dict(label=label, source=str(source.relative_to(ROOT)),
                                   fixture=str(root), changes=[dict(
                                       path=p, original_sha256=sha(source / p) if (source / p).is_file() else None,
                                       mutated_sha256=sha(root / p) if (root / p).is_file() else None)
                                        for p in paths]))

    def stage_synthesis(self, root):
        """Materialize retained bytes at live paths; live runs cannot use aliases."""
        mapping = [("manifest.json", "project/manifest.json"),
                   ("mapped.json", f"project/runs/asic/06-yosys-synthesis/{TOP}.nl.v.json"),
                   ("stat.json", "project/runs/asic/06-yosys-synthesis/reports/stat.json")]
        for source, destination in mapping:
            target = root / destination
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / source, target)
        self.mutations.append(dict(label="stage_retained_synthesis", fixture=str(root), mapping=mapping))

    def bind_physical_netlist(self, root):
        path = root / f"flow/final/nl/{TOP}.nl.v"
        checks = load(root / "physical-checks.json")
        checks["artifacts"][f"final/nl/{TOP}.nl.v"] = sha(path)
        write_json(root / "physical-checks.json", checks)
        run = load(root / "run.json")
        run["physical_checks_sha256"] = sha(root / "physical-checks.json")
        write_json(root / "run.json", run)

    def test_retained_public_cli_library_identity_stage_hash_and_measurements(self):
        for root, manifest_path, run_id, identity, completed in CASES:
            with self.subTest(run=run_id):
                evidence = self.inspect(root)
                self.assertEqual(evidence, self.api("inspect", root))
                self.assertEqual(evidence["contract"], "hardcaml-asic.resource-evidence")
                self.assertEqual(evidence["schema_version"], 1)
                self.assertEqual(evidence["coverage"], "legacy_resources_macro_contract")
                inventory, = evidence["resource_inventory"]
                self.assertEqual(inventory["resource_id"], "program")
                self.assertEqual(inventory["inventory_record"], load(root / manifest_path)["resources"][0])
                provenance = evidence["provenance"]
                self.assertEqual((provenance["run_id"], provenance["build_identity"],
                                  provenance["completed_stage"]), (run_id, identity, completed))
                self.assertEqual(provenance["manifest"]["sha256"], sha(root / manifest_path))
                self.assertEqual(provenance["run"]["sha256"], sha(root / "run.json"))
                self.assertEqual(provenance["context_sha256"], sha(root / "run.json"))
                self.assertEqual(provenance["preparation_link"]["status"], "unavailable")
                self.assertTrue(provenance["preparation_link"]["reason"])
                stages = [o["stage"] for o in evidence["observations"]]
                self.assertEqual(stages, ["synthesis"] if root == SYNTH else ["synthesis", "final_physical"])
                self.refs(evidence, root)
                for observation in evidence["observations"]:
                    self.assertEqual((observation["run_id"], observation["build_identity"]), (run_id, identity))
                    self.assertEqual(observation["producer_origin"]["stage"], observation["stage"])
                    self.assertEqual(observation["status"], "pass")
                    self.assertEqual(observation["unexpected_instances"], [])
                    row, = observation["resources"]
                    self.assertEqual({key: row[key] for key in inventory}, inventory)
                    self.assertEqual(row["status"], "matched")
                    self.assertEqual(row["expected"]["retention_requirement"], "required")
                    self.assertEqual(row["realized"], dict(count=1, instances=[dict(instance=INSTANCE, module=MACRO)]))
                    for key in ("timing_links", "electrical_links"):
                        self.assertEqual(row[key]["status"], "unavailable")
                        self.assertTrue(row[key]["reason"])
                self.assertTrue(all(c["required"] and c["status"] == "pass" for c in evidence["check_outcomes"]))
                synth = evidence["observations"][0]
                self.assertEqual(synth["producer"], "Yosys.Synthesis")
                for key, value in (("total_mapped_cells", 176), ("macro_count", 1), ("standard_cell_count", 175)):
                    self.measurement(synth, key, value, "count")
                types = {t["module"]: t["count"] for t in synth["cell_type_counts"]["types"]}
                self.assertEqual(types["sg13cmos5l_dfrbpq_1"], 16)
                self.measurement(synth, "sequential_cell_count", None, "count")
                for key, value in (("synthesis_standard_cell_area", 2182.7232),
                                   ("whole_design_sequential_area", 783.8208),
                                   ("macro_library_area", 28127.104),
                                   ("combined_cell_area_estimate", 30309.8272)):
                    self.measurement(synth, key, value if root == SYNTH else None, "um^2")
                if root == PHYSICAL:
                    final = evidence["observations"][1]
                    self.measurement(final, "total_physical_netlist_cells", 68929, "count")
                    self.measurement(final, "standard_cell_count", 68928, "count")
                    self.assertIn("filler/decap", final["measurements"]["standard_cell_count"]["scope"])
                    self.measurement(final, "final_standard_cell_area", 4793.64, "um^2")
                    self.measurement(final, "standard_cell_utilization", 0.0054829, "ratio")
                    self.assertIn("denominator/excluded regions unavailable", final["measurements"]["standard_cell_utilization"]["definition"])
                self.assertEqual(self.api("validate", self.output / self.commands[-2]["stdout"]), {"valid": True})

    def test_synthesis_semantic_negatives_with_consistent_stat(self):
        for kind, status in (("missing", "missing"), ("extra", "unexpected"),
                             ("renamed", "unexpected"), ("wrong_type", "unresolved"),
                             ("wrong_known_type", "unexpected"), ("empty", "missing")):
            with self.subTest(mutation=kind):
                root = self.fixture(SYNTH)
                original = load(root / "mapped.json")
                if kind == "wrong_known_type":
                    mutated = copy.deepcopy(original)
                    mutated["modules"][TOP]["cells"][INSTANCE]["type"] = "sg13cmos5l_inv_1"
                else:
                    mutated = mapped_mutation(original, kind)
                write_json(root / "mapped.json", mutated)
                cells = mutated["modules"][TOP]["cells"]
                stat = load(root / "stat.json")
                counts = dict(Counter(cell["type"] for cell in cells.values()))
                # Update both design and module views; no stale aggregate can mask
                # the exact instance reconciliation tested here.
                for row in [stat["design"], *stat["modules"].values()]:
                    row.update(num_cells=len(cells), num_cells_by_type=counts)
                    row["area"] = sum(float(mutated["modules"].get(c["type"], {}).get(
                        "attributes", {}).get("area", 0)) for c in cells.values())
                write_json(root / "stat.json", stat)
                self.stage_synthesis(root)
                self.record_mutation(root, SYNTH, kind, ["mapped.json", "stat.json"])
                evidence = self.inspect(root, 1)
                observation = self.assert_required_failure(evidence, "synthesis", status)
                self.assertNotIn("measurement_error", observation)
                self.refs(evidence, root)
                self.assertIsNone(observation["resources"][0]["area"]["value"])
                if kind in ("extra", "renamed"):
                    self.assertTrue(observation["unexpected_instances"])
                elif kind == "wrong_type":
                    self.assertEqual(observation["resources"][0]["realized"]["status"], "unavailable")
                    self.assertIn("non-leaf/non-library", observation["resources"][0]["reason"])
                self.assertEqual(self.api("collect", root)["resource_evidence"], evidence)

    def test_retained_report_and_reconstructed_collection_archive_closure(self):
        direct = self.inspect(PHYSICAL)
        report = self.api("report", PHYSICAL)
        self.assertTrue(report["accepted"], report["problems"])
        self.assertEqual(report["results"]["resource_evidence"], direct)
        root = self.fixture(PHYSICAL)
        # Reconstruct only paths with real retained source bytes. No stat/state
        # report is synthesized to fill the physical snapshot's missing reports.
        project = root / "project"
        shutil.copytree(root / "bundle", project)
        flow = project / "runs/asic"
        shutil.copytree(root / "flow", flow)
        mapping = [("metrics.json", "project/runs/asic/final/metrics.json"),
                   ("metrics.csv", "project/runs/asic/final/metrics.csv"),
                   ("final.gds", f"project/runs/asic/final/gds/{TOP}.gds"),
                   ("runtime/physical-runtime.py", "project/physical-runtime.py"),
                   ("runtime/macro-flow.py", "project/macro-flow.py"),
                   ("mapped.json", f"project/runs/asic/06-yosys-synthesis/{TOP}.nl.v.json")]
        for source, destination in mapping:
            target = root / destination
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / source, target)
        # Archive must use the retained staged bundle, never discover the old
        # absolute external bundle named in this historical run record.
        run = load(root / "run.json")
        run["bundle"] = str(project)
        write_json(root / "run.json", run)
        self.mutations.append(dict(label="portable_live_layout_reconstruction",
                                   source=str(PHYSICAL.relative_to(ROOT)), fixture=str(root),
                                   mapping=mapping, bundle_copy=["bundle/", "project/"],
                                   flow_copy=["flow/", "project/runs/asic/"],
                                   run_bundle_relocated=True, run_sha256=sha(root / "run.json")))
        evidence = self.inspect(root)
        collected = self.api("collect", root)
        self.assertEqual(collected["resource_evidence"], evidence)
        self.assertEqual(collected["resource_evidence"]["check_outcomes"], direct["check_outcomes"])
        self.assertEqual(collected["physical_evidence"]["status"], "pass")
        self.assertTrue({ref["path"] for ref in evidence["evidence_refs"]} <= set(collected["raw_artifacts"]))
        # Preserve the retained global results in this copy; add only the new
        # resource object. Collection's global coverage is limited by absent stat.
        stored = load(root / "results.json")
        stored["resource_evidence"] = evidence
        write_json(root / "results.json", stored)
        stored_hash = sha(root / "results.json")
        refreshed = self.api("report", root)
        self.assertTrue(refreshed["accepted"], refreshed["problems"])
        self.assertEqual(refreshed["results"]["resource_evidence"], evidence)
        self.assertEqual(sha(root / "results.json"), stored_hash)
        sources = self.api("archive-sources", root)
        advertised = {ref["path"]: ref["sha256"] for ref in evidence["evidence_refs"]}
        self.assertTrue(advertised.keys() <= set(sources))
        archive = self.output / "retained-physical-archive"
        self.invoke(self.provider, "archive", root, "--output", archive, "--json")
        with tarfile.open(archive / "reports.tar.gz") as stream:
            names = stream.getnames()
            self.assertTrue(advertised.keys() <= set(names))
            for path, digest in advertised.items():
                self.assertEqual(hashlib.sha256(stream.extractfile(path).read()).hexdigest(), digest)
        # verify_sources/archive reject bytes stale against an already produced object.
        evidence_path = self.output / "archived-resource-evidence.json"
        write_json(evidence_path, evidence)
        self.assertTrue(self.api("verify-sources", evidence_path, root)["valid"])
        mapped_path = root / f"project/runs/asic/06-yosys-synthesis/{TOP}.nl.v.json"
        mapped_bytes = mapped_path.read_bytes()
        mapped_path.write_bytes(mapped_bytes + b"\n")
        verdict = self.api("verify-sources", evidence_path, root)
        self.assertFalse(verdict["valid"])
        self.assertTrue(verdict["reason"])
        self.api("archive-sources", root, code=2)
        # A self-consistent count forgery with the SAME source hashes passes the
        # offline shape reader but must fail full source-derived replay.
        mapped_path.write_bytes(mapped_bytes)
        forged = copy.deepcopy(evidence)
        observation = forged["observations"][0]
        types = observation["cell_type_counts"]["types"]
        next(row for row in types if row["module"] == "sg13cmos5l_inv_1")["count"] += 1
        for key in ("total_mapped_cells", "standard_cell_count"):
            observation["measurements"][key]["value"] += 1
        forged_path = self.output / "coherent-count-forgery.json"
        write_json(forged_path, forged)
        self.assertTrue(self.api("validate", forged_path)["valid"])
        verdict = self.api("verify-sources", forged_path, root)
        self.assertFalse(verdict["valid"])
        self.assertIn("source-aware reconciliation replay", verdict["reason"])
        stored["resource_evidence"] = forged
        write_json(root / "results.json", stored)
        forged_stored_hash = sha(root / "results.json")
        rejected_archive = self.output / "rejected-forgery-archive"
        self.invoke(self.provider, "archive", root, "--output", rejected_archive, "--json", code=2)
        self.assertFalse(rejected_archive.exists())
        self.assertFalse(self.api("report", root)["accepted"])
        self.assertEqual(sha(root / "results.json"), forged_stored_hash)

    def test_missing_and_malformed_observation_not_empty_inventory(self):
        for label, contents in (("missing_file", None), ("malformed", '{"modules":{},"modules":{}}')):
            with self.subTest(label=label):
                root = self.fixture(SYNTH)
                if contents is None:
                    (root / "mapped.json").unlink()
                else:
                    (root / "mapped.json").write_text(contents)
                self.record_mutation(root, SYNTH, label, ["mapped.json"])
                observation = self.assert_required_failure(self.inspect(root, 1), "synthesis", "unresolved")
                self.assertEqual(observation["resources"][0]["realized"]["status"], "unavailable")
                self.assertTrue(observation["resources"][0]["realized"]["reason"])

    def test_physical_semantic_negatives_rebind_checker_and_run_digests(self):
        relative = f"flow/final/nl/{TOP}.nl.v"
        for kind, status in (("missing", "missing"), ("extra", "unexpected"),
                             ("renamed", "unexpected"), ("wrong_type", "unresolved"),
                             ("duplicate", "unresolved"), ("multideclarator", "unexpected")):
            with self.subTest(mutation=kind):
                root = self.fixture(PHYSICAL)
                path = root / relative
                raw = path.read_text()
                block, = re.findall(r"(?ms)^\s*" + MACRO + r"\s+" + INSTANCE + r"\s*\(.*?;", raw)
                if kind == "missing":
                    replacement = ""
                elif kind == "renamed":
                    replacement = block.replace(INSTANCE, INSTANCE + "_renamed", 1)
                elif kind == "wrong_type":
                    replacement = block.replace(MACRO, "RM_IHPSG13_1P_wrong_type", 1)
                elif kind == "extra":
                    replacement = block + block.replace(INSTANCE, INSTANCE + "_extra", 1)
                elif kind == "multideclarator":
                    # One declaration, two instances, nested connection syntax:
                    # the second instance must not disappear after the first ')'.
                    extra = block.strip()[len(MACRO):].lstrip().replace(INSTANCE, INSTANCE + "_extra", 1)
                    extra = extra.replace(".A_CLK(clknet_1_0__leaf_clk)",
                                          ".A_CLK({clknet_1_0__leaf_clk,clknet_1_0__leaf_clk})", 1)
                    replacement = block.rstrip().removesuffix(";") + ", " + extra
                else:
                    replacement = block + block
                path.write_text(raw.replace(block, replacement, 1))
                self.bind_physical_netlist(root)
                self.record_mutation(root, PHYSICAL, "physical_" + kind,
                                     [relative, "physical-checks.json", "run.json"])
                evidence = self.inspect(root, 1)
                self.assertEqual(evidence["observations"][0]["status"], "pass")
                observation = self.assert_required_failure(evidence, "final_physical", status)
                self.assertNotIn("hash mismatch", str(observation["reason"]))
                self.refs(evidence, root)
                if kind == "multideclarator":
                    self.measurement(observation, "macro_count", 2, "count")
                    self.assertEqual(observation["unexpected_instances"],
                                     [dict(module=MACRO, instance=INSTANCE + "_extra")])
                self.assertEqual(self.api("report", root)["accepted"], False)

    def test_unreached_synthesis_and_later_failure_boundaries(self):
        for status in ("failed", "interrupted", "completed"):
            with self.subTest(status=status):
                root = self.fixture(SYNTH)
                run = load(root / "run.json")
                run.update(status=status, completed_stage=None)
                write_json(root / "run.json", run)
                self.record_mutation(root, SYNTH, "synthesis_not_reached_" + status, ["run.json"])
                observation = self.assert_required_failure(self.inspect(root, 1), "synthesis", "unresolved")
                self.assertIn("completion/producer boundary", observation["reason"])
                self.measurement(observation, "total_mapped_cells", None, "count")
        root = self.fixture(SYNTH)
        run = load(root / "run.json")
        run.update(status="failed", requested_stage="full", completed_stage="synthesis")
        write_json(root / "run.json", run)
        self.record_mutation(root, SYNTH, "later_failure_after_synthesis", ["run.json"])
        evidence = self.inspect(root, 1)
        self.assertEqual(evidence["observations"][0]["status"], "pass")
        self.assert_required_failure(evidence, "final_physical", "unresolved")
        # Root aliases cannot rescue a staged live run bound to an absent flow.
        root = self.fixture(SYNTH)
        self.stage_synthesis(root)
        run = load(root / "run.json")
        run["outputs"]["flow"] = "unrelated-flow"
        write_json(root / "run.json", run)
        self.record_mutation(root, SYNTH, "wrong_live_producing_flow", ["run.json"])
        self.assert_required_failure(self.inspect(root, 1), "synthesis", "unresolved")

    def test_hidden_hierarchy_cannot_be_a_standard_cell_leaf(self):
        for contents in ("cells", "processes", "memories"):
            with self.subTest(contents=contents):
                root = self.fixture(SYNTH)
                mapped = load(root / "mapped.json")
                definition = mapped["modules"]["sg13cmos5l_inv_1"]
                self.assertTrue(int(definition["attributes"]["blackbox"], 2))
                definition[contents] = {"hidden": dict(type=MACRO)}
                write_json(root / "mapped.json", mapped)
                self.record_mutation(root, SYNTH, "blackbox_hidden_" + contents, ["mapped.json"])
                observation = self.assert_required_failure(self.inspect(root, 1), "synthesis", "unresolved")
                self.assertIn("non-leaf/non-library", observation["reason"])

    def test_physical_tamper_and_stage_not_reached_reject(self):
        for relative, reason in ((f"flow/final/nl/{TOP}.nl.v", "hash mismatch"),
                                 ("physical-checks.json", "digest mismatch"),
                                 ("final.gds", "GDS digest mismatch")):
            with self.subTest(tamper=relative):
                root = self.fixture(PHYSICAL)
                with (root / relative).open("ab") as stream:
                    stream.write(b"\n")
                self.record_mutation(root, PHYSICAL, "unbound_tamper", [relative])
                observation = self.assert_required_failure(self.inspect(root, 1), "final_physical", "unresolved")
                self.assertIn(reason, observation["reason"])
        root = self.fixture(PHYSICAL)
        run = load(root / "run.json")
        run["completed_stage"] = "synthesis"
        write_json(root / "run.json", run)
        self.record_mutation(root, PHYSICAL, "stage_not_reached", ["run.json"])
        observation = self.assert_required_failure(self.inspect(root, 1), "final_physical", "unresolved")
        self.assertIn("not reached", observation["reason"])

    def test_aggregate_disagreement_and_unbound_liberty_are_not_area_proof(self):
        root = self.fixture(SYNTH)
        write_json(root / "mapped.json", mapped_mutation(load(root / "mapped.json"), "extra"))
        self.record_mutation(root, SYNTH, "extra_stale_stat", ["mapped.json"])
        observation = self.assert_required_failure(self.inspect(root, 1), "synthesis", "unexpected")
        self.assertIn("count", observation["measurement_error"])
        self.measurement(observation, "synthesis_standard_cell_area", None, "um^2")
        root = self.fixture(SYNTH)
        relative = f"models/{MACRO}_typ_1p20V_25C.lib"
        path = root / relative
        path.write_text(path.read_text().replace("28127.104", "99999.104"))
        self.record_mutation(root, SYNTH, "unbound_liberty_area", [relative])
        observation = self.inspect(root)["observations"][0]
        # Realization can match despite unavailable optional cost evidence.
        self.assertEqual(observation["status"], "pass")
        self.measurement(observation, "macro_library_area", None, "um^2")
        self.measurement(observation, "combined_cell_area_estimate", None, "um^2")
        self.assertIn("not bound", observation["measurements"]["macro_library_area"]["unavailable_reason"])

    def test_invalid_provenance_exit_two(self):
        for label in ("build", "manifest_hash", "manifest_payload", "unknown_stage"):
            with self.subTest(label=label):
                root = self.fixture(SYNTH)
                run = load(root / "run.json")
                if label == "build":
                    run["build_identity"] = "0" * 64
                elif label == "manifest_hash":
                    run["manifest_sha256"] = "0" * 64
                elif label == "unknown_stage":
                    run["requested_stage"] = "invented"
                else:
                    manifest = load(root / "manifest.json")
                    manifest["project"] = "tampered"
                    write_json(root / "manifest.json", manifest)
                write_json(root / "run.json", run)
                self.record_mutation(root, SYNTH, label, ["run.json", "manifest.json"])
                self.inspect(root, 2)
                self.assertTrue((self.output / self.commands[-1]["stderr"]).read_text())

    def test_strict_public_schema_rejects_false_link_stage_build_and_nonfinite(self):
        baseline = self.inspect(SYNTH)
        mutations = {
            "fake_preparation": lambda x: x["provenance"].update(preparation_link=dict(status="verified", reason="name resemblance")),
            "stale_stage": lambda x: x["observations"][0].update(stage="final_physical"),
            "stale_build": lambda x: x["observations"][0].update(build_identity="0" * 64),
            "wrong_count": lambda x: x["observations"][0]["resources"][0]["realized"].update(count=0),
            "nonfinite": lambda x: x["observations"][0]["measurements"]["macro_count"].update(value=float("nan")),
            "erased_observation_inventory": lambda x: x["observations"][0].update(resources=[]),
            "typed_macro_count": lambda x: x["observations"][0]["measurements"]["macro_count"].update(value=0),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                evidence = copy.deepcopy(baseline)
                mutate(evidence)
                path = self.output / (label + ".json")
                write_json(path, evidence)
                verdict = self.api("validate", path)
                self.assertFalse(verdict["valid"])
                self.assertTrue(verdict["reason"])

    def test_fresh_emitted_flops_and_fallback_have_unavailable_attribution(self):
        for selection in ("flops", "fallback"):
            with self.subTest(selection=selection):
                bundle = self.output / ("emitted-" + selection)
                # Emission reads source Git. This command is EDA-less but needs Git.
                command = [str(self.memory), "emit", "--selection", selection, "--depth", "128",
                           "--operation", "synthesis", "--source-root", str(ROOT), "--output-dir", str(bundle)]
                process = subprocess.run(command, capture_output=True, text=True)
                stem = f"{len(self.commands):03d}"
                (self.output / (stem + ".stdout")).write_text(process.stdout)
                (self.output / (stem + ".stderr")).write_text(process.stderr)
                self.commands.append(dict(command=command, exit=process.returncode, expected_exit=0,
                                          stdout=stem + ".stdout", stderr=stem + ".stderr", test=self.id()))
                self.assertEqual(process.returncode, 0, process.stderr)
                manifest = load(bundle / "manifest.json")
                snapshot = manifest["resource_snapshot"]
                self.assertEqual((snapshot["mode"], snapshot["scope"]), ("implementation", "resolved"))
                self.assertTrue(snapshot["resources"])
                root = self.fixture(SYNTH)
                # Synthetic observation fixture, not a newly synthesized emitted design.
                write_json(root / "manifest.json", manifest)
                run = load(root / "run.json")
                run.update(build_identity=manifest["identity"], manifest_sha256=sha(root / "manifest.json"))
                write_json(root / "run.json", run)
                mapped = mapped_mutation(load(root / "mapped.json"), "missing")
                write_json(root / "mapped.json", mapped)
                (root / "stat.json").unlink()
                evidence = self.inspect(root)
                self.assertEqual(evidence["coverage"], "resource_snapshot")
                row, = evidence["observations"][0]["resources"]
                self.assertEqual(row["selected_implementation"]["kind"], "flops")
                self.assertEqual(row["status"], "unresolved")
                self.assertEqual(row["realized"]["status"], "unavailable")
                self.assertEqual(row["attribution"]["status"], "unavailable")
                self.assertIsNone(row["area"]["value"])
                self.assertTrue(row["area"]["unavailable_reason"])
                self.assertFalse(evidence["check_outcomes"][0]["required"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--research-only", action="store_true")
    parser.add_argument("--receipt", type=Path, help="new unittest receipt; parent must exist")
    parser.add_argument("--provider", type=Path)
    parser.add_argument("--consumer", type=Path)
    parser.add_argument("--memory", type=Path)
    parser.add_argument("--output-dir", type=Path, help="new public acceptance output directory")
    args = parser.parse_args()
    public = not args.research_only
    if public and not all((args.provider, args.consumer, args.memory, args.output_dir)):
        parser.error("public acceptance needs --provider --consumer --memory --output-dir")
    if public:
        for field in ("provider", "consumer", "memory"):
            setattr(PublicAcceptance, field, getattr(args, field).resolve(strict=True))
        PublicAcceptance.output = args.output_dir.resolve()
        if PublicAcceptance.output.exists():
            parser.error("public output directory must be new")
        if not PublicAcceptance.output.is_relative_to(ROOT / "acceptance/resource-realization"):
            parser.error("public output directory must be under acceptance/resource-realization")
        PublicAcceptance.output.mkdir()
    if args.receipt:
        destination = args.receipt.resolve()
        if destination.is_relative_to(SYNTH) or destination.is_relative_to(PHYSICAL):
            parser.error("receipt cannot be written inside historical evidence")
        if destination.exists() or not destination.parent.is_dir():
            parser.error("receipt must be new with an existing parent directory")
    before = historical_hashes()
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RetainedResearch)
    if public:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(PublicAcceptance))
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    after = historical_hashes()
    preserved = before == after
    receipt = {
        "scope": "PT.5 installed public-provider acceptance" if public else "PT.5 independent retained-evidence research; NOT public API acceptance",
        "command": sys.orig_argv,
        "python_version": sys.version,
        "python_executable_sha256": sha(Path(sys.executable).resolve()),
        "script_sha256": sha(Path(__file__).resolve()),
        "tests_run": result.testsRun, "failures": len(result.failures),
        "errors": len(result.errors), "skipped": result.skipped,
        "unittest_output": stream.getvalue(),
        "historical_files_before": before, "historical_files_after": after,
        "historical_bytes_preserved": preserved,
        "retained_providers": [load(root / "provider-receipt.json") for root, *_ in CASES],
        "public_api_acceptance": ("passed" if result.wasSuccessful() and preserved else "failed") if public else "not run: research only",
        "public_api_command": ["hardcaml-asic-flow", "resources-inspect", "RUN_DIR", "--json"],
        "unavailable": ["PT.5 provider receipt/source/executable identity (not captured yet)",
                        "public required-macro rejection outcomes (constructors tested only)",
                        "public collection/report and archive closure checks",
                        "named-flow FIFO compatibility on PT.5 provider",
                        "verified separate-preparation linkage for historical runs",
                        "per-resource flop cost and timing/electrical attribution"],
    }
    if public:
        receipt.update(commands=PublicAcceptance.commands, mutations=PublicAcceptance.mutations,
                       executable_ids={field: dict(path=str(getattr(PublicAcceptance, field)),
                                                  sha256=sha(getattr(PublicAcceptance, field)))
                                       for field in ("provider", "consumer", "memory")},
                       provider_receipt=load(PublicAcceptance.provider.parent.parent / "receipt.json"),
                       unavailable=["verified separate-preparation linkage (provider explicitly unavailable)",
                                    "per-resource flop/timing/electrical attribution",
                                    "physical snapshot synthesis stat/Liberty areas",
                                    "producer authentication / P6 source stamping",
                                    "fresh EDA realization of emitted flop/fallback bundles"])
        write_json(PublicAcceptance.output / "receipt.json", receipt)
    if args.receipt:
        with args.receipt.open("x") as output:
            json.dump(receipt, output, indent=2)
            output.write("\n")
    print(stream.getvalue(), end="")
    print(f"Historical bytes preserved: {preserved}; {len(before)} files")
    print("Public API acceptance: " + receipt["public_api_acceptance"])
    return 0 if result.wasSuccessful() and preserved else 1


if __name__ == "__main__":
    sys.exit(main())
