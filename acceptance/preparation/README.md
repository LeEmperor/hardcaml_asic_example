# PT4 headless consumer acceptance — 2026-10-25

## Final review-corrected capture

Current provider generation:
`.dev/asic-prepare/generations/a5de7cbfcc464e13ae1b5a5db6e39068`.
Captured SHA-256:
`549cf74e17b4c8af34a7133ea3d983786adf5ce6c4d4e8914f62aff0a05e2f2a`.

`capture-final/` contains the new receipt/report, ordered launch events and
portable exact/failure/FIFO attempts. Its workflow descriptors are v2 (correct
`circuit → snapshot → source_after` order); outer schemas remain 1.
`capture-final/historical-compatibility.json` records new-provider inspection
and explicit same/different/unavailable comparisons of the original v1 attempts,
with before/after hashes, sizes, mtimes and paths for the entire original archive.
The old `capture/` evidence and provider generation remain retained.

Use the refresh/build commands below, followed by this final acceptance command:

```sh
python3 -B scripts/check_prepare.py \
  --memory _build_prepare/default/memory/memory_cli.exe \
  --fifo _build_prepare/default/bin/project.exe \
  --provider .dev/asic-prepare/current/bin/hardcaml-asic-flow \
  --source-root "$PWD" --historical-dir "$PWD/acceptance/preparation/capture" \
  --output-dir "$PWD/acceptance/preparation/capture-final"
```

The destination must be new; omit `--output-dir` for a disposable repeat.
The consumer project source is unchanged by this recapture. Coverage continues
to mean observed declared sources, not compiled-source proof.

Final results: **89 checks passed** in the retained matrix and again through
`@scripts/preparation-test`; the cheap CLI checks passed. Full example
`dune runtest --build-dir _build_prepare -j6` passed (one opt-in installed-native
fixture test skipped). Full results and practical comparison commands are in
[`capture-final/validation.md`](capture-final/validation.md).

## Original v1 capture (preserved)

`capture/report.json` records **77 passed checks**, provider metadata, executable
hashes and the isolated development-capture receipt. `capture/launches.json`
retains each launch's allocation and terminal events in order. Three portable
attempts retain provider-owned records and, on success, the complete A payload:

| Directory under `capture/` | Result | Attempt ID |
| --- | --- | --- |
| `exact-synthesis/` | 256×16 stock macro, completed | `7efa34b35a6a4396b6d4d456f5bea0c2` |
| `unsupported-exact-128/` | 128×16 Exact rejected, no snapshot | `aaa438a99e63495a87fb940ea9579033` |
| `fifo-zero-resources/` | Completed, empty resource list | `1b51d0bc81234fe489945da9706d110b` |

Provider generation:
`.dev/asic-prepare/generations/7f396544929449ea9d2115daf332cf7d`

Captured provider SHA-256:
`41352fc461fc0656789da913d58940776d5a9f79171ec18370f3721e487ebd7a`

Observed provider base: `5caf5cf78200227e07ef4355ae1d964337d13588`.
The capture includes working changes and is not a clean-tree/source-stamp claim.

## Exact commands executed

From the example checkout:

```sh
opam exec --switch=5.2.0+ox -- python3 scripts/asic_dependency.py \
  --store "$PWD/.dev/asic-prepare" refresh \
  --source /home/wayne/devel/jane/hardcaml_asic --mode development --jobs 6
. .dev/asic-prepare/current/activate.sh
opam exec --switch=5.2.0+ox -- dune build --build-dir _build_prepare -j6 \
  bin/project.exe memory/memory_cli.exe memory/test/memory_test.exe
python3 -B scripts/check_project_cli.py _build_prepare/default/bin/project.exe
python3 -B scripts/check_prepare.py \
  --memory _build_prepare/default/memory/memory_cli.exe \
  --fifo _build_prepare/default/bin/project.exe \
  --provider .dev/asic-prepare/current/bin/hardcaml-asic-flow \
  --source-root "$PWD" --output-dir "$PWD/acceptance/preparation/capture"
_build_prepare/default/memory/test/memory_test.exe
HARDCAML_ASIC_PREPARATION_PROVIDER="$PWD/.dev/asic-prepare/current/bin/hardcaml-asic-flow" \
HARDCAML_ASIC_PREPARATION_SOURCE_ROOT="$PWD" \
  opam exec --switch=5.2.0+ox -- dune build --build-dir _build_prepare -j6 \
  @scripts/preparation-test
```

The CLI checks passed without Git/PATH for declaration and live FIFO inventory.
The existing memory test passed Flops Simulation/Implementation and Exact
Simulation (1,792 edges each), both-mode inventory/policy/unsupported-shape checks.
The Dune alias independently passed the same 77 preparation checks. No physical
simulation, EDA, provisioning or Workbench test was run.

## Read retained evidence

```sh
. .dev/asic-prepare/current/activate.sh
hardcaml-asic-flow preparation-inspect acceptance/preparation/capture/exact-synthesis --json
hardcaml-asic-flow preparation-inspect acceptance/preparation/capture/unsupported-exact-128 --json
hardcaml-asic-flow preparation-inspect acceptance/preparation/capture/fifo-zero-resources --json
```

The checker verified each copied attempt using this installed reader. Original
disposable allocation paths remain in launch events for audit; use the portable
directories above for inspection. Repeats must omit `--output-dir` or select a
fresh directory, preserving this evidence.

The matrix covers both operations for explicit flops, exact macro and real
fallback; unsupported Exact, missing sources, retry isolation, refused store,
corrupt payload, explicit Simulation roles, source/config/circuit identity changes,
and historical inspection after deleting the source fixture. Source observations
identify declared bytes/status, **not proof that compiled code came from them**.
Preparation is not bundle, PDK-readiness, synthesis-retention or physical evidence.

Preserved selections verified after testing:

- SRAM: `71a9a125992e4260b38dcdf954c6b965`;
- Workbench: `f64dd69b9a1845018b6e677a296f7031`.

Existing memory/physical evidence and the recorded dependency pin were preserved.
