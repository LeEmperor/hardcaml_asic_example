# PT7c native findings (C, live handoff)

**R1b final reader closure:** see [corrected LF-only inspector qualification](pt7c_reader_r1b_final.md).
Exact CR bytes in newly resealed audit copies reject semantically, while the
original/restored native-v2 results replay identically. This is reader-only
qualification, not another native execution or attribution change.

**Reviewed native-v2 closeout:** fresh coarse/STA, mandatory top and category-framed
raw diagnostics passed. Public review reproductions reject on the intended binding/
grammar diagnostics. Original native-v1 success is preserved as historical success,
explicitly unsupported by current readers. See [native-v2 final acceptance](pt7c_native_v2_final.md).

**Closeout:** the A continuation/derate/current-design and B environment-bootstrap
findings below are closed by fresh native execution of the corrected captured
provider. Full results: [PT7c final acceptance](pt7c_native_final.md). Earlier
failures remain retained under their original attempt identities.

2026-10-28. Actual standalone OpenSTA **2.7.0**, exact local image
`sha256:d109140b8f17fc54f4fca998beb8124f4949404ec52e339eebd2250854a18b5a`.
New evidence: `acceptance/pt7c/native-api-02/`; immutable r3 scalar SDC,
mapped netlist and Liberty mounted **read-only** as `/old`. Docker one CPU,
`sta -threads 1`, worker environment all one, serialized STA lock, 180s bound.
Before/after hashes and exact argv are in `receipt.json`.

## Concrete API / grammar for A and B

* Version is `sta::version`, **not** `sta::sta_version`. Attempt 01 retains
  that failed call. OpenSTA returned process exit zero despite a Tcl failure
  diagnostic: process success alone must never establish producer completion.
* `sta::check_timing_cmd` takes **exactly seven booleans**, in this order:
  `no_input_delay no_output_delay reg_multiple_clks reg_no_clks
  unconstrained_endpoints loops generated_clks`.
  `sta::check_timing_cmd 1 1 1 1 1 1 1` returns the empty Tcl list for the
  fully constrained r3 baseline; all-zero also returns empty. Empty results
  do not encode category names; producer must explicitly record the seven
  requested/completed categories. Arity diagnostics are retained verbatim.
* `sta::endpoints` takes zero arguments and returns native Pin handles.
  `get_full_name $pin` works. Baseline returns **12** endpoints: two
  `uo_out[0/1]`, five D pins and five RESET_B pins. These are not an
  unconstrained-endpoint count. Raw handles are process-local, not identities.
* `write_sdc [-digits N] [-significant_digits ...] [-map_hpins] [-compatible]
  [-gzip] [-no_timestamp] FILENAME`. Native default, digits default 4.
  Use `-no_timestamp` for deterministic state bytes. Tcl body retained.
* Actual native false-path grammar has backslash-newline continuation:

  ```tcl
  set_false_path\
      -from [get_ports {ena}]\
      -to [get_pins {_4_/D}]
  set_false_path\
      -from [get_ports {rst_n}]\
      -to [list [get_pins {_2_/RESET_B}]\
             [get_pins {_3_/RESET_B}]\
             [get_pins {_4_/RESET_B}]\
             [get_pins {_5_/RESET_B}]\
             [get_pins {_6_/RESET_B}]]
  ```

* Reset target order is native sorted, different from requested stage order.
  Native writer emits scalar get_pins for singleton and nested `[list ...]`
  for multiple objects; parser must handle both without evaluating Tcl.
* Ordinary state also includes `current_design`, clock/transition/uncertainty,
  input/output delay (`-min/-max -add_delay`), driving cell, load, timing
  derate and max fanout. Full `native.sdc` retained, including bus braces
  (`[get_ports {ui_in[0]}]`). Native write_sdc is stored state, not proof
  of exhaustive exception effects.

## Returned diagnostic structure (native-diagnostics-01)

`sta::check_setup_cmd` Tcl body confirms that each returned group is a Tcl list:
**first element = complete message, remaining elements = detail strings**.
There is no category tag in a group. Call each category independently with a
one-hot seven-boolean vector to establish category identity, retaining *all*
groups and their full details; do not classify by English message text.

Real no-SDC control, versus the positive baseline's seven empty categories:

| Category | Groups | Detail strings |
| --- | ---: | ---: |
| no_input_delay | 1 | 19 |
| no_output_delay | 1 | 2 |
| reg_multiple_clks | 0 | 0 |
| reg_no_clks | 1 | 5 |
| unconstrained_endpoints | 1 | 7 |
| loops | 0 | 0 |
| generated_clks | 0 | 0 |

The combined call returns four groups. Both full raw reports and one-hot native
results are retained in `acceptance/pt7c/native-diagnostics-01/`.
`write_sdc -no_timestamp` works. The setup-only and disable-timing calls returned
without Tcl exceptions; their actual serialized state is retained separately
in `setup-only.sdc` and `masking.sdc` (no edits to the original SDC).

## Counterfactuals and embedded OpenSTA

`controls-02-*` contains eight completed real native attempts on **new copies
of native-written state**, not patched emitted bundles. Baseline external
`ena -> _4_/D` min/max reports are empty. Removing its exception exposes both
min and max witnesses; setup-only exposes min and suppresses max. Broad scope
and CLK→Q disable masking state serialize successfully (masking emits
`set_disable_timing -from {CLK} -to {Q} [get_cells {_4_}]`). Separate missing
input-delay, output-delay and clock controls preserve native reports.
Downstream `_4_/Q -> _3_/D` baseline hold remains **−0.044244 ns**.
This establishes only bounded witness suppression, not exhaustive effect.

Attempt `native-controls-01` retains unsupported `reset_path`; subsequent attempts
use new native-state copies instead. Reset-effect coverage remains unavailable.

`openroad-api-01` confirms embedded OpenSTA **2.7.0**, identical seven-boolean
API and writer Tcl body in actual OpenROAD
`dcf36133a369abc8f3c5e5738cd4d82e4903c0e0`. OpenROAD's public `link_design`
requires technology LEF (`ORD-2010`), unlike standalone STA; this failed attempt
is retained. B's actual STAPrePNR Step must supply its normal technology context.

## Early qualification of A's actual producer literal

`producer-probe-01/` retains the source and extracted literal bytes of A's
`timing_coverage_tcl.ml` (source hash in `source.json`). This is explicitly an
early source probe, **not final provider capture or emitted bundle acceptance**.
All eight controls completed both `HC_ASIC_NATIVE_V1_COMPLETE` and the enclosing
probe marker. The producer runs unchanged on native OpenSTA 2.7.0. Baseline has
all seven explicit completed categories, zero groups and 12 endpoints.

The producer's raw check report exactly displays the preserved message/detail
strings in the observed native order. Missing-input-delay-only gives 18 input
details plus two unconstrained D endpoints; missing-output-delay-only gives two
output details. No-clock gives five unclocked CLK pins and seven unconstrained
endpoints. These differ legitimately from the wholly no-SDC 19-input control
(the delayed baseline's clock remains defined in the input-delay-only control).
Final emitted-member qualification and generic reader acceptance remain pending
the final A/B provider handoff.

**A integration finding (pending reader qualification):** the current
`timing_native_coverage.ml` `base_commands` list observed during C's preparation
omits `set_timing_derate`. All actual native baseline states here contain
`set_timing_derate -early ...` and `-late ...`; this is ordinary emitted policy,
not unsupported exception masking. Please qualify/include the actual writer
form before final provider capture, or baseline interpretation will reject.
The same observed baseline ends with `set_max_fanout 10.000000000000
[current_design]`; current `base_word` also omits the zero-argument
`[current_design]` query. Both ordinary writer forms need qualification. These
are concrete baseline bytes in `producer-probe-01-baseline/native-state.sdc`.

## Actual installed LibreLane API for B

`runtime-api-03/` retains the actual image-installed Step/MRO source under one
CPU (introspection only). `STAPrePNR.get_command()` normally invokes **standalone
`sta -no_splash -exit .../openroad/sta/corner.tcl`**. Thus using standalone
OpenSTA inside the genuine `OpenROAD.STAPrePNR` Step is native behavior; the
separate public OpenROAD LEF failure above does not block that route.

`STAPrePNR.load(config, state_in, pdk_root)` expects Step-filtered config;
`start(toolbox=..., step_dir=...)` is final and persists its own state/config.
`MultiCornerSTA.run` uses `ThreadPoolExecutor(max_workers=STA_THREADS or
_get_process_limit())`; explicit `STA_THREADS=1` is necessary. It deduplicates
equal corner file lists, creates each corner directory, prepares its environment
and calls `run_corner`. `STAPrePNR.run_corner` adds `_SDF_SAVE_DIR`, then
`MultiCornerSTA.run_corner` adds `_CURRENT_CORNER_NAME` and calls
`run_subprocess(get_command(), log_to=.../sta.log, env=current_env, silent=True,
report_dir=corner_dir)`. It does **not** overwrite the retained library/netlist/
SDC variables inside that parent call. This supports B's current wrapper seam.
Attempt 02 retains an introspection mistake (`OpenSTAStep` has no `run_corner`);
03 walks the actual MRO and completes successfully.

## Preliminary captured reader result — blocking A finding

`capture-integration-01` is explicitly a **preliminary**, separate
`.dev/asic-pt7c/probe-provider` snapshot (not the final provider store).
Capture/install and the `_build_pt7c` acceptance adapter compiled successfully.
Actual native baseline interpretation then **rejected**, exit 2:

```
native coverage: unsupported native SDC command: set_false_path -from
```

Evidence: `native-integration-01/baseline.stderr`, full outer attempt
`reader-integration-01/`. The tokenizer's bare-word backslash-newline handling
appears to append a space to the current token, skip indentation, then continue
consuming `-from` into the command token. Native writer emits `set_false_path\\`
newline with **no preceding space**, so outside braces/quotes the continuation
must act as a word separator. Please add the exact real writer form as a fixture.
No producer/parser implementation was copied into C, and no A-owned file changed.

## Preliminary real ordinary coarse run — blocking B finding

`coarse-integration-02` performed real ordinary synthesis from the fresh public
`bundle-integration-01`. Exact run:
`.dev/asic-pt7c/probe-runs/20261028T164800799130Z_44ded577`.
Synthesis completed; automatic **separate native STAPrePNR was attempted and
failed**. All failed companion/corner/native inputs are retained. Native error:

```
Error: driver.tcl, 1 can't read "::env(PT7_RECEIPT)": no such variable
```

Root cause established from actual image API in `runtime-api-06/stdout.log`:
`TclStep.run_subprocess` calls `_reroute_env`. Changed non-allowlisted variables
are written into `corner/_env_ThreadPoolExecutor-1_0.tcl`, not passed directly in
the process environment. `_TCL_ENV_IN` points to that file. **The wrapper driver
must source `$::env(_TCL_ENV_IN)` before accessing PT7_RECEIPT**, following the
normal native Tcl bootstrap. Normal corner script sourcing happens too late.
The retained environment Tcl contains the expected PT7 fields. A separate direct
native environment probe (`environment-api-01`) confirms OpenSTA itself preserves
normal subprocess environment variables; no image/tool issue was inferred.

`coarse-integration-01` retains C's earlier public grammar mistake (`--bundle`);
the actual public CLI takes positional bundle/run arguments. C's continuation
script is corrected. These preliminary attempts are not final acceptance.
