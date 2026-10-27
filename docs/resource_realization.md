# Resource realization: retained evidence and PT.5 acceptance

## Status and public interface

Slice C independently inspected retained evidence, then completed corrected,
frozen-provider acceptance on 2026-10-27 UTC. B's completed execution handoff provides this
read-only, host-only interface:

```text
hardcaml-asic-flow resources-inspect RUN_DIR --json
Hardcaml_asic_execution.Resource_evidence.inspect ~run_dir
```

CLI exit 0 means required reconciliation passed, 1 failed/unavailable required
evidence, 2 invalid input/provenance. The ASIC-owned JSON contract is
`hardcaml-asic.resource-evidence`, schema 1, also embedded by collection and used
by report. Acceptance asserts structured outcomes, not just exits. The corrected
schema also requires the manifest-derived `resource_inventory` anchor; observations
must agree with its complete expectation rows. Source-aware verification replays
the full reconciliation over actual source bytes, not merely their hash inventory.
The independent research receipt predates implementation acceptance. The final
`installed-final/verified/receipt.json` records **20 passing tests, no failures/errors/skips**.
The older `installed-04/` capture and `closeout.json` are preserved but superseded:
they predate the independent-review fixes and lack the new inventory anchor.
Run the public acceptance or research-only mode using the commands in
[`acceptance/resource-realization/README.md`](../acceptance/resource-realization/README.md).

## Independent synthesis findings

All paths below are relative to `acceptance/sram/8b48d7d0-functional/`:

* `manifest.json`: bundle
  `4fe842a7c07b94ae9e8e0546210c9273d019fccdca2d5cbf84311948bde64d09`.
  `run.json`: run `8b48d7d0818d494f8a9c45000c2bcbbd`, completed synthesis.
  Its historical absolute paths must not trigger source/PDK discovery.
* `mapped.json`, `modules.tt_um_program_memory.cells`: one instance
  `hc_resource_7_program` of `RM_IHPSG13_1P_256x16_c2_bm_bist`, also visible in
  `mapped.v` line 917. Module declarations/blackboxes are not instances.
* `stat.json`, `design.num_cells` is **176 total mapped cells**, including the
  macro, hence **175 standard cells**. `num_cells_by_type` agrees with mapped JSON.
  `physical-p4/results.json` historically labels 176 as a standard-cell instance
  count; preserve that report, but correct the semantics in the new public output.
* `stat.json`, `design.area`: **2,182.7232 µm²**. `synthesis.log` lines 990–993
  explicitly say the macro area is unknown and report that same area. This proves
  the macro is excluded; merely seeing two `-liberty` arguments is insufficient.
* `models/RM_IHPSG13_1P_256x16_c2_bm_bist_typ_1p20V_25C.lib`, cell declaration
  line 126 and area line 148: **28,127.104 µm²**. Match the Liberty cell name to
  the observed/expected macro type before adding. Their sum **30,309.8272 µm²**
  is a combined cell-area **estimate**, not placed/routed, core, die or occupancy.
* The 16 `sg13cmos5l_dfrbpq_1` cells and **783.8208 µm²** sequential area are
  whole-design staging state. They are not the SRAM's implementation flop cost.
* `manifest.json` carries implementation and behavioral simulation inventories
  separately, no `resource_snapshot`. Use B's explicit legacy adapter; do not
  insert a snapshot or attach the later PT.4 preparation by resemblance.
* `provider-receipt.json`: observed ASIC base
  `bba13079abd519b984e522aa7e898cbef85f4139`, captured snapshot
  `8f054fde7462a687139b31564fd823bedb4e0a0f1d7197ea813dcefee27214ca`.
  This records captured dirty bytes, not proof of a clean constructor build.

## Independent physical findings

All paths here are relative to `acceptance/sram/physical-p4/`:

* `bundle/manifest.json`: bundle
  `fa38d9064dffdf2ec1578c79c2e8890eba81bf704af460e85fcc6031b707d53c`.
  Accepted `run.json` run is `be961b2c95f74c81ad6af81ca4d2b269`, completed full.
  This is a distinct build/run from the synthesis specimen above. Failed p3 even
  shares its bundle identity and final netlist digest; bundle or netlist alone
  does not identify an accepted execution. Never select `failed-attempts/` metrics.
* `mapped.json` remains **synthesis** evidence (176 cells), despite residing in a
  physical acceptance directory. `mapped.v` is instead the **final** netlist,
  byte-identical to `flow/final/nl/tt_um_program_memory.nl.v`. Basename matching
  would incorrectly join stages.
* Final netlist contains one exact macro and 16 original flops, plus 81
  `sg13cmos5l_dlygate4sd3_1` combinational delay gates. Prefix `dl` alone would
  misclassify those as storage. Final type inventory is in `summary.json`.
* `metrics.json` keys: `design__instance__count` **68,929**;
  `design__instance__count__stdcell` **389**;
  `design__instance__count__class:fill_cell` **68,539**; macro count **1**.
  Fill class includes 68,227 decaps and 312 fillers. The 389 excludes that class.
* `design__instance__area__stdcell` **4,793.64 µm²** is a separate physical-stage
  standard-cell area, not the synthesis estimate. Aggregate instance area
  **899,576 µm²** includes physical-only cells; fill-class area is **866,655 µm²**.
  Macro physical metric **28,127.1 µm²** is rounded, distinct from exact Liberty
  area. Reported core/die areas are **902,417/916,214 µm²**. Keep all scopes distinct.
* `design__instance__utilization__stdcell` **0.0054829** differs from aggregate
  utilization **0.0364806**. Do not infer an exact occupancy denominator from
  these percentages or divide synthesis area by physical core area.
* `physical-checks.json` and `results.json.physical_evidence` bind artifact hashes:
  final netlist, `flow/53-openroad-fillinsertion/*.pnl.v`,
  `flow/69-netgen-lvs/lvs-reader.json`, power geometry and final GDS. Preserve the
  existing passing gates: three raw Magic findings with exact stock disposition,
  clean real-GDS KLayout, and **abstract macro-boundary LVS with schematic CDL**.
  Internal-device LVS remains unverified.
* `results.json.postchecks[0]`: same run/build, completed gate/precheck pass;
  postcheck `0553f6d19c8f42d28c057fc65ed23510`. Whole-chip slack and all-corner
  zero slew/cap violations do not establish resource-linked endpoint attribution.
* `provider-receipt.json`: observed ASIC base
  `ca4a42e30c11aff66cd1679d13e7175cce59a9b0`, captured snapshot
  `632cb3358e36d193d3a580b9fa11164b8f376673d259bfbcfdd46ee1fdf68b99`.

## Portable fixture and reproduction procedure

Historical snapshots are curated evidence, not complete run-directory layouts.
In particular physical metrics live at root `metrics.json`/`metrics.csv`, final
GDS at `final.gds`, bundle under `bundle/`, and flow artifacts under `flow/`;
`flow/final/` itself only has `nl/` and `lef/`. Physical synthesis `stat.json`
and synthesis log are not retained in this snapshot. Synthesis has no complete
bundle inventory, only manifest, source copies and selected collateral. Original
absolute run paths may exist locally but are not portable acceptance inputs.

B confirmed and acceptance exercised direct inspection of both retained directories.
The general `Collect_service`/archive APIs use the ordinary staged run layout.
The script reconstructs that layout in **disposable copies**, preserving actual
source bytes and recording every source-to-destination mapping. The complete
physical bundle is copied to `project/`, `flow/` to `project/runs/asic/`, root
metrics/GDS and retained runtime scripts to their standard paths. The disposable
run's bundle path is relocated, keeping its new run-file digest explicit. Physical
synthesis stat/Liberty inputs remain absent; the older run's inputs are not borrowed.
Retained `mapped.json` is copied to the real producing synthesis path in staged
fixtures. Root mapped/stat/metrics aliases are only valid for explicit curated
snapshot layouts; they cannot stand in for absent or unrelated live-flow outputs.

1. Capture the provider into `.dev/asic-pt5` after readiness; preserve the
   receipt, source snapshot digest, executable path and executable SHA-256.
   Keep its private build distinct. Any nested Dune command must explicitly use
   `-j6` and count within C's allocation of six. Any Dune in the ASIC checkout
   must use `/tmp/opencode/asic-pt5-build.lock`; capture builds a distinct private
   source directory and can overlap checkout reviews. Serialize example Dune with explicit `-j6`
   and build directory `_build_pt5`. Do not change provider selections.
2. Invoke the public inspector with no tools/PDK available. Assert contract/schema,
   run/build/manifest digests, legacy coverage, observation producer and stage,
   exact macro identity/type/count, artifact digests and required check outcomes.
   Require synthesis and final physical observations to remain distinct. Assert
   the derived areas/counts above with declared unit/scope and evidence references.
3. Assert unavailable reasons for separate-preparation linkage, per-resource flop
   cost, and unsupported resource timing/electrical attribution. Missing required
   macro evidence must instead fail closed. Verify collection/report agree with
   the inspector and archives retain all advertised evidence bytes.
4. Use `mapped_mutation` from the script on disposable fixture copies for missing,
   extra, renamed-same-count, wrong-type-same-count and valid-empty observations.
   Keep stat counts unchanged first to catch count-only false positives; add
   coherent count variants to isolate instance reconciliation. Also remove the
   observation file separately (unavailable is not a valid empty observation).
   Mutate disposable final netlists independently from synthesis JSON. Assert
   missing/unexpected/unresolved outcomes and required-check rejection, retaining
   command, exit, raw stdout/stderr, structured outcomes and changed digests.
   Distinguish stale hash/provenance rejection from actual reconciliation rejection.
5. Add stale run/build/stage and manifest-hash negatives, malformed observations,
   and explicit malformed preparation-link rejection through B's supported seam.
   Verified new linkage, if supplied, requires fresh emission plus config/circuit
   mismatch negatives; old retained runs cannot cover it.
6. Run `scripts/test_flow_emit.py /absolute/_build_pt5/default/bin/project.exe
   /absolute/example/source` standalone. This is named-flow FIFO **emission
   compatibility** only. The memory CLI remains coarse macro acceptance, with no
   named macro checkpoints. Retain full unittest outcomes and executable identity.
7. Hash both complete historical trees before and after all tests. Publish a new
   acceptance receipt with assertions, counts, skips and limitations; original
   records remain historical evidence.

## Executed acceptance and exact identities

The isolated capture used:

```sh
opam exec --switch=5.2.0+ox -- python3 -B scripts/asic_dependency.py \
  --store .dev/asic-pt5 refresh --source /home/wayne/devel/jane/hardcaml_asic \
  --mode development --jobs 6
```

Final generation: `.dev/asic-pt5/generations/dd1ec9002cdc40f2936488cedd9eb0fe`.
Observed ASIC base: `e183475325a0a976988383037e66fc402fff5a83`.
Final captured source snapshot: `bc8b35619819beb0bbe20a4f0d7213864013ee4b05e9c2688e901dd1f6cb05f0`.
This is a dirty development capture receipt, not a clean-source or P6 stamp.
Exact provider, installed-library probe, memory and FIFO executable hashes are in
the focused/closeout receipts. The installed probe is a thin public-API consumer,
not a local reconciliation implementation.

**Superseded:** generation `f4ba4e800613412d8ec8b3940f6217e4`, source snapshot
`d2f8c7058c1ebf0603d2ddfa3024ed1f9687661e73e495ea313f8ee3e93cdeb4`.
Its `installed-04/` and original closeout remain intact as historical acceptance
records. They do not validate the corrected parser, hierarchy/boundary rules,
inventory/typed-count consistency, source replay or collateral cross-check.
The current receipts are `provider-final.stdout`, `installed-final/verified/receipt.json`
and `closeout-final.json`.

Example builds were serialized; capture used its own private source/build:

```sh
# In a 5.2.0+ox environment:
source .dev/asic-pt5/current/activate.sh
dune build --build-dir _build_pt5 -j6 @all
dune build --build-dir _build_pt5 -j6 acceptance/resource-realization/installed_api.exe
# Run the public acceptance command in acceptance/resource-realization/README.md.
python3 -B scripts/test_flow_emit.py "$PWD/_build_pt5/default/bin/project.exe" "$PWD"
HARDCAML_ASIC_TEST_PROVIDER="$HARDCAML_ASIC_GENERATION/bin/hardcaml-asic-flow" \
  dune runtest --build-dir _build_pt5 -j6 --force .
```

Full logs and command receipts are under `acceptance/resource-realization/`.
All direct inspector/probe invocations used an empty tool PATH and nonexistent
toolchain. Fresh source emission and standalone FIFO tests use Git but no EDA.
The five FIFO tests and full example suite passed after focused acceptance.
The corrected final focused run also asserts `resource_inventory`, every
comma-separated physical macro instance, unsupported hierarchy, synthesis
completion boundaries and full source-derived replay. All **276 historical files** match the original research
inventory after every focused run and at closeout. Normal ASIC, SRAM, preparation
and Workbench provider pointers predate the initial research; no selection changed.
No ASIC checkout build/edit or physical EDA was performed by C.

### Negative outcomes actually asserted

| Disposable mutation | Public outcome |
| --- | --- |
| Synthesis missing or valid-empty inventory, coherent stat | CLI 1; required failure; resource `missing` |
| Synthesis extra or renamed same-count macro | CLI 1; `unexpected`; extras visible |
| Wrong known standard-cell type at required identity | CLI 1; `unexpected` |
| Wrong undefined macro type | CLI 1; `unresolved`; realized inventory unavailable with non-leaf/non-library reason |
| Missing/malformed synthesis JSON | CLI 1; `unresolved`, realized inventory unavailable |
| Extra cell with stale aggregate stat | CLI 1; explicit measurement/count error |
| Physical missing/extra/renamed/wrong/duplicate instance, checker and run hashes rebound | CLI 1; final physical failure while synthesis remains passing |
| Final netlist/checker/GDS ordinary tamper | CLI 1; explicit integrity failure; no semantic-pass claim |
| Full run not yet physically completed | CLI 1; stage-not-reached unresolved |
| Stale build/manifest hash, tampered manifest, invalid run stage | CLI 2; invalid provenance |
| False preparation claim, stale observation stage/build, false realized count, NaN measurement | Public strict validator rejects with reason |
| Changed Liberty without preflight hash rebinding | Retention passes; macro/combined area explicitly unavailable |
| Changed source after producing resource evidence | Public `verify_sources` and archive refuse stale bytes |
| Comma-separated macro instances in one declaration with nested connection expression | CLI 1; both macros counted, extra identity visible, physical `unexpected` while synthesis passes |
| Blackbox-flagged library module contains hidden cells/processes/memories | CLI 1; required reconciliation unresolved, non-leaf/non-library reason |
| Failed/interrupted/completed run with null synthesis completion boundary | CLI 1; mapped file does not establish synthesis completion |
| Later physical failure after completed synthesis | Synthesis stays passing; final physical unresolved |
| Root mapped alias with unrelated staged-live producing flow | CLI 1; alias does not rescue absent bound evidence |
| Erased observation rows or typed macro-count contradiction | Public schema reader rejects inconsistent assertion |
| Fully coherent forged counts over unchanged source hashes | Shape reader passes; source replay, report and archive reject; no archive published |

Rebound physical fixtures deliberately retain the real GDS and other artifacts
while changing the final netlist and its declared checker/run digest chain. They
test **semantic reconciliation after integrity validation**, not requalified
geometry or authenticated producer claims. Fixture mutations retain source and
changed digests plus the deterministic operation in the script.

Collection equality is checked against public inspection. Authoritative report
accepts the original retained physical global results while adding fresh resource
evidence in memory, and rejects the physical semantic negatives. A reconstructed
copy retains those global results and adds the new resource object for archival;
the script verifies **every advertised source's exact bytes inside `reports.tar.gz`**.
It also checks report inspection leaves stored results unchanged. General collection
cannot restore missing historical synthesis-stat coverage; its entire global result
is not asserted as a replacement accepted historical report.
The count-forgery test adjusts typed standard-cell counts and total/standard-cell
measurements consistently, retaining the real source hashes. Its offline schema
validity is intentional: rejecting it through source-aware replay demonstrates
the corrected guarantee that hash integrity alone cannot establish an assertion.

### Remaining limitations

* Separate-preparation linkage is explicitly unavailable; no verified linkage API
  or fresh config/circuit mismatch acceptance is claimed.
* Per-resource flop ownership/cost and resource-linked timing/electrical attribution
  remain unavailable. Fresh emitted flop/fallback snapshots are exercised with
  synthetic observation fixtures, not newly synthesized implementations.
* Physical snapshot synthesis stat/Liberty areas remain unavailable through the
  public API. Final footprint/utilization denominator/internal-device LVS/IR-EM
  and timed SRAM conformance are not established by these tests.
* Final public `standard_cell_count` is **68,928 netlist non-macro instances**,
  explicitly including fill/decap/tap/tie cells present; it is not the native
  placement metric's **389** logical standard cells. Their different scopes are
  asserted rather than silently equated.
* Historical executable/source authentication is unavailable. New inspector and
  consumer executable identities are recorded, but do not authenticate old tools.

Earlier harness-only failures are retained in `installed-01/` (unstaged collection
manifest) and `installed-02/` (archive output is a directory containing tarballs).
`installed-03/` passed 17 tests before expanded coverage. The old `installed-04/`
passed 18 tests before A/B's independent-review corrections and is superseded.
The first corrected-provider attempt is retained at `installed-final/receipt.json`:
one obsolete harness assertion expected complete unknown-instance details even
after the stricter leaf parser rejected an undefined module. That harness assertion
was corrected; `installed-final/verified/` passes all 20 tests. No new ASIC fix or
workaround was needed by C. A/B's own handoffs retain their direct collateral and
macro/standard-namespace area-overlap regression results; C does not count those
provider-owned tests as independent example assertions.
