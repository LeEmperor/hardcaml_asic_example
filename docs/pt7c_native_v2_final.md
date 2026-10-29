# PT7c reviewed native-v2 final acceptance

**Final inspection update:** the [reader-only R1b correction](pt7c_reader_r1b_final.md)
qualifies strict LF-only native SDC inspection against these exact retained
sources. The original native execution below remains attributed to generation
`4d4316e3a33942c2a577d6f55acaa34a`; the corrected reader has a separate capture and
receipt. No producer, runtime, profile, bundle or native evidence was changed.

2026-10-28. **Fresh public ordinary coarse synthesis and automatic separate linked
STAPrePNR completed against the reviewed A/B provider. Native profile2, mandatory
verified top, category-framed diagnostics, stricter source/transport binding, and
public archive/restore with original sources hidden pass bounded C acceptance.**
No remaining C execution blocker was observed. Exhaustive exception effects and
reset-effect adequacy remain unavailable; negative hold remains a violation.

## Exact candidate

| Item | Identity / SHA-256 |
| --- | --- |
| Installed generation | `.dev/asic-pt7c/provider/generations/4d4316e3a33942c2a577d6f55acaa34a` |
| Observed provider base | `1a8798a33a2f02a6018ee9854591f100efdd10bb` |
| Captured development source | `8d3fa9270712a47473c22615c2a7005d975b361db5f569dfbe8e911055ccbe89` |
| Provider receipt | `ec00d5619805de324201a23446a0dd5129eb2a8ef02713ed87bd5e1299809310` |
| New emitted build identity | `9d01f5c006c697dd103762c04038fd73e8322d3b546f2bf56dfcad0de19cc8c6` |
| Run ID | `83a02bdcb4b34f22bbc03b0ec5223b41` |
| Manifest | `225941cc67b4e2ff695c3350287b56839fa5bbfe13ce83330178ce57a91a6d1d` |
| Outer schema2 native audit | `3601a22810b532ae0c3495b96dc00b214480ce5d333fcb6f1c12d4d99ac06884` |
| New emitted native-v2 producer | `8d886b2bde7e50f7781ef7f3f73bfdfa47a8d7beba947119dd66129a2d48b03e` |
| Native-data schema2 bytes | `a1535be06542033176d28e2465abf0b4bf01223f9d0e541550cc2c42e204e9ec` |
| Unmodified emitted SDC | `7d66fe0de02bd45b4c214585719e39d8dab253a7e5cecc5342090c170bb1a128` |
| Fresh synthesis mapped netlist | `1fa6fc0404ac31a5c435d9fc2f4b33dbe95749d53618c3a14c5455ea414876e1` |
| Native-written constraint state | `5246923433cd2051b6ddba578cba771d513b6e38db370aad9092b2ca941bbe92` |

New run:
`.dev/asic-pt7c/runs/20261028T183412758171Z_83a02bdc`.
New unmodified source bundle: `.dev/asic-pt7c/bundle-emit-v2-01`.
The identical SDC/netlist/state hashes relative to v1 reflect deterministic fresh
production; the actual new synthesis/process receipts and new producer/build
identity are retained. No old run, bundle or report was patched or substituted.
Capture is a local development-byte receipt, not authenticated execution or a
clean-checkout/P6 source-stamp claim.

Actual runtime: LibreLane **3.1.0.dev3**, OpenSTA **2.7.0** through the genuine
`OpenROAD.STAPrePNR` Step API, exact image
`sha256:d109140b8f17fc54f4fca998beb8124f4949404ec52e339eebd2250854a18b5a`.
Only `nom_typ_1p20V_25C` was requested/executed for linked analysis. The original
configured fast/slow/typical corners and explicit typical-only delta remain
separate retained facts; this does not establish all-corner evidence.

## Actual flow, source binding and native-v2 dimensions

Completed receipts: `capture-v2-01`, `build-v2-01`, `emit-v2-01`, `coarse-v2-01`.
The ordinary CLI stopped synthesis at `Yosys.Synthesis`, then ran its automatic
supplementary STA in a separate directory. The unchanged emitted SDC was loaded
once, with one receipt before resolution, one resolution/application block,
`HC_ASIC_NATIVE_V2_COMPLETE`, and enclosing `PT7_AUDIT_COMPLETE` in order.

The wrapper now executes the **retained** corner script. `native-inputs.json`
binds that copy/hash, actual ordered Liberty paths and retained library references;
the runtime binds all executed driver/hook/native pointers to its recorded
historical execution root. The verifier checks qualified transport argv, resource
limits, terminal truth, synthesis state/netlist association and source closure.
The two actually loaded libraries retain hashes
`34163f3e7de9f854afac57332ba06f1739b78e7ac35660a8a5ddd39c570124ad`
and `e6b5adf1ce31db3a0c15e5ca069c62e7d9efb604a710b8f6582700f1721d2d98`.
All emitted members, declared current source inputs, companion/audit sources and
original failed companion sources were independently rehashed by
`verified-v2-01/summary.json` and `run-files.json`.

The profile is **opensta-2.7-native-state-v2**, native-data schema **2**, outer
audit schema **2**. The leading native `current_design tt_um_pt7_timing` matches
the identity-verified manifest top; interpreted `native_design` records it.
Five preserved `sg13cmos5l_dfrbpq_1` cells resolve as capture `_06_/_05_/_04_`
and control `_03_/_02_`. Exact stored scope matches all **six** relations:
`ena -> _06_/D` and `rst_n` to the five enumerated RESET_B pins, both min/max
and unrestricted transitions. Native endpoint inventory contains **12** pins.

All seven baseline diagnostic categories are explicit and empty. Each has its
own raw BEGIN/END markers under the V2 header and completion marker. Structured
messages/details are checked against these category-bound native report bytes;
no English warning text determines category identity. Empty complete groups
mean no findings from the returned algorithm, not exhaustive path coverage.

All three downstream setup witnesses remain **+19.432287 ns** and all three
hold witnesses remain **−0.044244 ns**, for `_06_/Q -> _05_/D`, `_05_/Q -> _04_/D`
and `_03_/Q -> _02_/D`. Hold violations were retained without repair or downgrade.

## Public archive, restore and sandbox replay

`public-v2-01/` executes real public inspect (exit **1**, completed/unavailable),
collect (**0**), report (**0**, ordinary synthesis acceptance), archive list (**0**)
and archive publication (**0**). Both archives were restored to a new root and
public inspect/collect/report replayed the exact same JSON. Inner-audit public
inspection (`standalone-v2-01`) also returns **1** and equals the coarse inner view.
Report success does not establish timing closure or exhaustive native coverage.

`sandbox-replay-v2-01/` repeats installed public inspect/collect/report in a private
bubblewrap namespace with the **original example root, PDK, original run/bundle
and provider source checkout hidden**. Only the frozen installed generation and
restored evidence are rebound read-only. All results equal the original. No host
directory was renamed or altered. Public read/archive protection verified all
**199 original run files** unchanged.

`public-negatives-v2-01/` passes twelve intended public assertions on new copies:
changed native source, missing native source and wrong run association. Inspect/
archive reject, collection reports invalid evidence, and report rejects it.

## Native diagnostic/scope/witness controls

`controls-v2-01-*` comprises **eleven actual single-thread native executions**
using the fresh coarse netlist, both retained libraries and unmodified emitted
V2 producer, with all reference inputs mounted read-only. Only NEW diagnostic
copies of native state are changed. Every attempt retains before/after input
hashes, exact argv, process result, raw/structured reports and completion markers.

* Baseline external capture min/max reports are empty; removing its exception
  exposes both exact witnesses.
* Setup-only exposes min and suppresses max; hold-only exposes max and suppresses
  min. Rise-only is retained as restricted scope, not equivalent full scope.
* Broad capture, extra relation and CLK→Q masking serialize natively but reject
  under the generic reader's intended scope/restriction/unsupported-command rules.
* Removing input delays returns 18 native missing-input detail strings and two
  unconstrained D details; removing output delays returns two missing-output
  details. Omitting the clock and associated delays returns five unclocked CLK
  details and seven unconstrained endpoints. Every case retains all seven
  category identities and independently cross-checked category-framed raw bytes.

`native-v2-01/` passes **four diagnostic positives and twelve intended scope/wire
rejections**, through the installed generic provider and mandatory-top adapter.
The adapter owns no parser, resolver or native producer. These are bounded witness
suppression observations, not exhaustive exception effects or reset-effect proof.

## Review reproductions against actual retained native-v2 output

`review-public-v2-01/` and the targeted downgrade completion
`review-public-v2-02/` cover **nine diagnostic cases / 36 public assertions**:

1. Executed Liberty list points outside its retained associations.
2. Native process driver has the wrong historical root.
3. Executed corner script pointer is not its retained copy.
4. Transport outcome/code is malformed.
5. Duplicate/conflicting CPU quota appears in transport argv.
6. A failed companion contradicts its successful process/cleanup truth.
7. Native top disagrees with the verified manifest top.
8. Continued native-SDC comment hides an exception.
9. Producer declaration/member is removed despite the run's advertised expectation.

These are **resealed diagnostic copies**, not authentic newly executed runs.
Changed inner source references, audit/runtime references and companion hashes
are updated so rejections reach the intended semantic diagnostics. Each case is
exercised through public inspect, collect, report and archive. The downgrade's
report rejects the manifest payload identity with exit **2**, while inspection
and archive reject the missing advertised producer. The first C launcher expected
report exit 1; that expectation failure remains retained. Only this last case was
rerun with the correct expected hard-rejection exit; earlier passing cases were
not broadly replayed. No provider defect was observed in that attempt.

`review-native-v2-01/` adds **nine intended generic-reader rejections**: wrong,
missing, repeated and late top; continued comment; category reassignment with
unchanged raw bytes; reserved-marker injection; legacy-v1 data; undelimited raw
report. Nonempty reassignment uses the actual missing-input native output, not
fabricated English category classification. Independent real `tclsh` inert
language controls return zero false-path calls for the continued comment and one
for the ordinary-comment positive. Inspection never executes retained Tcl.

## Native-v1 preservation and original schema1 compatibility

The successful native-v1 run `48ac4fc8a4cf4d51838a771f896a804e` and its frozen
provider `df6eaa70174c44d280bcb9c724917121` remain intact. `legacy-v2-01/` verifies:

* Current coarse and inner schema2 readers explicitly reject profile1 with a
  recapture/unsupported-legacy diagnostic, exit **2**.
* The retained historical provider still returns completed/unavailable, exit **1**,
  with JSON identical to its original native-v1 successful inspection.
* The original standalone **audit-schema1** r3 scalar history still returns its
  original unavailable-native semantics through the current reader, exit **1**.
* The original native-v1 run record still says **completed**; it is not relabelled
  failed, upgraded to profile2, or granted category-bound V2 coverage.

`v2-history-baseline-01/` was created before continuation edits. It records full
hashes for **3,622 prior evidence/run/installed-generation files**, and snapshots
the prior continuation sources/docs (including the original adapter). Verification
`v2-history-verification-01/` reports **zero changes**. The original broader
10398-file history/protected-input inventory remains separately verified.

## Resource limits and closeout

All builds/nested capture calls used switch `5.2.0+ox`, explicit `-j6` or lower,
and the ASIC/example checkout locks. Builds and EDA were sequential within C's
six-job allocation. Ordinary synthesis and supplementary analysis each have
explicit six-CPU Docker quota and bounded worker argv/environment. STA has
`STA_THREADS=1`, `OPENROAD_THREADS=1` and native `sta -threads 1`; native controls
use serialized one-CPU/one-thread launches with memory/PID/time bounds.
**P&R allocation/use is zero.** No extra broad suites were replayed.

`closeout-native-v2-01/` retains all new-evidence/source checksums, frozen installed
binary/archive and compiled adapter/emitter hashes, preliminary generation hashes,
A/B final handoffs/reviews, and original-history verification. The historical
native-v1 closeout and all initial failures remain untouched. No Git mutation,
ASIC implementation, Workbench/Protemu, daemon, pin, old application config or old
provider selection was changed by C; only the isolated PT7c provider pointer was
refreshed for the requested capture.

Coverage remains **unavailable** for exhaustive exception effects, per-check timing
analysis, reset/CDC protocol adequacy, analog MTBF and post-PNR behavior. Native
stored scope/category-bound diagnostics are supported dimensions; timing closure
is **not established** because negative hold remains visible.
