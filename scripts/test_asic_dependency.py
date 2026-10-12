"""PDK-free setup contract tests. Only temporary fixtures create Git commits."""
import fcntl
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import asic_dependency as dep

PROJECT_API = """type t
val create : name:string -> ?source_inputs:string list -> policy:Resource_policy.t -> unit -> t Or_error.t
val source_inputs : t -> string list
val describe : t -> Sexp.t
val emit_bundle : ?inputs:Target.Inputs.t -> ?include_simulation:bool -> t -> source_root:string -> output_dir:string -> Bundle.t Or_error.t
"""


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="asic setup's ")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "provider's source"
        self.source.mkdir()
        self.store = self.root / "private store's prefix"
        self.calls = []
        files = {
            "dune-project": "(lang dune 3.17)\n(name hardcaml_asic)\n",
            "lib/elaborated_project.mli": "type t\n",
            "lib/resolved_flow.mli": "type t = private { elaborated_project : Elaborated_project.t }\n",
            "lib/bundle.mli": "val render : ?simulation_project:Elaborated_project.t -> unit\n",
            "lib/project.mli": PROJECT_API,
            "flow/dune": "hardcaml-asic-flow\n",
            "toolchain.lock": "fixture data\n",
            ".gitignore": "_build/\n.toolchain/\nignored\n",
        }
        for name, text in files.items():
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        data = self.source / "flow/hardcaml_asic_flow/data"
        data.mkdir(parents=True)
        (data / "toolchain.lock").symlink_to("../../../toolchain.lock")
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                   GIT_AUTHOR_NAME="Bundle test", GIT_AUTHOR_EMAIL="bundle@test.invalid",
                   GIT_COMMITTER_NAME="Bundle test", GIT_COMMITTER_EMAIL="bundle@test.invalid",
                   GIT_AUTHOR_DATE="2026-01-01T00:00:00Z", GIT_COMMITTER_DATE="2026-01-01T00:00:00Z")
        def fixture_git(*args):
            return dep.run(["git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false",
                            "-c", "init.templateDir=", "-C", str(self.source), *args], env=env)
        self.fixture_git = fixture_git
        fixture_git("init")
        fixture_git("add", ".")
        fixture_git("commit", "-m", "baseline")
        self.assertEqual(fixture_git("remote"), b"")
        self.assertEqual(fixture_git("show", "-s", "--format=%an <%ae>|%cn <%ce>"),
                         b"Bundle test <bundle@test.invalid>|Bundle test <bundle@test.invalid>\n")
        self.record = dict(schema=1, package="hardcaml_asic", repository=dep.REPOSITORY,
                           revision=fixture_git("rev-parse", "HEAD").decode().strip())
        self.failure = None
        self.mutate = False

    def runner(self, argv, *, cwd=None, env=None):
        self.calls.append(argv)
        stage = argv[1] if argv[0] in {"dune", "ocamlfind"} else "cli"
        if stage == self.failure:
            raise dep.Error("injected " + stage + " failure")
        if stage == "build" and "probe.exe" in argv:
            self.assertIn("hardcaml_asic", (Path(cwd) / "dune").read_text())
            self.assertEqual((Path(cwd) / "probe.ml").read_text(), dep.PROBE)
            if self.failure == "dune-probe":
                raise dep.Error("injected Dune link failure")
        elif stage == "build":
            self.snapshot = Path(cwd)
            self.captured = {str(p.relative_to(cwd)): p.read_bytes()
                             for p in Path(cwd).rglob("*") if p.is_file()}
            self.assertTrue((Path(cwd) / "flow/hardcaml_asic_flow/data/toolchain.lock").is_symlink())
            self.assertFalse((Path(cwd) / ".git").exists())
            if self.mutate:
                (self.source / "toolchain.lock").write_text("changed after capture")
                self.assertEqual((Path(cwd) / "toolchain.lock").read_bytes(), b"fixture data\n")
        elif stage == "install":
            generation = Path(argv[argv.index("--prefix") + 1])
            package = generation / "lib/hardcaml_asic"
            for name in ("META", "dune-package", "elaborated_project.mli", "resolved_flow.mli", "bundle.mli",
                         "flow/hardcaml_asic_flow/cli.py", "flow/hardcaml_asic_flow/data/toolchain.lock",
                         "flow/hardcaml_asic_flow/data/toolchain.sh", "flow/hardcaml_asic_flow/data/version.txt"):
                target = package / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("stub installed bytes")
            for name in ("elaborated_project.mli", "resolved_flow.mli", "bundle.mli", "project.mli"):
                (package / name).write_bytes((self.snapshot / "lib" / name).read_bytes())
            if self.failure == "old-api":
                (package / "resolved_flow.mli").write_text("old API")
            if self.failure == "old-project-api":
                (package / "project.mli").write_text("type t")
            if self.failure == "capture-metadata":
                (package / "dune-package").write_text(str(self.snapshot / "_build/install/default/lib"))
            if self.failure == "external-link":
                (package / "external").symlink_to(self.source / "toolchain.lock")
            (generation / "bin").mkdir()
            (generation / "bin/hardcaml-asic-flow").write_text("stub CLI")
            if self.failure == "missing-data":
                (package / "flow/hardcaml_asic_flow/data/toolchain.lock").unlink()
        elif stage == "query":
            if self.failure == "wrong-package":
                return b"/shared/opam/lib/hardcaml_asic\n"
            return (env["OCAMLPATH"].split(":")[0] + "/hardcaml_asic\n").encode()
        elif stage == "ocamlc":
            self.assertIn("Resolved_flow.t", Path(argv[-1]).read_text())
            self.assertIn("?simulation_project:None", Path(argv[-1]).read_text())
            self.assertEqual(Path(argv[-1]).read_text(), dep.PROBE)
            for token in ("Project.create ?source_inputs:", "Project.source_inputs", "Project.describe",
                          "?inputs:Target.Inputs.t", "?include_simulation:bool", "Project.emit_bundle"):
                self.assertIn(token, dep.PROBE)
        return b""

    def refresh(self, mode="recorded"):
        return dep.refresh(self.source, mode, self.store, self.record, self.runner)

    def test_recorded_ignores_dirty_and_untracked_development_includes_them(self):
        (self.source / "toolchain.lock").write_text("dirty")
        (self.source / "new.ml").write_text("untracked")
        (self.source / "ignored").write_text("excluded")
        for directory in ("_build", ".toolchain"):
            (self.source / directory).mkdir()
            (self.source / directory / "secret").write_text("excluded")
        recorded = self.refresh()
        self.assertEqual(self.captured["toolchain.lock"], b"fixture data\n")
        self.assertNotIn("new.ml", self.captured)
        self.assertFalse(recorded["differs_from_recorded_snapshot"])
        dev = self.refresh("development")
        self.assertEqual(self.captured["toolchain.lock"], b"dirty")
        self.assertEqual(self.captured["new.ml"], b"untracked")
        self.assertNotIn("ignored", self.captured)
        self.assertFalse(any("secret" in p for p in self.captured))
        self.assertTrue(dev["differs_from_recorded_snapshot"])
        self.assertNotEqual(dev["snapshot_sha256"], recorded["snapshot_sha256"])
        self.assertTrue(Path(recorded["generation"]).is_dir())
        self.assertFalse((self.source / "_build/default").exists())
        self.assertEqual({c[0] for c in self.calls if "hardcaml-asic-flow" not in c[0]}, {"dune", "ocamlfind"})

    def test_failures_preserve_publication(self):
        first = self.refresh()
        for stage in ("build", "install", "query", "ocamlc", "dune-probe", "capture-metadata", "cli", "missing-data", "wrong-package", "old-api", "old-project-api", "external-link"):
            with self.subTest(stage=stage):
                self.failure = stage
                with self.assertRaises(dep.Error):
                    self.refresh()
                self.assertEqual((self.store / "current").resolve(), Path(first["generation"]))
                self.assertEqual(json.loads((self.store / "current/receipt.json").read_text()), first)

    def test_release_build_uses_capture_without_duplicate_root(self):
        self.refresh()
        build = next(c for c in self.calls if c[:2] == ["dune", "build"])
        self.assertIn("-p", build)
        self.assertNotIn("--root", build)  # -p already supplies --root .
        self.assertEqual(build[build.index("--build-dir") + 1], "_build")
        install = next(c for c in self.calls if c[:2] == ["dune", "install"])
        self.assertEqual(install[install.index("--build-dir") + 1], "_build")
        self.assertTrue(any("probe.exe" in c for c in self.calls))
        self.assertTrue(self.snapshot.is_relative_to(self.store))

    def test_missing_revision_api_and_wrong_source(self):
        first = self.refresh()
        self.record = dict(self.record, revision="0" * 40)
        with self.assertRaises(dep.Error):
            self.refresh()
        self.record = first["record"].copy()
        self.record["revision"] = dep.git(self.source, "rev-parse", "HEAD").decode().strip()
        (self.source / "lib/resolved_flow.mli").unlink()
        with self.assertRaisesRegex(dep.Error, "renamed public API"):
            self.refresh("development")
        with self.assertRaises(dep.Error):
            dep.refresh(self.source / "lib", "recorded", self.store, self.record, self.runner)
        with self.assertRaisesRegex(dep.Error, "renamed public API"):
            dep.api_check({})
        self.fixture_git("add", "lib/resolved_flow.mli")
        self.fixture_git("commit", "-m", "missing interface fixture")
        self.record["revision"] = self.fixture_git("rev-parse", "HEAD").decode().strip()
        with self.assertRaisesRegex(dep.Error, "renamed public API"):
            self.refresh("recorded")
        self.assertEqual((self.store / "current").resolve(), Path(first["generation"]))

    def test_old_recorded_api_allows_new_development_and_refusal_preserves_selection(self):
        (self.source / "lib/project.mli").write_text("type t\n")
        self.fixture_git("add", "lib/project.mli")
        self.fixture_git("commit", "-m", "old project API fixture")
        self.record["revision"] = self.fixture_git("rev-parse", "HEAD").decode().strip()
        (self.source / "lib/project.mli").write_text(PROJECT_API)
        first = self.refresh("development")
        self.assertTrue(first["differs_from_recorded_snapshot"])
        calls = len(self.calls)
        with self.assertRaisesRegex(dep.Error, "explicit development refresh"):
            self.refresh("recorded")
        self.assertEqual(len(self.calls), calls)
        self.assertEqual((self.store / "current").resolve(), Path(first["generation"]))
        self.assertEqual(json.loads((self.store / "current/receipt.json").read_text()), first)

    def test_project_api_requires_all_new_signatures(self):
        dep.project_api_check(PROJECT_API.encode())
        for token in ("?source_inputs:string list", "val source_inputs", "val describe", "val emit_bundle",
                      "?inputs:Target.Inputs.t", "?include_simulation:bool", "output_dir:string"):
            with self.subTest(token=token), self.assertRaises(dep.Error):
                dep.project_api_check(PROJECT_API.replace(token, "obsolete").encode())

    def test_validate_source_reports_uncompiled_and_does_not_publish(self):
        result = dep.run(["python3", str(Path(dep.__file__)), "validate-source",
                          "--source", str(self.source), "--revision", self.record["revision"]])
        report = json.loads(result)
        self.assertIs(report["compiled"], False)
        self.assertIs(report["project_api_present"], True)
        self.assertFalse(self.store.exists())
        self.assertEqual(self.calls, [])

    def test_lock_contention(self):
        first = self.refresh()
        with (self.store / "writer.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaisesRegex(dep.Error, "writer lock"):
                self.refresh()
        self.assertEqual((self.store / "current").resolve(), Path(first["generation"]))

    def test_snapshot_does_not_follow_later_source_edits(self):
        self.mutate = True
        receipt = self.refresh("development")
        self.assertFalse(receipt["differs_from_recorded_snapshot"])
        self.assertEqual(self.captured["toolchain.lock"], b"fixture data\n")
        self.assertEqual(dep.status(self.store, self.record)["receipt"], receipt)

    def test_concurrent_capture_change_is_rejected(self):
        original = dep.development
        def moving(source, store):
            entries = original(source, store)
            (source / "toolchain.lock").write_text("moving")
            return entries
        with patch.object(dep, "development", moving):
            with self.assertRaisesRegex(dep.Error, "changed during capture"):
                self.refresh("development")
        self.assertFalse((self.store / "current").exists())

    def test_activation_repeated_and_status_stale_environment(self):
        first = self.refresh()
        second = self.refresh()
        env = dict(os.environ, OCAMLPATH="/unrelated path/lib:/manual/_build/install/default/lib",
                   PATH=os.environ["PATH"])
        command = '. "$1"; . "$2"; . "$2"; exec python3 -c "import os,json; print(json.dumps(dict(os.environ)))"'
        result = json.loads(dep.run(["sh", "-c", command, "sh",
                                    first["generation"] + "/activate.sh",
                                    second["generation"] + "/activate.sh"], env=env))
        self.assertEqual(result["OCAMLPATH"], second["generation"] + "/lib:" + env["OCAMLPATH"])
        self.assertEqual(result["PATH"], second["generation"] + "/bin:" + env["PATH"])
        with patch.dict(os.environ, HARDCAML_ASIC_GENERATION=first["generation"],
                        OCAMLPATH=first["generation"] + "/lib"):
            status = dep.status(self.store, self.record)
            self.assertTrue(status["active_is_older"])
            self.assertFalse(status["active_is_published"])
            self.assertTrue(status["active_library_path_is_first"])
        self.assertEqual(status["published_generation"], second["generation"])

    def test_explicit_manual_override_removal_is_recorded_and_carried_forward(self):
        manual = str(self.source / "_build/install/default/lib")
        first = dep.refresh(self.source, "recorded", self.store, self.record, self.runner,
                            remove_source_build_override=True)
        second = self.refresh()
        self.assertEqual(first["removed_library_paths"], [manual])
        self.assertEqual(second["removed_library_paths"], [manual])
        env = dict(os.environ, OCAMLPATH=manual + ":/unrelated/lib")
        result = dep.run(["sh", "-c", '. "$1"; python3 -c "import os; print(os.environ[\'OCAMLPATH\'])"',
                          "sh", second["generation"] + "/activate.sh"], env=env)
        self.assertEqual(result.decode().strip(), second["generation"] + "/lib:/unrelated/lib")

    def test_store_safety_and_read_only_status(self):
        self.assertIsNone(dep.status(self.store, self.record)["published_generation"])
        self.assertFalse(self.store.exists())
        self.store.mkdir()
        sentinel = self.store / "keep"
        sentinel.write_text("user work")
        with self.assertRaisesRegex(dep.Error, "ownership"):
            self.refresh()
        self.assertEqual(sentinel.read_text(), "user work")
        alias = self.root / "alias"
        alias.symlink_to(self.store)
        with self.assertRaises(dep.Error):
            dep.store_path(alias)
        with self.assertRaises(dep.Error):
            dep.store_path(self.root / "colon:path")

    def test_unsafe_symlink_rejected(self):
        (self.source / "escape").symlink_to("/etc/passwd")
        with self.assertRaisesRegex(dep.Error, "absolute source symlink"):
            self.refresh("development")
        self.assertFalse((self.store / "current").exists())

    def test_store_inside_source_is_excluded_and_foreign_pointer_preserved(self):
        self.store = self.source / "private-store"
        self.refresh("development")
        self.refresh("development")
        self.assertFalse(any(p.startswith("private-store/") for p in self.captured))
        current = self.store / "current"
        current.unlink()
        current.symlink_to(self.root)
        with self.assertRaisesRegex(dep.Error, "selection"):
            self.refresh()
        self.assertEqual(current.resolve(), self.root)

    def test_process_errors_and_cli_requires_explicit_mode(self):
        with self.assertRaisesRegex(dep.Error, "failure detail"):
            dep.run(["python3", "-c", "import sys; sys.stderr.write('failure detail'); sys.exit(3)"])
        result = subprocess.run(["python3", str(Path(dep.__file__)), "refresh", "--source", str(self.source)],
                                capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"--mode", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
