# Final consumer validation — 2026-10-25

## Capture and retained identities

Provider generation: `a5de7cbfcc464e13ae1b5a5db6e39068`.

Provider captured SHA-256:
`549cf74e17b4c8af34a7133ea3d983786adf5ce6c4d4e8914f62aff0a05e2f2a`.

| Case | New attempt ID | Preparation identity |
| --- | --- | --- |
| Exact synthesis | `53dfde6a551a4911b104ad52c023290b` | `fd456fbf5035f7b86d0816d78a6d6323932f73c761ae4d522d0a0cc5e7593fbb` |
| Zero-resource FIFO | `557b71387a454d12b0a245402898bcc7` | `8cedb61350e9bf3d9d22ed93a0af8295dd3433886a9bd0d23563ed10a7709d9b` |

Both preparation identities and payload byte digests match the original v1
capture. New workflow descriptors are v2, outer schemas still 1. Old descriptor
v1 remains unchanged and readable. Preparation/source hashes observe declared
bytes; they do not prove the compiled constructor came from them.

`historical-compatibility.json` retains the original operations, explicit identity
comparisons and before/after fingerprints for **every file** under the original
`capture/`: SHA-256, byte length, mtime and path. They compare equal. New evidence
was written exclusively under `capture-final/` and disposable `.dev` fixtures.

## Commands executed

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
  --source-root "$PWD" --historical-dir "$PWD/acceptance/preparation/capture" \
  --output-dir "$PWD/acceptance/preparation/capture-final"
HARDCAML_ASIC_PREPARATION_PROVIDER="$PWD/.dev/asic-prepare/current/bin/hardcaml-asic-flow" \
HARDCAML_ASIC_PREPARATION_SOURCE_ROOT="$PWD" \
  opam exec --switch=5.2.0+ox -- dune build --build-dir _build_prepare -j6 \
  @scripts/preparation-test
opam exec --switch=5.2.0+ox -- dune runtest --build-dir _build_prepare -j6
```

All passed. The checker rejects named-pipe operation/snapshot artifacts with
reader exit 2 within a five-second bound; no duplicate reader implementation.
Consumer project code and compiled-source coverage semantics were unchanged.

Full example test results:

- 89 focused preparation checks (also passed through the focused alias).
- CLI declaration/help/invalid-command and Git/PATH-free live-inventory checks.
- 11 recorder-only bootstrap tests; no real provisioning.
- 24 isolated dependency-setup tests.
- 21 routing tests: 20 passed, one installed-native fixture test skipped because
  `HARDCAML_ASIC_TEST_PROVIDER` was not supplied.
- Memory cycle/policy tests: Flops Simulation/Implementation and Exact Simulation,
  1,792 edges each; both-mode inventory, hardening intent and unsupported shape.
- FIFO directed/seeded core and wrapper tests, resolution and catalog tests.
- Bundle deterministic/provenance/failure checks and generated synthesis/simulation
  RTL replay, 11,429 edges each; both deliberately corrupted oracles rejected.

No physical EDA, PDK provisioning, Workbench tests or workspace Git mutation.
Existing setup/routing/bundle tests use disposable synthetic Git fixtures.
SRAM selection remains `71a9a125992e4260b38dcdf954c6b965`; Workbench selection
remains `f64dd69b9a1845018b6e677a296f7031`. Original preparation and SRAM evidence
remain retained.

## Practical read-only historical comparisons

From the example checkout, use the immutable final generation explicitly:

```sh
PROVIDER="$PWD/.dev/asic-prepare/generations/a5de7cbfcc464e13ae1b5a5db6e39068/bin/hardcaml-asic-flow"
OLD="$PWD/acceptance/preparation/capture"
EXACT_ID=fd456fbf5035f7b86d0816d78a6d6323932f73c761ae4d522d0a0cc5e7593fbb
FIFO_ID=8cedb61350e9bf3d9d22ed93a0af8295dd3433886a9bd0d23563ed10a7709d9b
"$PROVIDER" preparation-inspect "$OLD/exact-synthesis" --json
"$PROVIDER" preparation-inspect "$OLD/unsupported-exact-128" --json
"$PROVIDER" preparation-inspect "$OLD/fifo-zero-resources" --json
# Same: matches. Different explicit current preparation: differs.
"$PROVIDER" preparation-inspect "$OLD/exact-synthesis" --current-identity "$EXACT_ID" --json
"$PROVIDER" preparation-inspect "$OLD/exact-synthesis" --current-identity "$FIFO_ID" --json
# Failed attempt: unavailable, not an empty successful inventory.
"$PROVIDER" preparation-inspect "$OLD/unsupported-exact-128" --current-identity "$EXACT_ID" --json
```

The supplied IDs also identify the final retained current preparations. This is
explicit content equality/comparison, not automatic source or binary validation.
Repeat the matrix without `--output-dir` or with a fresh directory.
