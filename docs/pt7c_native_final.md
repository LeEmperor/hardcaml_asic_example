# PT7c final-candidate native acceptance

**Historical native-v1 candidate.** This run remains completed and readable by its
retained historical provider. Current reviewed readers explicitly reject its
native-v1 profile as unsupported and require fresh capture; it has not been
relabelled as a failed original run. See [native-v2 final acceptance](pt7c_native_v2_final.md)
for the fresh reviewed producer/profile2 run and preservation verification.

2026-10-28. **Fresh ordinary coarse synthesis and automatic separate linked
LibreLane STAPrePNR completed. Public retained-source archive/restore and native
scope/diagnostic/witness controls passed.** Overall exhaustive exception-effect
coverage remains **unavailable**, and the negative hold witnesses remain
**violations**. Independent A/B review is separate from this C native acceptance.

## Exact candidate and provenance

| Item | Identity |
| --- | --- |
| Isolated final generation | `.dev/asic-pt7c/provider/generations/df6eaa70174c44d280bcb9c724917121` |
| Observed provider base | `1a8798a33a2f02a6018ee9854591f100efdd10bb` |
| Captured provider source SHA-256 | `80057ede2666414820ba97cd39d1475200cf7ced89a99c79df487d4abfe90caf` |
| Provider receipt SHA-256 | `7785d3985827a92384c9dca9dfd01cb85aa13db5355cb32f3931f2cace0b74f5` |
| Build identity | `9a591920cf3c6697f8189500dbb55cf7c9ce4e53c210b31b5f85b2ae907367d7` |
| Run ID | `48ac4fc8a4cf4d51838a771f896a804e` |
| Manifest SHA-256 | `40b1c6056b67806bb1373ea629226f6740c547eb340eba1b8b33fdbe16bf7ebf` |
| Inner schema2 audit SHA-256 | `3d8464cb68e809b3ea07f8fde3cd4f78ca3d2594290b35dd68404d5b6d07d823` |
| Exact emitted SDC SHA-256 | `7d66fe0de02bd45b4c214585719e39d8dab253a7e5cecc5342090c170bb1a128` |
| Mapped Verilog SHA-256 | `1fa6fc0404ac31a5c435d9fc2f4b33dbe95749d53618c3a14c5455ea414876e1` |
| Retained producer SHA-256 | `3bba1e69eddb5f57a8ce8608fcf3dd1e9b86b1ea99efa6d4b5faa551cb9412e3` |
| Native stored SDC SHA-256 | `5246923433cd2051b6ddba578cba771d513b6e38db370aad9092b2ca941bbe92` |

Run root:
`.dev/asic-pt7c/runs/20261028T173519344419Z_48ac4fc8`.
The exact immutable source bundle is `.dev/asic-pt7c/bundle-emit-01`.
Capture receipts identify local development bytes; they are not authenticated
execution, clean-checkout or P6 source-stamp claims.

The actual runtime is LibreLane **3.1.0.dev3**, exact local image
`sha256:d109140b8f17fc54f4fca998beb8124f4949404ec52e339eebd2250854a18b5a`.
Native `OpenROAD.STAPrePNR` uses **OpenSTA 2.7.0** internally. The effective
analysis requests/executes only `nom_typ_1p20V_25C`; original configured fast,
slow and typical corners are retained separately in the explicit delta. This
is typical-only evidence, not all-corner evidence or an OpenROAD P&R run.

Two actual loaded libraries are retained: stdcell SHA-256
`34163f3e7de9f854afac57332ba06f1739b78e7ac35660a8a5ddd39c570124ad`
and IO SHA-256
`e6b5adf1ce31db3a0c15e5ca069c62e7d9efb604a710b8f6582700f1721d2d98`.
`verified-final-01/summary.json` binds these, all 65 companion sources, 20 inner
audit sources, effective config/delta, native process/version, runtime binding,
synthesis config/state/netlist and the complete run inventory. The native SDC
and producer inputs equal the unmodified emitted members byte-for-byte. Every
emitted bundle member and current declared source-input hash was also verified.

## Actual ordinary flow and public replay

The commands in `capture-01`, `build-01`, `emit-01` and `coarse-01` completed.
The public ordinary command was `hardcaml-asic-flow run BUNDLE --stage synthesis`.
It stopped the synthesis recipe at **Yosys.Synthesis**, then automatically ran
the provider's genuine Step API linked analysis in separate `timing-intent/`.
No source overrides, re-elaboration, replacement synthesis state, named execution
or P&R endpoint was used.

`public-02/` retains actual public CLI attempts:

| Operation | Exit | Observed result |
| --- | ---: | --- |
| coarse timing-intent-inspect | 1 | completed evidence, verdict unavailable |
| collect --stdout --json | 0 | native evidence included |
| report --json | 0 | synthesis acceptance; native exhaustive coverage unavailable |
| archive --list | 0 | complete advertised source selection |
| archive --output | 0 | `archive-output/` with reports and complete input bundle |
| restored inspect | 1 | exact same interpreted evidence |
| restored collect/report | 0/0 | exact same JSON as original collection |

The report's exit zero is ordinary synthesis acceptance, **not** a native
timing-closure verdict. `standalone-final-01/` separately executes public schema2
inner-audit inspection, exit 1, exactly matching the coarse envelope's inner view.

Both archives were extracted into a new `public-02/restored/`; archived records
and retained bundle contents reconstruct its project. `sandbox-replay-01/`
then ran the actual installed public inspect/collect/report inside a private
bubblewrap namespace with the **original example root (including PDK, original
run and source bundle) and provider source checkout hidden**. Only the frozen
installed generation and restored evidence were rebound read-only. All three
JSON results match the original. Host sources were never renamed or changed.
`public-02/read-only-verification.json` confirms all **199 original run files**
remained unchanged during public inspection, collection, reporting and archiving.

Three independent new restored-run corruptions—changed native source, missing
native source, wrong run association—pass twelve public assertions in
`public-negatives-01/`: inspect/archive reject with exit 2; collect returns its
explicit timing error; report returns exit 1. Each assertion checks the intended
source/association diagnostic, not merely an arbitrary failure.

## Native stored scope, diagnostics and preserved downstream timing

All five preserved cells are `sg13cmos5l_dfrbpq_1`:
capture first/second/third = `_06_`/`_05_`/`_04_`; control first/second =
`_03_`/`_02_`. Native resolution validates the Q anchors, chain connections,
clock and reset connectivity before any applied record. The six exact stored
relations match the validated request: solely `ena -> _06_/D`, and `rst_n` to
the five enumerated RESET_B pins, unrestricted min/max and both transitions.

Baseline native diagnostics explicitly retain all seven categories, each with
zero returned groups. The bounded complete native endpoint inventory has **12**
pins: five D, five RESET_B and two driven output ports. Empty algorithm groups
do not establish exhaustive path coverage. Raw native check and endpoint reports
are cross-checked by the generic reader against all structured groups/details.

| Exact downstream relation | Setup/max slack (ns) | Hold/min slack (ns) |
| --- | ---: | ---: |
| `_06_/Q -> _05_/D` | +19.432287 | **−0.044244** |
| `_05_/Q -> _04_/D` | +19.432287 | **−0.044244** |
| `_03_/Q -> _02_/D` | +19.432287 | **−0.044244** |

All three setup and hold witnesses are retained. Negative hold was not suppressed,
repaired, downgraded or relabelled as timing closure.

## Real native counterfactuals and generic reader acceptance

`controls-final-01-*` are **eleven separately labelled real native attempts**,
using the exact completed coarse netlist and both retained libraries mounted
read-only, plus the unchanged emitted native producer. Each control reads a NEW
diagnostic copy of native-written state. The baseline bundle and baseline run
are never edited. Native launch receipts retain exact input hashes before/after,
argv, process results, limits and complete reports. All eleven native executions
complete both producer and enclosing-control markers.

* Baseline: external `ena -> _06_/D` has no returned min/max witness.
* Remove its exception: both exact external min/max witnesses return.
* Setup-only: min returns, max remains suppressed.
* Hold-only: max returns, min remains suppressed.
* Rise-only, broad, extra relation and CLK→Q masking: native state retained;
  the generic provider rejects the unsupported/restricted/mismatched scopes.
* Omit input delays: 18 native missing-input details plus two unconstrained D
  endpoint details. Omit output delays: two native missing-output details.
* Omit clock and clock-associated delays: five native unclocked CLK details
  and seven unconstrained endpoints. All seven explicit categories remain present.

`native-final-02/` passes **four positives and twelve intended rejections** through
`Hardcaml_asic_execution.Timing_native_coverage.inspect`. Seven native scope/
masking negatives reject for the expected relation/restriction/command diagnostic;
five retained-wire controls reject missing category, incomplete wire, endpoint
count mismatch, raw-report mismatch and truncation. The adapter contains no
consumer-local timing parser or producer. `native-final-01` remains the first
passing iteration; 02 adds explicit intended-diagnostic assertions.

These observations establish **bounded external witness suppression only**.
Exhaustive exception effects, per-check timing analysis, reset-effect adequacy,
analog CDC/MTBF, reset-release protocol, post-PNR preservation and timing closure
remain unavailable/not established.

## Preservation, failures and resource receipts

The original preliminary provider remains separate in `probe-provider/`.
The failed reader and failed linked run `44ded577c4524024a041c6397bf8f93f` remain
failures. All **30 original failed companion source hashes** still match, and
the native process exit remains 1. Its wrapper/error/SDC were not patched.
A's real continuation/derate/current-design and B's rerouted-environment startup
findings are closed only for the fresh corrected candidate above.

`public-01` retains a C launcher mistake: its command receipt directory occupied
the archive destination. The provider correctly refused it. C changed the new
launcher destination to `archive-output` and reran as new attempt `public-02`.
No failed attempt was overwritten.

`closeout-final-01/` retains final installed binary/archive and compiled emitter/
adapter hashes, the preliminary installed generation inventory, A/B handoff
snapshots, original-history verification and full new-evidence checksums.
The original-history baseline protects **10,398 files**, including all prior r3
acceptance history, with zero changes. New example changes are isolated PT7c
scripts/docs/acceptance/build outputs; hardware, old provider selections, app
configuration, old untracked artifacts and old acceptance evidence remain intact.

All Dune/nested capture calls used `5.2.0+ox`, explicit `-j6` or lower and the
designated ASIC/example locks. Builds and EDA were sequential within six workers.
Ordinary synthesis uses Docker six CPUs, `--jobs 6`, explicit worker environment
and `STA_THREADS=1`. Separate analysis has six-CPU quota, `STA_THREADS=1`,
`OPENROAD_THREADS=1` and native `sta -threads 1`; corner execution is serialized.
Counterfactual tools use one CPU/thread, one-worker environment, read-only image,
memory/PID/time bounds and the native STA lock. **P&R allocation/use is zero.**
No Git mutation, Workbench/Protemu, daemon, pin or old provider/config edit was
performed by C. No remaining C native acceptance blocker is known for this
captured candidate; concurrent independent review is not claimed complete here.
