# Registered program-memory SRAM testbed

Independent of the FIFO, this is a real public `Single_port_ram.create` consumer:
**256 words × 16 bits, one shared read/write port, read latency one**, stable
resource ID **`program`**. `program_memory.ml` contains the typed full-width core,
a small byte-wide TT adapter, and the project declaration. It uses production
`Technology.ihp_sg13cmos5l`, never an experimental mapping or local macro RTL.

This is the ongoing production-style SRAM consumer. Exact now selects stock
`RM_IHPSG13_1P_256x16_c2_bm_bist` through the production backend, retaining the
original cycle contract and **no new architecture registers**. The existing two
8-bit TT staging registers remain consumer-owned. Exact requests
`Flow.Operation.Synthesis`; explicit flops retain their previous Hardening declaration.

The Exact declaration includes optional consumer intent using
`Macro_intent.tt_cmos5l_r0 ~resource:(Resource.Id.of_string_exn "program")
~x_um:42. ~y_um:81. ~halo_um:2. ()`, passed with `Flow.librelane ~macros`.
`Program_memory.project ~with_macro_intent:false Exact` explicitly omits that intent;
the CLI uses the declared intent. The actual emitted instance is
**`hc_resource_7_program`**. R0, halo and power mappings are declarative intent,
not verified physical supply access. Hardening/full/segmented macro execution is
explicitly unsupported in this provider slice.

## Isolated dependency and validation

The PT.0 historical private generation was
`.dev/asic/generations/3c70c76700764a58974ef7d969adba36`, observed provider base
`ad290d825272b588eb0fe0202e84ce407ae221f5`, captured snapshot SHA-256
`4d804d7f454a940bd93a9a5b72192922c901011e2f0d18e3413ac5c095f78f3f`.
The adoption capture is instead stored in **`.dev/asic-sram`**, keeping FIFO and
Workbench selections independent. The old `asic-dependency.json` pin remains unchanged.
Refresh explicitly captures current provider worktree bytes without Git writes:

```sh
python3 scripts/asic_dependency.py --store "$PWD/.dev/asic-sram" refresh \
  --source /home/wayne/devel/jane/hardcaml_asic --mode development --jobs 6
. "$PWD/.dev/asic-sram/current/activate.sh"
python3 scripts/asic_dependency.py --store "$PWD/.dev/asic-sram" status --json
ocamlfind query hardcaml_asic
dune build --build-dir _build_sram -j6 memory/memory_cli.exe memory/test/memory_test.exe
dune runtest --build-dir _build_sram -j6 memory --force
MEMORY="$PWD/_build_sram/default/memory/memory_cli.exe"
"$MEMORY" check --selection flops
"$MEMORY" check --selection exact
python3 memory/check_bundle.py --cli "$MEMORY" \
  --core-exporter "$PWD/_build_sram/default/memory/test/memory_test.exe" \
  --source-root "$PWD" --pdk-root "$PWD/_flow_tools/pdk" --require-rtl
```

Every invocation requires explicit `flops` or `exact`. There is no fallback:
the policy has only an instance rule for `program` and no default. `check`
elaborates/resolves without reading source or creating output; `emit` uses public
`Project.emit_bundle` with both implementation and simulation RTL and explicit
source provenance. Output must be new/empty. No command invokes physical tools.
The 48 MHz clock and 0–1 ns input / 0–2 ns output delays are specimen assumptions,
not evidence of timing closure or fit of 4096 flop storage bits in TT6x4.

Exact selection succeeds in both elaboration modes. Simulation remains a generated
behavioral model; Implementation directly instantiates the selected stock macro.
Unsupported 128×16 Exact requests still fail in both modes without fallback or rounding.

## Coordinator-only public synthesis launch

After validation, emit a fresh immutable bundle (choose a new directory on repeats):

```sh
. "$PWD/.dev/asic-sram/current/activate.sh"
MEMORY="$PWD/_build_sram/default/memory/memory_cli.exe"
PROVIDER="$PWD/.dev/asic-sram/current/bin/hardcaml-asic-flow"
BUNDLE="$PWD/.dev/program-memory-exact-c1"
"$MEMORY" emit --selection exact --source-root "$PWD" --output-dir "$BUNDLE"

# Coordinator runs these separately when allocated; neither ran for assignment C.
"$PROVIDER" preflight "$BUNDLE" --toolchain "$PWD/_flow_tools" \
  --results-root "$PWD/_flow_results/sram" --json
"$PROVIDER" run "$BUNDLE" --toolchain "$PWD/_flow_tools" \
  --results-root "$PWD/_flow_results/sram" --stage synthesis --json
```

This is the installed provider's **fresh coarse synthesis** route, not a custom
executor or FIFO/named-stage dispatch. The provider caps this macro route at six
LibreLane/OpenROAD/KLayout/OMP cores and one STA corner worker. Full Hardening,
segmented stages/checkpoints and physical finalization are rejected. Keep all Dune
commands at `-j6` or lower. Emission/functional acceptance do not run EDA or preflight.

The manifest's `macro_contract` binds logical resource to actual instance, stock
collateral, explicit physical intent and synthesis-only execution. Its
`implementation_simulation.models` contains the two `pdk_dir::` vendor references;
`defines` is `["FUNCTIONAL"]`. Acceptance resolves these against the selected PDK
technology directory and compiles them with implementation RTL, **without** the
generated synthesis stub or behavioral top. Timed-model conformance, mapped synthesis
and physical acceptance remain separate evidence. The fast standard-cell −40 °C /
macro −55 °C Liberty difference remains explicit.

## Memory and adapter contract

At a rising edge, enable=0 holds response and storage; enable=1/write_enable=0
registers the addressed word; enable=1/write_enable=1 writes the full 16-bit word.
There is no RAM reset, initialization, mask, or simultaneous read/write. Response
after writes and reads of unwritten words is unspecified. Tests load before read
and never assert those values or depend on simulation poison/power-up zeros.

The bundle top is `tt_um_program_memory`. `clk` clocks everything. `ena && rst_n`
permits commands; low `rst_n` synchronously clears only adapter address/low-data
staging, never the memory. `ui_in[1:0]` commands use `uio_in[7:0]` as payload:

| Command | Edge action |
| --- | --- |
| 0 | Read staged address; response appears after this edge |
| 1 | Stage 8-bit address; RAM disabled |
| 2 | Stage low write-data byte; RAM disabled |
| 3 | Write `{uio_in, staged_low_byte}` at staged address |

Stage address and low byte before committing. `uo_out` shows low response byte
when `ui_in[2]=0`, high byte when `ui_in[2]=1`; this byte selection is combinational.
`ui_in[7:3]` are ignored. `uio_oe` and `uio_out` are always zero (input-only payload
bus). `uo_out` masks to zero while disabled/reset; unmasking reveals retained RAM
response. Inputs must be synchronous; no reset synchronizer is supplied.

The PDK-free Cyclesim tests exercise public Simulation and Implementation flop
circuits and Exact Simulation, all addresses/full-width data, consecutive latency-one
reads, disabled reads/writes and output hold. Resource checks cover both modes and
both selections, optional intent resolution and unsupported Exact shape rejection.
The bundle checker uses read-only Git inspection of the actual source checkout,
two deterministic public emissions, all file/input hashes, separate RTL sets,
resource policy, real macro identity/configuration and original register count. Temporary bundles live
under `.dev/` and are removed after checking. It performs no Git writes.
With `iverilog` and `vvp`, the checker also replays full-address load/read and
adapter/disabled-hold/reset checks against each emitted RTL set independently,
and proves all four selection/source-set combinations reject a corrupted expected
response. A separate public-elaboration core RTL export is replayed against the
same actual vendor models, with consecutive changing-address reads, disabled writes
and full-width overwrites; it also rejects a corrupted oracle. `--require-rtl` makes
missing tools an error; without it their absence is an explicit RTL skip.

## PT.0 verification (2026-10-24)

The following is historical, before public Exact adoption. Its old negative Exact
expectation is superseded by the current commands and adoption evidence below.

Using the exact private ASIC prefix above:

* `dune build -j6 memory/memory_cli.exe` — passed.
* `dune runtest -j6 test memory --force` — passed. Memory Simulation and
  Implementation each checked **1,792 edges** plus inventory/policy/Exact checks;
  the FIFO core checked **7,330 directed + 20,017 seeded edges**.
* `python3 memory/check_bundle.py --cli _build/default/memory/memory_cli.exe
  --source-root "$PWD" --require-rtl` — passed whole-bundle/CLI acceptance and
  **1,280 word checks per generated RTL set**, including negative oracles.
* `dune runtest -j6 .` — passed the existing FIFO wrapper, resolution, catalog,
  CLI, bundle and routing checks. FIFO synthesis/simulation RTL each passed
  **11,429 edges** and a negative oracle. The routing suite reported 21 cases,
  with its opt-in installed-native-provider fixture explicitly skipped.
* `dune build -j6 @all` — passed with the existing Workbench provider SDK also
  selected (needed only for the existing simulation provider adapter):

  ```sh
  OCAMLPATH="$PREFIX/lib:$PWD/.dev/workbench-provider-sdk/lib" dune build -j6 @all
  ```

  Without that extra SDK path, the broad build reports the existing missing
  `hardcaml_workbench_provider` dependency; the memory targets need only the ASIC
  prefix. No dependency build/install, active-generation change, Workbench config
  edit, or physical EDA was needed. Exact's unsupported production mapping is the
   intentional remaining backend blocker at PT.0.

## Public Exact adoption verification (2026-10-24)

Isolated generation: `.dev/asic-sram/generations/ae408e67c800432f9d16cf1d19ed3d74`.
Observed provider base: `bba13079abd519b984e522aa7e898cbef85f4139`.
Captured worktree SHA-256:
`9d8dd740d3ff69990b08ee8e024898ba83a7844400785bb3aeae94b33837255f`.
This is a local development receipt, not a released pin or generator stamp.

* Six-job refresh passed install, compiled external API and Dune link probes.
* Focused build and memory tests passed: **1,792 edges each** for Flops Simulation,
  Flops Implementation and Exact Simulation (**5,376 total**).
* Inventory checks passed for both selections/modes; optional intent resolved both
  present and absent; unsupported 128×16 Exact failed in both modes without fallback.
* Two deterministic emissions per selection passed whole-tree/hash/source-provenance,
  configuration, macro/source-separation and nonempty-output refusal checks.
* Four TT RTL replays passed **1,280 word checks each** (**5,120 total**).
* Direct Exact core vendor-model replay passed **2,048 edges / 1,536 response checks**.
  All **five** RTL replays rejected a corrupted-data oracle. Core RTL has no local
  registers; Exact TT RTL has only the two original 8-bit staging registers.
* No preflight, synthesis or physical EDA ran in assignment C. Coordinator launch
  and mapped-netlist evidence are pending; timed-model and physical gates remain open.
