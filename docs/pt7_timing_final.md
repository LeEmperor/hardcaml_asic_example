# PT.7 final-candidate native acceptance — bit and scalar

2026-10-28, round r3. **Bounded native bit-source and scalar-source acceptance
completed. B inspection remains intentionally exit 1 / coverage unavailable.**
Earlier failures are retained, not relabelled or overwritten. This round uses a
new provider capture, new complete public bundles and new actual native runs.

## Exact identities

| Item | Identity |
| --- | --- |
| Isolated provider generation | `.dev/asic-pt7/provider/generations/74e9a52b43a14c69bff2763325b39522` |
| Observed provider base | `e46bfd7609e0b119ad74a8b412a3e866da5297de` |
| Captured provider source SHA-256 | `a6723afb6a88bce6152d7b05662ea614a6e1a75352b870b4e20391e7c2d3f684` |
| Capture receipt SHA-256 | `10b8bf667b72adf1b1936f810a6df37ea8974ae3770bd6db736960cf1ba606ef` |
| Installed renderer SHA-256 | `9c53a5b75313adacd979ea5b559fd17ad0c51d2961c4df6dc0a41813a88d25d2` |
| Emitter executable SHA-256 | `0ff4ef097819a3f854ae7a90a2343fa792aefebd776aff9e0de8abf6f7e69e31` |
| Native B inspector SHA-256 | `e6a3dd3b2d1464638c4467a9ae728eb61a07163bb2ae144fd2554396c48d0344` |

The installed renderer exactly matches the requested final candidate. The retained
provider receipt identifies dirty development bytes, not an authenticated
execution, clean checkout or P6 source stamp. All installed binary/archive hashes,
emitter compiled artifact hashes, actual A sources and final A/B handoffs are in
`acceptance/timing/closeout-final-r3/`.

| Item | Bit source | Scalar source |
| --- | --- | --- |
| Build identity | `6db329a39eb1c1e4d500f1808bc0dbfb95a355561b919f1b810a4e299503fadb` | `a6e8bd78b9db84e12c71a9e312df34b01944f9669e955092289a7a1c1a684ddd` |
| Audit/run ID | `sta-bit-r3` | `sta-scalar-r3` |
| Audit JSON SHA-256 | `162134bb581647d74db57a73f9f5ec8220d29e0447cf67edf8e979619ac7bd0c` | `eadd4162e90b0374bc353c861e5dcc143204fd5293faf8d82ad76648311f53e6` |
| Producer receipt SHA-256 | `80c79d61cca42570d9b02f0de6217683d1d64eca513abfdd640f9897fb832e61` | `3a12c8f7308d14360b6e97c26b24ac9fe2b2b6c81630ffa5f24ea46c0d7fea1c` |
| Complete emitted SDC SHA-256 | `47077f72e69b42bbb046c84ee0a8ac552035249eac68c7a830006b6fb5027db8` | `7d66fe0de02bd45b4c214585719e39d8dab253a7e5cecc5342090c170bb1a128` |
| Mapped Verilog SHA-256 | `d3858042fe1672eb9ba2fb97e7deaacf30b80385dc719ecde9d262c29d82f132` | `8d6459a26eda8a65c1a9d729ff2031cb675295f8449e5421f446e30822984e0b` |

The raw `audit.json` source inventories additionally bind the full emitted
manifest, exact executed driver, Liberty, complete native log, resolution stream,
exception/unconstrained reports, downstream min/max reports, native version,
receipt and process result. Whole emitted bundles are retained in
`synth-bit-r3-bundle/` and `synth-scalar-r3-bundle/`. All bundle member hashes and
current declared input hashes were verified during closeout.

Actual producers: Yosys **0.66**, commit
`86f2ddebce7e98ce7cacc27e8a5c14cb53b51b51`; standalone OpenSTA **2.7.0**;
CMOS5L `nom_typ_1p20V_25C` Liberty SHA-256
`34163f3e7de9f854afac57332ba06f1739b78e7ac35660a8a5ddd39c570124ad`.
Exact local tool image:
`sha256:d109140b8f17fc54f4fca998beb8124f4949404ec52e339eebd2250854a18b5a`.
OpenROAD was used only for the earlier native diagnostic probes; neither these
successful audits nor any P&R result is attributed to it.

## Executed commands and bound inputs

Capture and build logs: `capture-03/` and `emitter-build-07/`. Commands ran via
`timing/record_command.py` to retain argv/stdout/stderr/result and supply the
isolated provider `PATH`/`OCAMLPATH`:

```sh
opam exec --switch=5.2.0+ox -- flock /tmp/opencode/asic-pt7-build.lock \
  python3 -B scripts/asic_dependency.py --store .dev/asic-pt7/provider \
  refresh --source /home/wayne/devel/jane/hardcaml_asic --mode development --jobs 6
opam exec --switch=5.2.0+ox -- flock /tmp/opencode/example-pt7-build.lock \
  dune build --build-dir _build_pt7 -j6 timing/timing_cli.exe
_build_pt7/default/timing/timing_cli.exe emit \
  /home/wayne/devel/jane/hardcaml_asic_example \
  /home/wayne/devel/jane/hardcaml_asic_example/.dev/asic-pt7/bundle-bit-r3
_build_pt7/default/timing/timing_cli.exe emit-scalar \
  /home/wayne/devel/jane/hardcaml_asic_example \
  /home/wayne/devel/jane/hardcaml_asic_example/.dev/asic-pt7/bundle-scalar-r3
```

For each `KIND` in `bit`, `scalar`, executed **sequentially**:

```sh
python3 -B timing/real_tools.py synth --label synth-KIND-r3 \
  --bundle .dev/asic-pt7/bundle-KIND-r3
python3 -B timing/real_tools.py audit --label sta-KIND-r3 \
  --bundle acceptance/timing/synth-KIND-r3-bundle \
  --synthesis acceptance/timing/synth-KIND-r3
python3 -B timing/check_acceptance.py --generation .dev/asic-pt7/provider/current \
  --audit acceptance/timing/sta-KIND-r3 --synthesis acceptance/timing/synth-KIND-r3 \
  --output acceptance/timing/checked-KIND-r3
python3 -B timing/connectivity_cases.py --audit acceptance/timing/sta-KIND-r3 \
  --synthesis acceptance/timing/synth-KIND-r3 --label connectivity-KIND-r3
python3 -B timing/connectivity_cases.py --audit acceptance/timing/sta-KIND-r3 \
  --synthesis acceptance/timing/synth-KIND-r3 --label taps-KIND-r3 --taps-only
python3 -B timing/check_semantic_evidence.py --generation .dev/asic-pt7/provider/current \
  --audit acceptance/timing/sta-KIND-r3 --output acceptance/timing/semantic-KIND-r3
```

Additional executed checks:

```sh
python3 -B timing/native_negatives.py --attempt r3 --audit sta-scalar-r3
python3 -B timing/check_semantic_evidence.py --generation .dev/asic-pt7/provider/current \
  --audit acceptance/timing/sta-bit-r3 --output acceptance/timing/semantic-envelope-bit-r3 \
  --envelope-only
python3 -B timing/seal_final.py --generation .dev/asic-pt7/provider/current \
  --output acceptance/timing/closeout-final-r3
```

These names refer to completed immutable attempts; any rerun needs new names.
The synthesis script and emitted RTL bytes are retained. This is explicit bounded
standalone mapping/STA of public bundle inputs, not a claimed named-flow or
execution-store run. No consumer-local timing parser/resolver was introduced.
The driver reads the exact unmodified emitted SDC once. External receipt bytes
avoid a self-hash cycle, print before SDC, and bind all primary inputs; completion
prints only after native reports. Process-result argv and input pre/post hashes
are retained independently by the bounded launcher.

## Actual preservation, scope and downstream checks

Both synthesis inventories preserve five distinct `sg13cmos5l_dfrbpq_1` cells:
capture first/second/third = `_4_`/`_3_`/`_2_`; control first/second = `_5_`/`_6_`.
Assertions verify scalar exact Q nets/unique drivers, chain D links, primary CLK
and actual external active-low `rst_n` to RESET_B. The bit source is `ui_in[0]`;
the scalar source is `ena`. All original registers use active-low reset-to-zero.

Both native SDC loads resolve every stage, clock, first-stage source and enumerated
reset source before `validated` and two successful `set_false_path` calls.
Capture scope is solely source → `_4_/D`; reset scope is the five RESET_B pins.
The corrected real Pin→Term→internal-Net route succeeds without overrides.

Each main audit retains three setup and three hold paths with exact native
start/endpoints, type, library setup/hold checks and numeric slacks:

| Path | Max/setup slack (ns), both audits | Min/hold slack (ns), both audits |
| --- | ---: | ---: |
| `_4_/Q -> _3_/D` | +19.432287 | **−0.044244** |
| `_3_/Q -> _2_/D` | +19.432287 | **−0.044244** |
| `_5_/Q -> _6_/D` | +19.432287 | **−0.044244** |

The first-stage external capture samples have no min/max paths after exception.
Downstream paths remain visible, **including the hold violations**. This is
preservation acceptance, not timing closure. Clock is ideal and interconnect
parasitics are absent; only the typical corner was allocated.

## Native fixtures: real graph checks, not common baseline failures

All **34 connectivity fixtures** passed their assertions, 17 per source form:

* Three positives per form: direct baseline; actual noninverting mapped CMOS5L
  buffers on clock/data/reset; eight-buffer data-source route. Each emitted two
  applied records, complete, and all three downstream min/max path samples.
* Four negatives for each of clock/data/reset: wrong input, constant,
  disconnection and inversion. Plus wrong interstage D and nine-buffer overflow.
  All **28 negatives** exited 1 with the intended role-specific diagnostic and
  zero validated/applied/complete records. A passing baseline is a prerequisite.

Six additional native tap controls passed (baseline plus Q-output/source-output
tap per form), directly exercising R4's filtering of top-level output sinks.
Five further anchor/scope negatives passed: missing anchor, two Q drivers,
buffer master on Q, wrong interstage connection, and downstream capture target.
The last uses an explicit diagnostic SDC copy; the published bundle is untouched.
All others above consume unchanged emitted SDC. Raw native diagnostics, process
results, netlist mutations and exact hashes are retained. Buffer/tap fixtures are
controlled mapped-netlist mutations, not additional synthesized products.

Native `check_setup -verbose` bytes are retained for each main audit. There is no
native `report_exceptions` in this runtime: the actual native unsupported-command
help warning is retained, and coverage stays unavailable. The separate current
no-SDC diagnostic control retains 19 missing-input-delay ports, two missing-output
delay ports, five unclocked register pins and seven unconstrained endpoints.
`report_checks -unconstrained` output is preserved; samples are not exhaustive.

## B corrected public CLI and semantic assertions

Both actual native audits pass public inspection as **exit 1 / unavailable**,
with requested/resolved/applied separation, five producer-reported stages and
two command-completed exceptions. They do not receive a passing coverage verdict.

Across both forms, 14 ordinary evidence negatives reject with exit 2: missing
resolution, stale SDC hash, wrong producer, truncated stream, coherent wrong pin
scope, nonzero process despite completion and wrong native version.

The semantic suites add 14 rejections: changed whole-SDC prefix with re-bound
receipt/log hashes, unsupported schema, minimal envelope, broken source-copy
closure, bracketed/ANSI fatal lines and overlong lines. Four equivalence controls
(quoted INFO and reordered receipt object keys per form) remain valid/unavailable.

Eight targeted R5/R6 envelope negatives also reject for their **intended semantic
diagnostics**: absent generated/resolved configuration keys with null declarations,
SDC-as-simulation-RTL, empty/contradictory runtime policy, nonstring/missing floorplan
setting and wrong floorplan reference source. These deliberately invalid manifests
retain the asserted original payload identity; assertions require semantic
rejection before identity verification, not an incidental hash failure. They do
not claim a newly emitted or authenticated build. Total B rejections: **36**.

## Findings closed, history retained, qualifications

* A-REAL-1: closed for this candidate by actual native bit-source resolution.
* A-REAL-2: closed by successful checked internal-net tracing in both actual runs.
* R4: native Q/source output taps pass.
* B R5/R6: targeted presence/role/runtime/floorplan diagnostics pass.
* No new unexpected failure was observed in r3. Earlier compile, emission,
  unmodified-SDC native failures and probes remain under their original names.

`closeout-final-r3/preservation.json` verifies all files in both prior closeout
inventories unchanged, along with the originally observed protected files and old
provider pointers. The final checksums inventory covers all new PT.7 evidence.
No historical SRAM evidence was rewritten or associated with these runs.
Preexisting dirty app/configuration files remain intact; only the previously
necessary two existing Timing record migrations were made. No ASIC library,
Workbench, Protemu or Git mutation was performed by C.

All Dune calls used explicit `-j6` and the required locks; capture's nested builds
were sequential within six workers. Native tools were serialized under the STA
lock, explicit `-threads 1`, Docker one CPU / 4 GiB / 128 PIDs / no network /
read-only image root, with 180-second bounds. **P&R allocation/use was zero.**
Unrelated broad suites were not repeated; source hardware and old delay budgets
were unchanged. Coordinator independent review remains separate. Native coverage,
post-PNR preservation/closure, other corners, analog CDC/MTBF, reset-release
protocol and Protemu qualification remain explicitly outside this acceptance.
