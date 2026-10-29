# PT7 named synthesis — C actual native acceptance

**Completed: two fresh actual public named synthesis + linked native STA executions,
sequential within C's six-job allocation.** Both finalized synthesis occurrences and
companions completed with exit0; explicit `timing-intent-inspect --kind execution`
returns exit1/completed/unavailable, as intended. Public named `report` exits0 and
contains the exact same checked timing value. Native schema2/profile2 are unchanged.

The durable bounded receipt is
`acceptance/pt7named/native-closeout-final-03/acceptance.json`.
No earlier failed capture/precheck/history was edited or completed in place.

**Validation-only R4 closeout:** C independently replayed the already-built
corrected helper against both original execution paths; inspection and entire
report JSON remain identical, with source/checkpoint bytes unchanged. See
[corrected-reader qualification](pt7named_reader_r4_final.md). The correction does
not replace the original execution generation below or imply new native runs.

## Captured provider and exact public path

After reading A's R3/alias and B's R2S/alias handoffs, `capture-final-03` captured:

- Generation: `.dev/asic-pt7named/provider/generations/ce6be246fafa4d0dbe1dd00da980482b`
- Captured source snapshot SHA256:
  `acbd7ca972fba8c3f98473fc47bd099b5ce79d82ac97f8774e1a3601f06b66d5`
- Provider receipt SHA256:
  `bebcd8f6b7362fd00265578ed38887c76843a623de5fb0cadbb03205ea94232d`

`build-final-03` freshly built the catalog consumer and public reader/precheck
adapters in `_build_pt7named`. Capture's nested build/install/consumer probe used
explicit `--jobs 6`; every Dune call used switch `5.2.0+ox`, `-j6` or equivalent,
and the designated ASIC/example shared lock. Builds and EDA did not overlap.

`area-prepare-final-03` and `delay-prepare-final-03` each executed public catalog
`Methodology_plan.prepare` followed by `Bundle.publish`, requiring exact plan/emit
equality and checking every bundle member hash. The emitter reuses the original
five-stage specimen without hardware/source changes. Original project inputs plus
the three explicit named catalog/CLI/Dune inputs are retained in each manifest.

The public precheck adapter passes the **unchanged declared input list**, explicit
canonical **whole PDK** and original support-tool roots. It does not replace paths
by canonical targets or deduplicate aliases. The new4096-source/128MiB-file/512MiB
contract admits the full1505 declared pre-launch inputs with1062 aliases, including
the67,485,696-byte GDS. This is stat admission, `hashes_verified:false`; actual
publication and public readers subsequently hash the complete retained closure.

Each run uses public `stages` with the **exact frozen** methodology-plan file,
expected plan identity and published bundle; no coarse `run`, manual STA, rerender,
recipe modification or fake coarse record is used. Returned `execution_file`
selects all subsequent public queries, with no recency selection.

| | Area | Delay |
| --- | --- | --- |
| Run receipt | `area-run-final-04` | `delay-run-final-03` |
| Actual attempt | `cb5e7cd92dbf43b4a6c00a74b61c6d72` | `9374823306a64897959e1b2295f52c84` |
| Plan identity | `85b949035d025689a14f72b0698440becc52224fdb785e710d16cd53d9d73687` | `673350dd8606ec6c8be49385eb8f109780dd1aae3df0452980efc2a8d94b7888` |
| Bundle identity | `d102a1866f7033be317a96ef01ec4ade0f3074f862d7ba2bdecdafaf7b160669` | `b778f25e704354c1bc7084b4de69076378fc084b2c8820dc6c3dede8c34ecdce` |
| Published checkpoint identity | `ce398522bace78e0f4b0249826f662ab7dce5d574f903d0c36d8ff6add78e84d` | `9b72f1aeb191a967e792e6dfb8ef5a3fbaabc8e815b94569c202aa51a58ccc62` |
| Public evidence receipt | `area-public-final-03` | `delay-public-final-03` |
| Entire public run elapsed | 32.926422s | 32.833127s |

Execution files remain at:

```text
.dev/asic-pt7named/workspaces/area-run-final-04/execution-cb5e7cd92dbf43b4a6c00a74b61c6d72.json
.dev/asic-pt7named/workspaces/delay-run-final-03/execution-9374823306a64897959e1b2295f52c84.json
```

## Native results, without timing waivers

For **each** profile, public/native verification establishes:

- Five original resolved stages; six native stored exception relations matched.
- Seven complete returned diagnostic categories;12 native endpoints.
- Three configured corners, but **only the default** `nom_typ_1p20V_25C` requested
  and actually executed. This is not all-corner acceptance.
- OpenSTA **2.7.0**, actual `sta -version` exit0 with retained version output/hash;
  actual native argv `sta -threads 1 -no_splash -exit .../driver.tcl`, exit0.
- Two actual ordered retained Liberty inputs:
  - `library-0.lib`, SHA256
    `34163f3e7de9f854afac57332ba06f1739b78e7ac35660a8a5ddd39c570124ad`
  - `library-1.lib`, SHA256
    `e6b5adf1ce31db3a0c15e5ca069c62e7d9efb604a710b8f6582700f1721d2d98`
- Both Liberty files declare `time_unit : "1ns"`. The following are **quoted native
  bounded downstream witness values**, not a new local production timing parser or
  overall design closure claim:

| Profile | Setup/max witnesses | Hold/min witnesses |
| --- | --- | --- |
| Area |3 × **+19.432287ns**, `slack (MET)` |3 × **−0.044244ns**, `slack (VIOLATED)` |
| Delay |3 × **+19.432287ns**, `slack (MET)` |3 × **−0.044244ns**, `slack (VIOLATED)` |

Reports preserve the paths `_06_ → _05_`, `_05_ → _04_`, `_03_ → _02_`. Exact
native line numbers/text, report hashes and paths are recorded in the closeout.
No waiver was added. Negative hold remains negative hold. The provider explicitly
retains downstream reports without interpreting them as exhaustive coverage.

## Exact association, checkpoint preservation and source parity

`scripts/pt7named_closeout.py` checks the final executions against their explicit
prepared plan/bundle and preflight metadata:

- One exact `implementation.synthesis` occurrence and one synthesis checkpoint per
  execution. Immutable publication binds that occurrence while **Running**; final
  occurrence is completed. It originates from `execute_segment`, not publication
  validation, and matches the exact frozen methodology/plan/bundle.
- The companion request selects the promoted checkpoint's exact `state.json`.
  Native Step `corners/state_in.json` equals that published State JSON, not candidate
  State. The checkpoint's manifest, closure, config, segment, State and two promoted
  native views—**all seven files**—still match their pre-STA publication hashes.
- The read-only early mode0400 expectation snapshot and hash agree exactly with
  `operation.json`, `preflight.json`, `prepared.json`, their checked requests and
  final execution expectation. Its mtime precedes the first retained probe result.
  Preflight directories are selected explicitly and matched by exact expectation
  and workspace, not guessed from timestamps.
- Public inspection equals named report `timing_intent` exactly. Public
  `Timing_intent_execution.source_files` returns exactly the checked view's source
  list. Each profile exposes **1584 verified sources**, including **all1486 target
  PDK paths**, every required host closure member, and the large GDS.
- Every one of the **1062 immutable external alias proofs** matches its original
  checkpoint closure key, exact canonical target/root, byte count and SHA256. Alias
  declarations are not removed or canonical-target deduplicated. Runtime authority
  uses whole PDK plus staged `project/tt`, not the precheck's original support root.
- Public queries/controls preserve original execution-tree hashes. Source inventory
  and checkpoint checks stream/re-hash actual files; no current renderer or PDK
  discovery is used by the public readers.

The two profiles happen to produce byte-identical mapped netlists on this tiny
specimen. That does **not** make their attempts, frozen methodology/bundles or
checkpoint references interchangeable.

## Real substitution negatives

`substitutions-final-04/controls.json` records one unchanged positive and five
negative captured snapshots using **real** objects from the two executed profiles:

| Control | Result |
| --- | --- |
| Unchanged captured snapshot | Pass; equals public inspector and named report |
| Other real attempt's expectation | Reject2: expectation attempt/occurrence/profile mismatch |
| Other real profile's methodology reference | Reject2: methodology contract/attempt mismatch |
| Other real published checkpoint | Reject2: methodology/checkpoint bundle or publication mismatch |
| Other real completed occurrence | Reject2: occurrence identity/order mismatch |
| Remove independently required expectation | Reject2: advertised/present evidence missing expectation |

These use B's public captured-snapshot API with the exact original execution path,
hash and validated checkpoint seam. The originals are never overwritten; no fake
coarse records or relocation workaround is introduced. They are API rejection
fixtures, not five additional EDA runs or claims that every corruption was sent
through the CLI. The positive additionally demonstrates public CLI/report parity.
All command outcomes/diagnostics and original-source immutability are retained.
The earlier narrower `substitutions-final-03` attempt remains intact.

## Explicit resource and preservation receipt

Per profile, closeout inventories21 exact launch receipts:18 preflight probes,
one synthesis execute transport, one publication-validation transport, and one
linked STA transport. Original receipts retain full argv/process/cleanup records.

- Probe timeout20s; segment/publication/analysis timeout600s; outer consumer
  command timeout900s. Host metadata inherits `OMP_NUM_THREADS=1`,
  `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`.
- Every tool-running Docker `run` uses exactly one `--cpus=6`; named executor/
  worker count is6. Linked analysis transport records workers6 and STA threads1;
  effective OpenROAD/STA configuration is1 thread and actual STA argv is1 thread.
- Docker image is pinned to
  `sha256:d109140b8f17fc54f4fca998beb8124f4949404ec52e339eebd2250854a18b5a`;
  LibreLane producer version is3.1.0.dev3. Process exits and owned cleanup are
  successful. **Two synthesis runs, two linked STA runs, zero P&R**. No build/EDA
  overlap exceeds the six-job allocation.
- `preservation-native-final-03.json` verifies **16,084 original files, zero
  changes**, including protected PT7c histories/source inputs/old provider pointers.
  Original failed prechecks and all prior named generations/receipts remain intact.

The checkpoint and methodology references remain **path-bound**. This acceptance
does not claim named archive/export, relocated runnable checkpoints, exhaustive
exception effects, reset-release/CDC safety, post-PNR qualification or timing
closure. Overall exhaustive coverage remains unavailable; inspection's exit1 is
truthful even though native execution and bounded acceptance completed.
