# Independent physical timing qualification — C

2026-10-29. **Native interface qualification passed198 controls across all three
corners, plus standalone/ODB-readback clock API controls.** Exact emitted RTL and
timing-environment preservation passed. Deterministic RTL replay passed512
observations with a valid intentional failure control. Fresh public all-corner
synthesis baseline has completed all three actual corners with the expected
negative hold retained. Coordinator has authorized full attempt1 after B's F1–F6
corrections; a fresh corrected capture and Hardening emission passed admission.
**Bounded physical and portable-source acceptance is complete.** Actual full
attempt1 completed routing/RCX/STAPostPNR and all-corner timing pass; normal
TT/final-netlist checks and public report pass. Archive-only republication restores
all423 advertised raw artifacts and passes exact hidden-input inspect/collect/report
parity; all449 archive members match the original run bytes. A's independent actual
review confirms1720 assertions. Full attempts used: **1/2**, no repair rerun.
Actual thread accounting is dedicated all-corner STA1 and linked STA1, with
mid-PNR OpenROAD steps36/38/43 requesting6 (step31 requests1), within allocation6.
Coordinator accepted this disclosed methodology discrepancy without physical repeat.
Earlier findings/blocked checkpoints below are historical; their pre-correction
documentation bytes are snapshotted in `evidence/portable-before-01/`.
B's reviewed macro-free model adapter passed actual positive/negative Icarus
qualification for all four supported reset-flop masters. Synthesis public
inspection/collection/report/archive/restoration replay passed, including hidden
original inputs. Earlier vendor-model failures remain retained below.
All16,377 historical files/selectors remain unchanged after synthesis/replay.

## Scope and execution gates

The authoritative plan is
`hardcaml_asic/docs/development/timing-physical-qualification.md`.
New consumer source belongs to `physical_timing/`; dependency captures, command
receipts, raw logs, bundles and EDA outputs belong only to
`.dev/asic-timing-physical/`. Dune uses `_build_timing_physical`, switch
`5.2.0+ox`, explicit `-j6` or lower and the shared ASIC/example PT7 build locks.
C's six workers are shared by builds and EDA, which serialize. Dedicated pre/post-
PNR all-corner STA and linked STA serialize with one native thread. Actual mid-PNR
OpenROAD steps36/38/43 requested6 threads (step31 requested1); these stayed within
the six-worker allocation. Initial native controls used one thread. Existing
histories, provider selectors, project
configuration and PDK files are read-only inputs.

Before full flow: A's public physical-resolution/checked-endpoint contract and B's
coarse full/all-corner/audit3/runtime limit handoffs must be available, native ODB
controls must pass, and a fresh all-corner synthesis baseline must complete.
The authorized physical budget is one ordinary public full flow and one further
full run only after a recorded specific diagnosis and behavior-preserving repair.
There are no blind retries. A further attempt requires coordinator plan revision.

## Preserved design and timing

The original `timing/timing_specimen.ml` supplies three capture and two synchronous
control stages. The physical consumer will reuse these exact source bytes via
Dune `copy_files`, with scalar `ena` as the asynchronous capture source. It keeps
20 ns clock, 0/1 ns input delays, 0/2 ns output delays, 0.25 ns uncertainty,
0.15 ns transition, 0.95/1.05 derates and existing output loads. Only first-stage D
and the five enumerated RESET_B controls receive timing exceptions. No register,
latency or reset change is authorized. Negative hold results remain failures;
uncertainty is not reduced to obtain a pass.

## Initial integration state (historical)

Initial workspace instructions, queue, preservation status and qualification plan
have been read. Neither physical handoff existed at the initial inspection.
The current public `Timing.create` exposes stages and exceptions but has no
physical-policy/all-corner opt-in yet. No EDA has been launched and no production
source, emitted bundle or PDK has been patched. `physical_timing/preserve.py`
seals existing histories and provider selectors into a new immutable baseline.

Required handoff details: exact public opt-in signature, qualified cell set and
checked endpoint-map API (A); exact public run arguments and enforced container,
flow, OpenROAD, KLayout, postcheck and STA limits plus audit3/closure schema (B).
Native controls can begin after the relevant interfaces are known; full flow
remains gated on both confirmations and the synthesis baseline.

## 04:36 UTC — first fresh capture blocked at A/B API integration

`capture-native-01` failed after 25.64 seconds, exit1, while compiling the private
captured provider under the ASIC shared lock, switch5.2.0+ox and nested jobs6.
Raw log:
`.dev/asic-timing-physical/evidence/capture-native-01/capture/stderr.log`.
`execution/results/timing_intent_evidence.ml:297` supplies `expected` as a string
to `String.ends_with`; its actual type is now
`?physical:bool -> unit -> string`. A's serializer signature changed while B's
reader call site had not yet integrated it. Required fix belongs to A/B: update
the production caller for the explicit physical flag and final unit argument,
preserving default-policy replay. C has not patched the captured provider.
There is no installed generation and no EDA was launched. A new capture waits
for an actual source correction, rather than retrying these same inputs.

The preservation baseline records **16,377 files**, including existing timing,
named, resource and SRAM evidence plus protected provider selectors. The explicit
public opt-in emitter and native-control/functional replay consumers are now in
`physical_timing/`. Both handoffs have been read; they currently publish contracts
before implementation readiness. Full flow has consumed zero attempts.

## Native functional-model defect — ordinary final replay integration needed

`physical_timing/check_testbench.py --attempt testbench-01` compiled the retained
five-flop mapped specimen with actual unchanged vendor standard-cell RTL and UDP
models using host Icarus, one-CPU affinity and one native worker. Compilation exits0,
but **both positive and intentional-negative executions exit1 at observation8**,
101 ns (`expected=00 got=0X`). This is not a passing negative control: the positive
baseline is invalid. Raw logs are under
`.dev/asic-timing-physical/evidence/testbench-01/{compile,positive,negative}/`.
Compile diagnostics explicitly say `$setuphold`/`$recrem` timing checks are unsupported
and `delayed_CLK`, `delayed_D`, `delayed_RESET_B` will not be driven. The vendor
`sg13cmos5l_dfrbpq_1` model uses those delayed signals in its UDP functional path.
This is an actual simulator/model limitation, not inferred metastability.

Provider `physical_runtime.replay_models` already has a reviewed zero-delay
functional adaptation for this exact flop, but currently requires
`manifest["macro_contract"]["implementation_simulation"]`. Macro-free ordinary
postchecks cannot use that SRAM-only entry point. B/coordinator must support the
same reviewed functional-view contract for the macro-free physical timing profile
(including exact realized supported sizing if needed), retaining model/PDK hashes
and explicitly limiting the claim to zero-delay digital functional replay.
Do not change PDK bytes or patch the final netlist. C has made neither change.
No repeat was attempted without a diagnosed model/runtime correction. Fresh normal
final-netlist functional acceptance remains required; this retained-input test is
only checker preparation and grants no physical acceptance.

## Native physical resolver qualification — 66 actual controls passed

A corrected the initial serializer integration by restoring the historical
`Timing_tcl.render` signature and adding `render_physical`. New capture
`capture-native-02` succeeded (45.88 seconds): generation
`13c5a0a77460474693bec81c74fe6707`, source snapshot
`814602be030788d036f2b8ce810dbf4a51d589ce0bdc078ce06c3b506590db05`.
The isolated public physical emitter built and emitted the unchanged opt-in SDC
successfully in `build-native-01` / `synth-emit-native-01`. This preliminary
generation is for native interface qualification; B full admission is not ready.

`native-suite-01` completed **66 distinct native controls**: 33 standalone STA and
33 ODB-backed OpenROAD. Each has a complete successful enclosing process, input
hashes before/after, 1-CPU/1-thread/4-GiB/128-PID container ceilings, exact immutable
image and confirmed owned-container absence. All inputs were unchanged. Controls
load actual typical Liberty; OpenROAD additionally loads the actual technology
and cell LEF (84 cells), creates an ODB-backed design and retains positive ODBs.

Passing controls: direct baseline; all five flops sized to supported `_2`; moved
anchor through one/eight buffers; one/eight buffers on capture, reset, clock and
interstage roles; each of the three qualified delay cells on each source/interstage
role. Rejection controls: ninth anchor/source/interstage hop, inversion, unqualified
AND transform, contention at the top input root and extra sequential state. Every
negative rejected before any false-path exception appeared in native serialized
state; checked endpoints were unavailable. Every positive retained exactly five
native registers, queried all endpoint objects via A's checked map and retained
three nonempty downstream minimum path reports (maximum reports are also retained).
Raw logs/SDCs/maps/reports/ODBs:
`.dev/asic-timing-physical/controls/native-suite-01-*`; immutable per-control
references and summary:
`.dev/asic-timing-physical/evidence/native-suite-01/`.

The ordinary direct typical native control retains **−0.044244 ns hold slack**:
clock-to-Q arrival0.199838 ns, ideal launch/capture clock delay0, uncertainty
**+0.250000 ns**, library hold−0.005918 ns, required0.244082 ns. This explicitly
shows the inherited uncertainty contribution; it is preserved unchanged. This is
a native control on retained mapped input, not fresh all-corner synthesis or
extracted post-PNR closure. No P&R has run and the full-attempt budget is untouched.

### All three real Liberty controls completed

`native-fast-01` and `native-slow-01` each passed the same 66 distinct controls
against their actual fast and slow libraries, still serial one-thread native
processes. **Total:198 controls**, 99 standalone STA and 99 ODB-backed OpenROAD,
with passing baselines at every corner. Native input receipts bind the exact
libraries to their hashes (matching A's table). This qualifies the actual native
object/checked-map/bounded-transform interfaces at all three corners; fresh public
all-corner synthesis and full extracted timing/closure remain pending B readiness.

C's public-run launcher will retain B's ready handoff and its hash, then verify
actual run/config/process worker evidence. Please explicitly confirm in B's
handoff: preflight/probe transport workers<=6, implementation container CPUs6,
flow jobs6, OpenROAD6, KLayout DRC/XOR6, dedicated all-corner and linked STA corner
workers1/native `-threads 1`, TT/final replay nested budgets<=6, bounded timeout and
owned-container cleanup. C will fresh-capture after that confirmation. All native
controls now pass, so B readiness and the model-runtime fix are the remaining
integration dependencies rather than the physical object interface.

Accounting correction after actual independent review: the initial handoff's
blanket in-flow STA1 wording did not describe repeated mid-PNR OpenROAD steps36/
38/43, which actually requested6. Dedicated all-corner and linked STA remained1;
the corrected actual accounting and coordinator disposition are at the end.

`clock-sta-01` / `clock-odb-01` additionally passed B's exact native clock and
annotation hooks: `sta::all_clocks`, `get_property $clock is_propagated`,
`set_propagated_clock [all_clocks]`, `report_parasitic_annotation
-report_unannotated`, and native propagated-clock SDC serialization. The OpenROAD
probe **read back the retained baseline ODB** in a fresh process before reapplying
the emitted SDC; five checked stages still resolved. This is a clock/object API
control without extracted parasitics, not evidence of routed clock delays or
successful SPEF annotation. Raw clock-state/annotation/process sources are in
`.dev/asic-timing-physical/controls/clock-{sta,odb}-01/`.

Native direct-path control attribution (all values ns; retained mapped input,
**not** the fresh synthesis acceptance baseline):

| Actual Liberty | Clock-to-Q/data arrival | Launch/capture network | Uncertainty | Library hold | Required | Slack |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| fast | 0.141575 | ideal0 / ideal0 | 0.250000 | +0.000652 | 0.250652 | −0.109076 |
| typical | 0.199838 | ideal0 / ideal0 | 0.250000 | −0.005918 | 0.244082 | −0.044244 |
| slow | 0.294262 | ideal0 / ideal0 | 0.250000 | −0.013615 | 0.236385 | +0.057878 |

Reports use native six-digit rounding; slack is taken directly from native report,
not recomputed from the rounded rows. Derates remain early0.95 / late1.05.
`native-controls-review.json` independently rereads all198 command receipts,
source hashes, log hashes, successful process/cleanup outcomes and **both** min/max
reports on all three downstream paths per positive control. It passed.
`preservation-after-native.json` verifies all16,377 original files/selectors with
zero changes after these controls.

`emission-native-01.json` verifies that the newly emitted synthesis RTL is
**byte-identical** to the retained original scalar specimen:
`dc387d8d445d55cbd75eb11d71bf5c36f4dc7ce395749e476e3614af55f2124a`.
The entire emitted SDC prefix before the resolver is also byte-identical to the
original, covering clock/uncertainty/transition/derates, driving cells, fanout,
6 fF loads and all min/max I/O delays. Only the explicit physical resolver policy
and metadata differ; C has not changed architecture or relaxed timing constraints.

The same unmodified deterministic testbench now passes against the exact fresh
emitted RTL (`testbench-rtl-01`): **512 observations**, positive exit0 and intended
negative exit1 at observation20. This distinguishes the earlier vendor delayed-
signal/Icarus failure from a bad functional scoreboard. One-CPU affinity, raw
compile/replay logs and all input hashes are retained. Final mapped/routed replay
still requires the ordinary production zero-delay model integration; no PDK or
final-netlist patch is an acceptable substitute. The relevant production branch
is `execution/results/postcheck_service.ml:208–246`: only macro `physical=true`
currently selects and hash-checks `physical_runtime.replay_models`; the macro-free
timing marker currently only lowers worker limits, leaving the broken raw model.

## 05:24 UTC integration checkpoint — full launch still blocked

B's handoff remains its initial 80-line contract, explicitly saying it is **not
readiness for C's full run**, without the forthcoming implementation/resource-
limit confirmation. C has therefore not launched public synthesis or P&R against
the preliminary capture. No full attempt or repair rerun has been consumed.
This is an external integration gate, not physical acceptance or a failed routed
design. The ordinary final-gate model defect above also remains unresolved in the
production postcheck source at this checkpoint.

After B confirms readiness, the consumer route is implemented in
`physical_timing/acceptance.py` and `physical_timing/public_flow.py`: fresh capture,
locked build, emission with exact original RTL/environment byte checks, ordinary
public synthesis, inspection of three actually executed corners, then one ordinary
public full launch. The full launcher requires the actual synthesis inspection
and maintains exclusive first/second full-attempt ledgers; the second requires a
written diagnosed repair plan. `archive_replay.py` implements ordinary archive
restoration and public inspect/collect/report replay in a read-only child namespace
with the original example/PDK and ASIC source hidden. These full/postcheck/archive
paths have CLI/import checks only and are **not labeled executed acceptance**.

Latest preservation receipt `preservation-checkpoint-0524.json`: **16,377 files,
zero failures**. Provider selectors, project configuration and histories remain
unchanged. Every actual native PDK input retains matching before/after hashes.
No source or emitted-bundle patch, PDK edit, Git mutation, provider reselection,
SRAM rerun or daemon operation was performed by C.

## READY6 synthesis integration — 07:05 UTC actual baseline

Coordinator authorized fresh all-configured synthesis and adapter replay under
READY6, with **full launch explicitly held for A's F1–F6 findings**. C read both
current-authority handoff and independent review before proceeding. New capture
`capture-synthesis-01` succeeded, generation
`875e76c936d14c49817afce1ddb41342`, source snapshot
`564e0893579c0cb0cc4f91167728ca14c549ab1bd8e2243d5fb6660ed2d15dc0`.
Locked consumer build `build-synthesis-01` and fresh emission `synth-emit-01`
succeeded. Original RTL and timing-environment bytes still match exactly; bundle
identity remains `0209f9ab1b8729dfe39c9776fade08860603797eef0a2639f967cc77cc6d4803`.

`synthesis-run-01` used the ordinary public `run --stage synthesis`, explicit
900-second TERM deadline plus60-second kill grace, container/flow/OpenROAD limits6,
dedicated linked STA corners1 and native threads1. Actual run:
`.dev/asic-timing-physical/synthesis-runs/20261029T070532999179Z_4821044b`,
ID `4821044b31e44b3a8f7543f8e9ea6cb7`. Run exits0/completed; linked Step and all
three actual native processes complete. Public inspect exits1 because exhaustive
coverage is unavailable, but status is completed and corner coverage complete.
No producer/parser API mismatch occurred in this baseline.

`synthesis-baseline-01.json` passes independent consumer assertions over the
public view and source hashes: configured=requested=executed exactly fast/slow/
typical, no equivalent substitute; five distinct declared/native flops; exact
checked topology inventory; six stored exception relations; twelve endpoints;
seven diagnostic categories with zero returned groups; three nonempty downstream
min and max witnesses each corner; actual standard-cell then I/O library order
and corner hashes. This is completed baseline evidence, **not timing closure**.

| Actual native corner | Worst setup ns | Worst hold ns | Setup violations | Hold violations | Slew/cap violations |
| --- | ---: | ---: | ---: | ---: | --- |
| nom_fast_1p32V_m40C | +16.644657679 | −0.250146660 | 0 | 6 | 0 / 0 |
| nom_typ_1p20V_25C | +16.594198485 | −0.243063021 | 0 | 6 | 0 / 0 |
| nom_slow_1p08V_125C | +16.499676759 | −0.234721582 | 0 | 3 | 0 / 0 |

These are provider-interpreted whole-corner process/log/State metrics, not sampled
interstage slack. The three interstage witness paths retain the earlier direct-
path attribution (−0.109076 / −0.044244 / +0.057878 ns fast/typical/slow). Whole-
corner minimum includes other timed I/O paths and correctly remains failed even
where slow interstage hold passes. Ideal-clock network0 and uncertainty0.25 ns
are preserved. All timing/log/State/native/library sources and raw failures stay
in the actual run. Full attempts remain **0/2**; no P&R was launched.

The native whole-corner `min.rpt` identifies the actual worst path as synchronous
`ui_in[1]`→`control_first/D` (`_03_/D`), with zero minimum external input delay:

| Corner | Data arrival ns | Launch/capture network | Uncertainty ns | Library hold ns | Required ns |
| --- | ---: | --- | ---: | ---: | ---: |
| fast | 0.000670 | ideal0 / ideal0 | 0.250000 | +0.000817 | 0.250817 |
| typical | 0.000938 | ideal0 / ideal0 | 0.250000 | −0.005999 | 0.244001 |
| slow | 0.001436 | ideal0 / ideal0 | 0.250000 | −0.013842 | 0.236158 |

Native rounded reports are retained alongside full-precision provider metrics.
This is an ordinary timed synchronous input, **not** the waived asynchronous
capture input. The output-gate input→output paths also violate early hold. The
0.25 ns uncertainty dominates these direct paths and is not reduced or waived.

### Actual captured production model adapter / Icarus acceptance

`model-adapter-01` passed using generation `875e76c936d14c49817afce1ddb41342`.
Actual `--version --json` advertises
`timing_intent_physical2.functional_postcheck=cmos5l_physical_timing_used_cells_v1`.
The native diagnostic calls **that captured installed helper's
`reviewed_timing_cell`**, the same cell-body adaptation used by production
`replay_models`. C adds no local functional rewrite. All16 qualified supplied
cell module bodies were accepted and hashed. Vendor/UDP source hashes match the
fresh synthesis preflight; unchanged complete source copies are retained.

Actual Icarus compiles/replays passed for the fresh synthesis netlist and three
disposable five-flop master-substitution controls, covering
`sg13cmos5l_dfrbpq_{1,2}` and `sg13cmos5l_dfrbp_{1,2}`. Each positive runs512
observations with exit0; each `+negative` exits1 at the intended observation20.
Every compile/replay uses one-CPU host affinity and one native worker, serialized
with all C builds/EDA. The unchanged testbench, actual mapped input, captured
helper, vendor/UDP, model view, selected module hashes, diagnostics and executables
are hash-bound in per-command receipts and `adapter-inventory.json`.

This is **actual production-adapter/zero-delay digital simulator qualification**,
not a completed ordinary postcheck or final-netlist acceptance. C deliberately
does not fabricate a Hardening manifest, a final-netlist path or native post-PNR
evidence to bypass production admission. Used-cell/full-profile artifact closure
and normal TT/final-netlist checks still require the eventual ordinary full run.
The raw vendor-model failure `testbench-01` is retained unchanged; passing adapted
controls do not relabel that earlier failure or claim vendor timing/SDF conformance.

### Synthesis public evidence and portable replay

`synthesis-public-01` first passed inspect/collect/report parity but its archive
launch failed because C's receipt directory `archive/` collided with its requested
archive destination. This was a **consumer harness path bug**, not a native or
provider mismatch. Raw failed logs remain intact. C changed its output destination
to the separate fresh `archive-output/`; no source or bundle was patched.

The diagnosed non-EDA rerun `synthesis-public-02` passed public inspect, collect,
report, archive-list and archive publication. Report's timing-intent view equals
the independent public inspection, retaining all negative hold goals. Stored
implementation sources remain unchanged apart from the allowed collection cache.
`synthesis-restore-01` restored **241 files** and passed exact public
inspect/collect/report parity inside a read-only child namespace with the original
example/PDK and ASIC source paths hidden. No current PDK/renderer lookup is needed
for this historical read. Archive and restored bytes remain unchanged.

`synthesis-baseline-limits-01.json` additionally verifies actual implementation
jobs6, OpenROAD6, KLayout DRC/XOR6, STA_THREADS1, linked STA threads/workers1, and
successful owned-container cleanup. `preservation-after-synthesis-01.json`:
**16,377 preserved files/selectors, zero failures**. No actual producer/parser API
mismatch was encountered. At that checkpoint full/P&R remained held for F1–F6
and attempts remained0/2.

## Full attempt1 authorization and prelaunch admission

Coordinator explicitly authorized the first ordinary public coarse full launch
after B's205 tests and the unchanged independent38-observation reproducer passed.
C read the final current-authority handoff before capture. `capture-full-01`
captured generation `4856e6af993642988c18c07f47a8c689`, snapshot
`4a821a382619f33eda6be911cb1bddc9d71345a882e97c5fb5b5de68979153a3`.
Locked build `build-full-01` and explicit Hardening emission `full-emit-01` passed.

`full-admission-01` checks actual advertised
`source_closure=extracted_state_views_retained_filter_v2` and
`functional_postcheck=cmos5l_physical_timing_used_cells_v1`, workers6 and dedicated
all-corner STA1 (actual repeated mid-PNR OpenROAD6 is disclosed below).
Hardening RTL, complete emitted SDC and native coverage producer are **byte-identical**
to the emission used in the198 controls; timing intent and qualification marker
are also identical. The198 controls are not repeated. Architecture, reset/latency,
clock/IO/uncertainty/loads/derates remain unchanged. Corrected-reader replay of the
original synthesis baseline completed and truthfully retains failed hold.

The next invocation is **full attempt1 of2**, ordinary public `run --stage full`,
with container CPUs6, flow jobs6, OpenROAD6, KLayout DRC/XOR6, serialized dedicated
all-corner/linked STA corners1 and native threads1, outer3600-second TERM deadline
plus60-second kill grace and
owned cleanup. A second full attempt is not launched without diagnosis communicated
and coordinator plan note. No emitted-bundle patch or source workaround is allowed.

## Actual full result and historical archive closure finding (resolved below)

`full-run-01` exited0/completed after **1477.77 seconds**, ordinary Classic through
routing, RCX, original STAPostPNR and linked extracted analysis. Actual run:
`.dev/asic-timing-physical/full-runs/20261029T075052976305Z_23a6954b`, ID
`23a6954b852d4205b542d3815634d772`, build
`ac513e0e7e9cfa935f73d697caebca8f601aeeb4ea62c2a2ccf61c10a10789cd`.
`full-inspect-01` returns completed/post-PNR with all-corner timing **pass**.
`full-postcheck-01` completed normal public TT and final-netlist Icarus checks,
both **pass**, check `bc95939552ae415c9a5aaa8c1fff1cfe`. `full-public-01` passed
inspect/collect/report parity and archive publication; public report exits0.
This is actual native completion, not a wrapper-only or modeled result.

### Archive replay omission — precise remaining producer closure finding

Archive:
`.dev/asic-timing-physical/evidence/full-public-01/archive-output/`.
`full-restore-01` initially exposed a C restoration omission: public archives keep
`postcheck.json` as a loose record rather than a tar member. C corrected only its
restoration consumer to copy those **exact archived bytes** back to the unique
archived `checks/<id>/postcheck.json`; the failed restoration is retained. No run,
emitted bundle or archive bytes were altered.

The diagnosed `full-restore-02` now reproduces timing inspection and the complete
postcheck record, but public collect has **416 raw artifacts instead of423**.
`full-restore-02-artifact-differences.json` shows the **only** response difference:

```text
project/runs/asic/40-openroad-checkantennas/reports/antenna.rpt
project/runs/asic/40-openroad-checkantennas/reports/antenna_summary.rpt
project/runs/asic/46-openroad-checkantennas-1/reports/antenna.rpt
project/runs/asic/46-openroad-checkantennas-1/reports/antenna_summary.rpt
project/runs/asic/62-magic-drc/reports/drc.magic.rpt
project/runs/asic/66-netgen-lvs/reports/lvs.netgen.json
project/runs/asic/66-netgen-lvs/reports/lvs.netgen.rpt
```

All seven exist in the original actual run and are advertised by public collection,
but are absent from `archive.json.members` / reports tar. Retained source review
of `execution/archive/archive_service.ml:138–173` shows the macro-only
`physical_files` branch does not apply to this macro-free timing profile; ordinary
fallback candidates include synthesis and post-PNR timing, not these intermediate
physical report directories. B needs to include these advertised ordinary physical
report bytes in the macro-free full archive closure. Do not normalize the missing
artifact list away, copy directly from the live run into a purported restored
archive, or rerun P&R. A source-corrected archive publication from this immutable
actual run followed by fresh hidden-input replay is sufficient to verify the fix.

Raw original/restored public responses and per-command hashes remain under
`evidence/full-public-01/`, `evidence/full-restore-01/`, and
`evidence/full-restore-02/`. Native timing replay itself passes in the hidden-input
namespace. The failed complete collect-parity assertion is retained truthfully;
full source-replay acceptance is not declared complete. **One full attempt used;
no second full attempt has been launched.**

### Full native/public assertions and unchanged architecture

`full-native-public-acceptance-01.json` passes C's independent assertions over
actual provider views and all advertised source hashes. Three corners actually
execute; no equivalent substitute is credited. Each is audit3/post-PNR, has
propagated primary clk, exact retained consumed SPEF, successful single-thread
native process, five distinct original `sg13cmos5l_dfrbpq_1` stages and exact native
sequential inventory, six stored exception relations and seven empty diagnostic
categories. CTS adds one **combinational clock-load endpoint** `clkload0/Y`
(`sg13cmos5l_inv_1`, unused output), so the truthful final native inventory has
**13 endpoints**, versus12 in synthesis. C's first full assertion inherited the
synthesis-only12 expectation; it was corrected to check all ten stage data/reset
pins, both output endpoints and that exact CTS load. No producer data was changed
and no extra architectural register was added.

| Actual extracted corner | Worst setup ns | Worst hold ns | Setup/hold violations | Slew/cap violations | Filtered annotation |
| --- | ---: | ---: | --- | --- | --- |
| nom_fast_1p32V_m40C | +16.058594908 | +0.102353212 | 0 / 0 | 0 / 0 | pass |
| nom_typ_1p20V_25C | +15.729073600 | +0.276686071 | 0 / 0 | 0 / 0 | pass |
| nom_slow_1p08V_125C | +15.113663637 | +0.590927102 | 0 / 0 | 0 / 0 | pass |

The original producer is `55-openroad-stapostpnr/state_in.json`; linked input
State equals it exactly and the physical chain retains placement28, CTS35,
detailed-routing44 and RCX54. **CTS35 is the pre-repair checkpoint**. The actual
ordinary `37-openroad-resizertimingpostcts` log reports six hold-violating endpoints,
then **nine inserted hold buffers** with no setup violations. Native final
`53-odb-cellfrequencytables/cell.rpt` records: five original `_dfrbpq_1`, nine
`_dlygate4sd3_1`, six `_buf_1`, three `_buf_8`, one clock-load `_inv_1`, two `_and2_1`
and22 tie cells (plus physical filler/decap cells). Original synthesis has the same
five flops, two AND2, two BUF1 and22 ties; zero memory. These original raw stage
logs, reports and before/after views remain in the immutable full run.

The checked endpoint traces enumerate nine unique transformations across the
declared timing roles (three clock BUF8, four interstage delay cells, and two
input BUF1); maximum checked path depth is2, below the qualified eight-hop bound.
This trace subset is not claimed as the total chip delay-cell count: the native
whole-design cell report has nine delay cells. No cloning/merging/state/latency/
reset change or uncertainty reduction was used. The ordinary first full run's
supported repair closes hold; a separate repair rerun was unnecessary.

### Extracted data/clock contributions (native first interstage hold witness)

All quantities ns, directly quoted from each retained `downstream_min.rpt` for
capture_first→capture_second. Clock propagation and extracted net delays are
actually active; uncertainty remains0.25 and derates0.95/1.05. Native increments
include the library/load/net treatment in that report; they are not invented
cell-only versus wire-only decompositions.

| Corner | Launch CLK arrival | Capture CLK arrival | Clock→Q increment | Increment through hold29/X | Final D net increment | Data arrival | Uncertainty | CRPR | Library hold | Required | Slack |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fast | 0.088903 | 0.101238 | 0.101213 | 0.232137 | 0.000151 | 0.422404 | 0.250000 | −0.007107 | −0.024080 | 0.320051 | +0.102353 |
| typical | 0.129149 | 0.146974 | 0.150138 | 0.345112 | 0.000144 | 0.624542 | 0.250000 | −0.010061 | −0.039057 | 0.347856 | +0.276686 |
| slow | 0.204894 | 0.232585 | 0.239965 | 0.553051 | 0.000138 | 0.998047 | 0.250000 | −0.015374 | −0.060090 | 0.407120 | +0.590927 |

All three downstream min and max witnesses are nonempty and MET in every corner.
The original synthesis and earlier controls remain negative where reported; the
physical improvement is linked to real propagated clocks/extracted implementation
and qualified added delay, not waived downstream checks. Annotation explicitly
uses the native ODB connected-net filter scope: e.g. fast raw unannotated count15,
filtered count0. The pass is **not** a claim that every raw reported driver is
annotated; original raw reports, checks.rpt, filter inputs/process/script and
filtered metrics are retained and source-checked by the corrected reader.

### Ordinary physical/external gates

Public collection reports antenna nets/pins0, routing/Magic DRC0 and LVS errors0.
Normal TT precheck reports all nine checks pass, including actual CMOS5L KLayout
DRC, pin/boundary/layer/cell-name/analog-pin gates. Normal final mapped-netlist
Icarus replay prints `checks=512` and passes. Production replay-model profile2
pins vendor/UDP/used-module/helper/view hashes; final simulation netlist hash equals
the exact netlist consumed by extracted timing. There is no SRAM waiver or
SRAM-specific physical policy in this macro-free run. These assertions pass;
remaining completion blocker is the seven-file public archive closure above.

`full-restore-report-01` completes all three diagnostic reader calls rather than
stopping at the first parity difference. Its immutable summary records457 restored
files, `inspect:true`, `collect:false`, `report:false`, with archive/restored bytes
unchanged and original source/PDK hidden. The restored public report itself exits0;
its **only** difference from the original report is the same seven missing raw
artifact entries (`full-restore-report-01-differences.json`). This does not repair
or normalize the archive: strict full-response parity remains failed. The issue
is retained physical report closure, not a failed native timing run or TT check.

`preservation-after-full-01.json` verifies all16,377 original files/selectors,
zero failures. Actual full inputs and postcheck artifact hashes passed C assertions.
No second full run, emitted-file patch, PDK edit, protected-provider/config change,
SRAM rerun or Git mutation was performed.

## Portable closeout complete — corrected archiver, same actual execution

Coordinator authorized B's archive-only correction and explicitly disposed the
thread-label discrepancy without repeat physical execution. Before live doc
corrections C snapshotted the three C documentation files byte-for-byte, all1196
actual run files, the original public evidence/archive, execution-provider receipt
and run-record hashes in `evidence/portable-before-01/snapshot.json`. Prior capture,
archive and failed restoration attempts remain intact. No actual run record was
changed or attributed to a later execution provider.

`capture-archive-01` created a new isolated reader/archiver generation
`1ba205c2a11c4904b03d98b0e7a3f616`, captured-source snapshot
`454be3f35b6183bf5142913e224b5e5665d186a1fa251efbb8e3e31c2eef8512`.
The installed captured `archive_service.ml` is exactly
`4c86b6516f31b0c1c18a07364ab85b7c38a9122633debec2cafeac93befb415d`.
This is the **archive reader/producer identity**, not the physical execution
identity. Original execution remains generation `4856e6af993642988c18c07f47a8c689`,
snapshot `4a821a382619f33eda6be911cb1bddc9d71345a882e97c5fb5b5de68979153a3`.
The new capture uses switch5.2.0+ox, shared ASIC lock and nested-j6. No EDA,
preflight, synthesis, postcheck or full flow is rerun.

New public archive:
`evidence/full-public-corrected-01/archive-output/`. Its exact identities and both
provider receipts are bound in `identity-binding.json`. The authoritative report
inventory is `librelane-native-direct-reports-v1`, with all seven formerly omitted
reports and their producer/config/State/runtime metadata. It has449 tar members;
that is distinct from the423 publicly advertised raw-artifact entries.

| Corrected archive file | SHA256 |
| --- | --- |
| reports.tar.gz | `8f2bff91bb171b95f24d05142009619693ac80aa5ce358c4d5a66ba762b4e366` |
| input-bundle.tar.gz | `ab91f86aaf778631cb4533b10199c1cb4baab529173d5f0d04e7875915a0759d` |

`full-restore-corrected-01` restores476 files using only the new archive and loose
records/input bundle. The original example/full-run/PDK and ASIC source are hidden
in the read-only child namespace. Public inspection, collection and report match
the **original execution responses exactly**, including all423 raw artifacts and
the complete normal postcheck/model record. No response normalization or live-run
copy fills the restore. Inspection retains unavailable exhaustive coverage; normal
collection/report exit0. Archive and restored bytes remain unchanged.

`portable-verification-01.json` additionally checks every449 archive member and
every423 advertised source byte against the pre-republication original-run hashes,
all emitted input-bundle members, exact original run-record bytes, and all1196
run files unchanged. It records A's1720-assertion actual review and direct native
command evidence for the corrected thread accounting:

| Actual native occurrence | Requested native threads |
| --- | ---: |
| Dedicated STAPrePNR12, three cell corners | 1 each |
| Dedicated STAPostPNR55, three cell corners | 1 each |
| Linked extracted STA, three cell corners | 1 each |
| Mid-PNR OpenROAD31 | 1 |
| Repeated mid-PNR OpenROAD36/38/43 | 6 each |

The six-thread requests are in original retained `COMMANDS` and native process
records; they are not relabelled as one-thread execution. The original all-STA1
description was overbroad. All actual requests stayed within C's allocation6.
Coordinator accepts corrected disclosure, with any future implementation adjustment
owned by B. This disposition does not change the actual commands or require new
physical execution. Three distinct cell-PVT corners use one nominal extracted RC
view (`nom_*`); no claim of three distinct RC extraction corners is made.
