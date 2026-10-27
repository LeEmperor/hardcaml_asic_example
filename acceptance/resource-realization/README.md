# PT.5 resource realization acceptance

Status: **corrected frozen-provider acceptance passed** (2026-10-27 UTC).
`installed-final/verified/receipt.json` is the final focused result: **20 tests passed,
0 failures, 0 errors, 0 skips**. Public responses use the ASIC-owned
`hardcaml-asic.resource-evidence` schema. Receipts here only record test execution.

**Superseded historical capture:** `installed-04/` and `closeout.json` are preserved
byte-for-byte but predate the A/B review corrections. Their old derived schema
lacks the now-required `resource_inventory`; they are not final acceptance of the
corrected provider. `closeout-final.json` is the current closeout.

## Installed-provider reproduction

After activating the isolated provider and building `installed_api.exe` as shown
in the [guide](../../docs/resource_realization.md), run:

```sh
python3 -B scripts/check_resource_evidence.py \
  --provider .dev/asic-pt5/current/bin/hardcaml-asic-flow \
  --consumer _build_pt5/default/acceptance/resource-realization/installed_api.exe \
  --memory _build_pt5/default/memory/memory_cli.exe \
  --output-dir acceptance/resource-realization/installed-NEW
```

Use a new output directory. Raw numbered stdout/stderr, command/exit records,
mutation source/changed digests, identities and unittest outcomes are retained.
Mutation fixtures are disposable copies; the deterministic script and mutation
descriptors reproduce them without retaining rewritten copies of historical runs.

Coverage includes direct CLI/library agreement for both retained runs, precise
stage/identity/hash/count/area assertions, synthesis and independently rebound
physical missing/extra/renamed/wrong/duplicate macro rejects, missing/malformed
observations, ordinary tampering, invalid provenance, strict public-schema
rejection, collection/report agreement and archive byte closure. Fresh emitted
flop/fallback snapshots verify explicitly unavailable attribution using **synthetic
observations**, with no new synthesis claim.

Correction coverage additionally includes comma-separated macro instances with
nested connections, blackbox-flagged hidden cells/processes/memories, unreached
synthesis boundaries, a later failure after completed synthesis, unrelated live
flow aliases, observation/inventory and typed-count consistency, and a coherent
count forgery rejected by source-aware replay/report/archive despite valid shape
and unchanged source hashes. Staged fixture copies now populate actual live-flow
paths rather than relying on root snapshot aliases.

`closeout-final.json` binds provider/source/executable IDs and the final logs:

* `provider-final.stdout`: corrected generation `dd1ec9002cdc40f2936488cedd9eb0fe`,
  source SHA-256 `bc8b35619819beb0bbe20a4f0d7213864013ee4b05e9c2688e901dd1f6cb05f0`.
* `build-final.stderr`: `_build_pt5 -j6 @all` rebuilt against that generation.
* `fifo-final.stderr`: **5 standalone FIFO emission tests passed**.
* `suite-final.stderr`: full `dune runtest --build-dir _build_pt5 -j6 --force .` passed,
  with installed-provider routing enabled; unittest groups **11 + 24 + 21**,
  directed/seeded FIFO and wrapper checks, three memory replay checks, bundle/CLI
  checks, and synthesis/simulation RTL replay plus corrupted-response rejection.
* `installed-01/` and `installed-02/`: retained earlier fixture-harness failures;
  fixed staging/archive-layout assumptions. `installed-03/`: 17 passing tests
   before final additional tamper/area coverage. No ASIC edit or defect workaround.
* `installed-final/receipt.json`: first corrected-provider run; one obsolete harness
  expectation required unknown-instance details after a parser-level rejection.
  The corrected expectation and all tests pass in `installed-final/verified/`.

`python3 -B acceptance/resource-realization/record_closeout.py --final` verifies
these existing logs, executable hashes, old provider
selection timestamps and the original historical hash inventory before writing
a new closeout. It does not execute tests or reconcile resources.

Run from the example checkout (Python 3.11+, no EDA or build):

```sh
python3 -B scripts/check_resource_evidence.py --research-only \
  --receipt acceptance/resource-realization/research.json
```

The receipt destination must be new. It retains individual unittest outcomes,
failures/errors/skips, script/Python executable digests, historical provider
receipts, and before/after SHA-256 inventories of both complete retained trees.
In research-only mode, disposable mutations exercise fixture construction only;
the installed-provider mode separately asserts public rejection.

## Initial independent research

`research.json` records **8 tests passed, 0 failures, 0 errors, 0 skips**.
Both complete retained trees were hashed before and after: **276 files unchanged**.
The passing tests cover checksum inventories, manifest/run identities and stages,
synthesis instances/counts/areas, final netlist counts, physical measurement
scopes, physical artifact hashes/original verdicts, and five disposable mutation
constructors. No public required-macro rejection is counted as passing.

That earlier research run preceded the completed A/B handoffs and provider capture.
Historical provider receipts preserve source snapshot IDs but do not bind a
retained historical provider executable; that executable attribution is unavailable.

See [the resource-realization guide](../../docs/resource_realization.md) for exact
artifact semantics, executed public assertions, limitations and reproduction.
