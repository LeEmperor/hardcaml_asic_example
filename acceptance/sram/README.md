# Exact SRAM acceptance evidence

## Accepted physical P4 checkpoint — 2026-10-25

**Public full run and external postcheck passed**, followed by independent
physical-record/hash/policy validation and positive/negative final-gate replay.

| Identity | Value |
| --- | --- |
| Public run | `be961b2c95f74c81ad6af81ca4d2b269` |
| External TT/gate postcheck | `0553f6d19c8f42d28c057fc65ed23510` |
| Bundle | `fa38d9064dffdf2ec1578c79c2e8890eba81bf704af460e85fcc6031b707d53c` |
| Development provider generation | `71a9a125992e4260b38dcdf954c6b965` |
| Captured source SHA-256 | `632cb3358e36d193d3a580b9fa11164b8f376673d259bfbcfdd46ee1fdf68b99` |

[`physical-p4/`](physical-p4/README.md) retains the immutable bundle inputs, exact
provider receipt, public run/collection, physical policy and all hashed artifacts,
final GDS/netlist/metrics, original external TT reports/logs and used-cell replay
models. It also retains compact raw failed P1/P2/P3 records, exact bundles, provider
receipts and diagnostics; large old final views are hashed rather than duplicated.
Original public failures are never relabeled.

One unchanged stock `RM_IHPSG13_1P_256x16_c2_bm_bist`, latency one, **16 original
staging flip-flops**, and no new architectural state. Final physical fillers/decaps
and combinational delay/buffer cells are not additional registers.

| Corner | Setup slack, ns | Hold slack, ns | Setup/hold/slew/cap/fanout violations |
| --- | ---: | ---: | --- |
| Fast | 15.809827 | 0.223533 | all 0 |
| Slow | 11.246561 | 0.814843 | all 0 |
| Typical | 14.150889 | 0.430151 | all 0 |

Routing DRC, assembled-real-GDS KLayout, illegal overlaps, power-grid, antenna and
LVS counts are zero. **Raw Magic count remains 3**: exact stock wide-LEF-obstruction
layer controls disposition all 3; unclassified count is 0. Supplied stock SRAM
collateral is unchanged. LVS is **abstract macro-boundary with schematic CDL**,
not internal-device verification. The accepted external gate replay and portable
replay are **zero-delay functionality**, not SDF/timed SRAM conformance. IR/EM is
not established, and the fast standard-cell −40°C / SRAM −55°C difference remains.

The original public compiled gate rejects `+negative` on the deliberately corrupted
low byte, exit **1**, with the run mounted read-only. A tar-restored snapshot compiled
with host Icarus passes **1,280 word checks** and rejects the same negative oracle.
Before/after original artifact hashes are retained; no original run was changed.

### Verify or replay without the original workspace

```sh
python3 acceptance/sram/verify.py acceptance/sram/physical-p4
python3 acceptance/sram/verify.py acceptance/sram/physical-p4-archive-check
python3 memory/replay_snapshot.py --snapshot "$PWD/acceptance/sram/physical-p4" \
  --output-dir /tmp/opencode/sram-p4-replay-NEW
```

- Main snapshot: **237 files / 85,863,331 bytes**, complete SHA-256 inventory verified.
- [`physical-p4.tar.gz`](physical-p4.tar.gz): **8,789,090 bytes**.
  SHA-256: `91503ecea09bd81fbe880874e4bd18737b1d5030ac206e3176656dd65f2aeb52`.
- [`physical-p4-archive-check/`](physical-p4-archive-check/summary.json): **12 files /
  9,014 bytes**, verified final-archive restoration and positive/negative replay logs.

Extract the archive and run `python3 verify.py .` inside `physical-p4/`; then run
its `replay_snapshot.py` with a new external output directory. Checksum verification
needs standard-library Python only; portable replay additionally needs Icarus.
Neither needs a PDK/provider/original absolute paths. Full physical tool re-execution
still needs the identified original dependencies. See [PHYSICAL.md](../../memory/PHYSICAL.md).

## Historical synthesis checkpoints (C1/C2)

The remaining sections describe the historical synthesis-only scope, unchanged.

C2 run **`8b48d7d0818d494f8a9c45000c2bcbbd`**, 2026-10-24, public installed
coarse synthesis with the corrected resource/instance evidence validator, bundle C2
`4fe842a7c07b94ae9e8e0546210c9273d019fccdca2d5cbf84311948bde64d09`.

Provider generation: `.dev/asic-sram/generations/aa00a92d707447fcba308789e57fa2f6`.
Development capture SHA-256:
`8f054fde7462a687139b31564fd823bedb4e0a0f1d7197ea813dcefee27214ca`, differing
from observed base `bba13079abd519b984e522aa7e898cbef85f4139`.
The retained receipt is local capture evidence, not a released pin or generator stamp.

Previous C1 run `cfd39c581711495cbfd7a150a21715f4`, bundle
`480bdd2c6fe04f307fb18de70cebd2fe20c031caeec81d095fa30fe2b317be77`, remains
preserved separately.

## Passing mapped functional evidence

`8b48d7d0-functional/` is the current durable passing snapshot;
`cfd39c58-functional/` is the unchanged historical C1 snapshot. Both use this layout:

| File(s) | Evidence |
| --- | --- |
| `summary.json` | Run/bundle/dependency attribution, mapped cell counts, metrics, area scope, replay commands/outcomes, model adaptation and limitations |
| `checksums.json` | SHA-256 and sizes of every other file in the snapshot; original source paths for retained inputs |
| `mapped.v`, `mapped.json` | Actual final gate netlist and raw Yosys mapped JSON, not generated behavioral RTL |
| `stat.json`, `metrics.json`, `synthesis.log`, `lint.log` | Raw synthesis counts/area/checks, Yosys version and unused-input warning |
| `run.json`, `run-preflight.json`, `public-preflight.json` | Public launch/completion and raw preflight records; C2 uses the run-local report for both preflight copies |
| `manifest.json`, `bundle-config.json`, `resolved-config.json`, `synthesis-config.json` | Exact bundle contract and resolved synthesis settings |
| `provider-receipt.json`, `bundle-inputs/` | Captured development dependency identity and exact bundle source inputs, including dirty/untracked attribution |
| `check_mapped.py`, `replay.v` | Acceptance runner and existing testbench snapshot |
| `models/` | Original stock SRAM models, standard-cell Verilog/UDP, macro typical Liberty area, and derived used-cell zero-delay functional view |
| `compile.*`, `replay.*`, `negative.*`, `iverilog-version.*` | Raw compiler/replay output, expected negative mismatch, simulator version |

The gate test passed **1,280 word checks** and its negative oracle exited **1** on
the deliberate low-byte mismatch. Compilation and positive simulation exited **0**.
The gate netlist retains **one stock SRAM + 16 original staging flip-flops**, with
176 total mapped cells and no inferred latches, unmapped cells or synthesis check
errors. Synthesis reports 2,182.7232 µm², omitting macro area; the macro Liberty
area is 28,127.104 µm². Their sum is only a cell-area estimate.

Direct `cmp` checks found C2 **mapped Verilog and metrics byte-identical to C1**.
Both mapped netlists have SHA-256
`a12c6b63e21ed2ab2898bd7c41da3f6dfac768b53382538a7acfb96dd9918575`.
The corrected provider changed runtime validation, not this synthesized hardware.

Verify the complete snapshot inventory from the example root:

```sh
python3 acceptance/sram/verify.py acceptance/sram/cfd39c58-functional
python3 acceptance/sram/verify.py acceptance/sram/8b48d7d0-functional
```

Verification passed: C1 **37 files / 591,602 bytes**; C2 **37 files / 595,437 bytes**.

The original timing-cell model cannot run directly in Icarus because timing-check
delayed-reference outputs are unsupported. The retained derived view preserves
used-cell vendor logic and UDP calls, omits `specify`, and directly wires the
staging cell's delayed CLK/D/RESET_B inputs. It does not modify the gate netlist,
PDK checkout or vendor SRAM model. **No timing/SDF claim is made.**

To replay using only this evidence snapshot and installed Icarus, from the example
root (compiled output goes outside the snapshot):

```sh
E="$PWD/acceptance/sram/8b48d7d0-functional"
iverilog -g2012 -DFUNCTIONAL -s memory_replay -o /tmp/opencode/sram-mapped.vvp \
  "$E/replay.v" "$E/mapped.v" \
  "$E/models/RM_IHPSG13_1P_256x16_c2_bm_bist.v" \
  "$E/models/RM_IHPSG13_1P_core_behavioral_bm_bist.v" \
  "$E/models/sg13cmos5l_used_functional.v" "$E/models/sg13cmos5l_udp.v"
vvp -n /tmp/opencode/sram-mapped.vvp
vvp -n /tmp/opencode/sram-mapped.vvp +negative  # Expected exit 1.
```

## Retained initial failure

`cfd39c58/ATTEMPT.md` describes the first attempt using the unmodified timing-cell
model. Its compiler/replay logs show undriven delayed-reference nets and an X-valued
first response. It is not a passing acceptance snapshot.

## Attribution and limits

The bundle preserves example revision `ac7054395a068c19ced0cd01dd5cc0bcc1ec0015`
plus untracked `memory/` input bytes. It does not claim a clean checkout.
The C1 linked provider was development capture
`9d8dd740d3ff69990b08ee8e024898ba83a7844400785bb3aeae94b33837255f`, differing
from observed base `bba13079abd519b984e522aa7e898cbef85f4139`; the historical
dependency record was not advanced. Later README/checker edits are not C1 inputs.
The current C2 provider/capture is identified at the top of this index. C2 preserves
its own exact source inputs and Git statuses; subsequent index/memory documentation
updates are outside both checksum-covered snapshots. No historical snapshot files
were changed for the C2 update.

This evidence establishes mapped synthesis and bounded zero-delay gate functionality.
It does **not** establish timed SRAM conformance, STA closure, physical macro power
access, placement/routing, DRC, LVS or physical acceptance. Whole toolchains and
large PDK/layout trees are intentionally not archived here.
