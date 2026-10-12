# Controlled FIFO ASIC specimen

An independent Dune project containing a fixed Hardcaml FIFO core, a consumer-owned
Tiny Tapeout wrapper, an ASIC declaration, a standalone bundle emitter, repeatable
bundle acceptance, and PDK-free Cyclesim and generated-Verilog tests. This is a
**development specimen, not dependency-pinned**.
It uses `core`, `hardcaml`, `ppx_jane`, `ppx_hardcaml`, `yojson`, and a selectable
development build of `hardcaml_asic` exposing the hardened `Resolved_build.mli`.
The project declares Dune language 3.17 and has been built with Dune 3.24.2 and
OCaml 5.2.0+ox. No opam package or invented pin is supplied. The installed
Hardcaml interfaces under `~/.opam/5.2.0+ox/lib/hardcaml/` are the API authority.

The generic `lib/`, `test_support/`, and `test/` stanzas remain independent of the
ASIC library. ASIC integration lives in `asic/`, `bin/`, `asic_test/`, and
`acceptance/`. Building,
simulation and resolution need no PDK, Workbench, or physical EDA. The emitter
only renders/writes a bundle; it never provisions dependencies or runs a flow.

## Fixed core contract

`lib/controlled_fifo.mli` is the public contract; `Controlled_fifo.create` accepts
a typed `Signal.t I.t` and returns a typed `Signal.t O.t`.

* Capacity: **16 words of 8 bits**, held in individual registers, not
  `Single_port_ram` or another memory primitive.
* Addressing: two 4-bit circular pointers; occupancy: 5 bits, ranging from 0 to 16.
* Inputs: `clock`, synchronous active-high `clear`, `enable`, `push`, `pop`, and
  8-bit `push_data`.
* Outputs: registered 8-bit `data_out` and 1-bit `data_valid`; combinational
  `push_accept`, `pop_accept`, `occupancy`, `full`, and `empty`.

At a rising edge, using **pre-edge** occupancy `count`:

```text
active      = enable && !clear
pop_accept  = active && pop && count > 0
push_accept = active && push && (count < 16 || pop_accept)
```

`clear` dominates all other inputs, including disabled operation: its edge zeros
both pointers, count, response data, and response valid. Stored words need not
reset. Apply a clear edge before use; power-up register values are unspecified.
While clear is asserted **before** that edge, both accepts are low but occupancy
and flags still describe the existing queue.

| Pre-edge state and requests (enabled, not clearing) | Behavior |
| --- | --- |
| Empty, pop only | Reject pop; hold response data, clear response valid |
| Empty, push + pop | Accept push only; no bypass to the response |
| Full, push only | Reject push |
| Full, push + pop | Accept both; return the **old head** before replacing its slot |
| Nonempty/nonfull, push + pop | Accept both; preserve occupancy and FIFO order |

Every accepted pop registers the old head into `data_out`. Every non-clear edge
sets `data_valid` to that edge's `pop_accept`. A disabled or no-accepted-pop edge
clears valid and holds response data; disabled edges also hold the entire queue.
`data_valid` is a response to the last edge, **not** a head-visible valid signal.
Consecutive pops may keep it high. `full` and `empty` depend only on occupancy.

## Build and run

Run from this repository using the existing toolchain environment. Select the
parent library directory of the intended ASIC installation; the shared installed
package may be older and is not an equivalent API. For this workspace, one usable
development installation is `/home/wayne/devel/jane/hardcaml_asic/_build/install/default/lib`.
That sibling location is an example, not a requirement or a release pin. Preserve
any existing OCAMLPATH suffix and apply the selection to each command:

```sh
ASIC_LIBDIR=/home/wayne/devel/jane/hardcaml_asic/_build/install/default/lib
OCAMLPATH="$ASIC_LIBDIR${OCAMLPATH:+:$OCAMLPATH}" dune build @all
OCAMLPATH="$ASIC_LIBDIR${OCAMLPATH:+:$OCAMLPATH}" dune runtest --force
OCAMLPATH="$ASIC_LIBDIR${OCAMLPATH:+:$OCAMLPATH}" dune build @acceptance-strict --force
OCAMLPATH="$ASIC_LIBDIR${OCAMLPATH:+:$OCAMLPATH}" dune exec test/fifo_test.exe -- --directed
OCAMLPATH="$ASIC_LIBDIR${OCAMLPATH:+:$OCAMLPATH}" dune exec test/fifo_test.exe -- --seed 42 --cycles 100000
OCAMLPATH="$ASIC_LIBDIR${OCAMLPATH:+:$OCAMLPATH}" dune exec asic_test/wrapper_test.exe
OCAMLPATH="$ASIC_LIBDIR${OCAMLPATH:+:$OCAMLPATH}" dune exec asic_test/resolution_test.exe
```

The strict alias requires both `iverilog` and `vvp` on PATH. Ordinary `runtest`
still runs bundle acceptance when either is absent, printing an explicit RTL
**SKIP**; it does not count that as RTL acceptance. Python 3 and Git are required
for the synthetic fixture. These commands use existing tools, without installing
dependencies. Both acceptance aliases consume Dune executable dependencies
directly and never invoke nested Dune builds.

The ordinary core test executable accepts either `--directed` or **both** `--seed INT`
and `--cycles NONNEGATIVE_INT`; there are no implicit random defaults.
`dune runtest` runs the directed suite and seed 20261012 with 20,000 traffic edges.
A regression adds one initial clear, enough pops to drain the remaining queue,
and one rejected pop, so reported edge counts exceed `--cycles`. Seeded traffic
uses a local PRNG and is reproducible for the same toolchain. It alternates
fill/drain bias, emphasizes boundary simultaneous requests, and includes clear
and disabled cycles. Final draining checks the remaining data order.

Successful runs report edges, accepted and rejected operations, clear/disabled
edges, and pre-edge visits to occupancies 0, 1, 15, and 16. Rejection totals
include requests suppressed by clear or disable. Failures include the suite/seed,
cycle, phase, field, expected/actual value, current labeled stimulus and expected
trace, and up to eight preceding traces (newest first).

### Directed coverage

* All four push/pop combinations at each occupancy 0, 1, 15, and 16, crossed
  with both clear values and both enable values: **64 independent probes**.
  Each probe primes a nonzero response, builds its queue, and drains afterward.
* Clear priority while disabled, full, and requesting both operations, including
  a full queue with a valid response from the preceding replacement.
* Overflow/underflow rejection, empty no-bypass, old-head full replacement,
  response hold and valid clearing across idle/disabled/rejected-pop edges.
* Three 1,024-edge simultaneous streams at occupancies 1, 15, and 16, with
  consecutive valid responses and order-checked drains.
* 64 fill/overflow/drain/underflow rounds, exercising both pointer wraps.

## Independent model and acceptance tests

`test_support/fifo_test_support.mli` exposes plain OCaml values and depends only
on Core, not Hardcaml or the DUT:

* `Stimulus.t` / `Stimulus.create`: edge inputs without a simulator clock port.
* `Snapshot.t`: occupancy/flags and registered response data/valid.
* `Model.initial`, `Model.snapshot`, `Model.step`: immutable list-based reference
  state and a pure transition returning next state, accepted push, accepted pop.
  It removes the old head first, then appends if there is room. It has no circular
  pointers and shares no RTL acceptance implementation.
* `Trace.of_stimuli`: turn labeled stimuli into expected before/after snapshots
  and edge accepts. Custom traces should start with a clear edge.
* `directed ()` and `regression ~seed ~cycles`: ready-to-replay expected traces.

`test/fifo_test.ml` is the separate Cyclesim adapter. It drives the stimulus,
calls `cycle_check` and `cycle_before_clock_edge`, and reads `Before` outputs to
check accepts and existing state. It then calls `cycle_at_clock_edge` and
`cycle_after_clock_edge`, and reads `After` outputs to check registered responses
and updated occupancy/flags. After-edge accepts refer to a future edge and are
not mistaken for the just-completed transaction. The first edge checks clear's
accept suppression and post-clear state without assuming power-up values.

`asic_test/wrapper_test.ml` replays those same directed and seeded traces through
the TT pins without duplicating the core acceptance rules. It checks every output
byte before/after edges, thus checking occupancy bit order, response data/valid,
zero low output bits and OE. Between edges it crosses enable/reset and toggles
ignored upper inputs, then unmasks the unchanged state. These probes distinguish
an immediate output mask from a synchronous queue reset. Upper inputs also vary
at actual edges. The directed cases inherit full replacement, empty no-bypass,
reset-while-disabled priority, overflow, underflow and pointer-wrap checks.

`asic_test/resolution_test.ml` uses public `Project.elaborate_for_flow` and a
separate `Project.elaborate ~mode:Simulation`. It checks exact top/ports, target,
clock, all I/O delay ranges, template setting values/reasons, generated settings,
24 pin descriptions, and empty resource inventories in both builds. It also
checks that a Simulation build is rejected by the implementation resolution
boundary. These tests read no PDK files and render no bundles.

## TT wrapper and pin map

`asic/tt_wrapper.ml` aliases `Tt_cmos5l.I` and `Tt_cmos5l.O`; the top is
**`tt_um_controlled_fifo`**. The exact ports are inputs `clk`, `ena`, `rst_n`
(one bit each), `ui_in[7:0]`, `uio_in[7:0]`, and outputs `uo_out[7:0]`,
`uio_out[7:0]`, `uio_oe[7:0]`.

| TT pins | Meaning |
| --- | --- |
| `ui_in[7:0]` | Push data, bit 0 LSB |
| `uio_in[0]` | Push request |
| `uio_in[1]` | Pop request |
| `uio_in[7:2]` | Ignored |
| `uo_out[7:0]` | Registered pop response, bit 0 LSB |
| `uio_out[1:0]` | Always zero; these pins remain inputs |
| `uio_out[2]` | Registered response valid |
| `uio_out[7:3]` | Occupancy 0–16, **pin 3 LSB** |

All 24 UI/UO/UIO pin descriptions are declared in `asic/declaration.ml`.
`clk` connects directly to the core clock, `ena` to enable, and `!rst_n` to
**synchronous** clear. Inputs and reset must be synchronous to `clk` and stable
across its rising edge. There is **no implicit reset synchronizer**. Apply a reset
edge before use, including when disabled. Queue reset takes effect only at that
edge, while the output mask is combinational: `uo_out` and `uio_out` are zero
whenever `!(ena && rst_n)`; `uio_oe` is `0xFC` iff `ena && rst_n`, else zero.
Releasing a reset pulse that contained no clock edge reveals the old queue and
response. Masking alone is not a queue clear. Consumers decode empty/full from
occupancy 0/16; the explicit core flags and accepts remain covered by core tests.

## ASIC analysis assumptions

The declaration selects **TT6x4 / IHP SG13 CMOS5L**, LibreLane **Hardening**, and
`Tt_cmos5l.overrides ()`. It explicitly selects default resource policy **Flops**.
The FIFO's ordinary registers are not registered `Single_port_ram` resources:
the resource inventory is intentionally empty, not an inventory of 128 RAM bits.

* One `clk`, **48 MHz**, period approximately **20.833333 ns**.
* Inputs `ui_in`, `uio_in`, `ena`, `rst_n`: **min 0 ns, max 1 ns**.
* Outputs `uo_out`, `uio_out`, `uio_oe`: **min 0 ns, max 2 ns**.

These are fixed **specimen analysis assumptions**, following the library example's
0/1 ns input and 0/2 ns output convention, with every nonclock port covered.
Explicit zero minimums allow earliest-change/hold analysis rather than omitting
minimum constraints. They are not measured board timing, a reset CDC solution,
or evidence of physical timing/area/DRC acceptance. The library supplies reference
target revisions and geometry; pure resolution checks their structure without
opening or verifying external files. Those target references do not pin this
consumer's OCaml dependencies. No dependency lock or source revision is invented.

## Standalone bundle emitter

The Dune executable has this exact interface (both options required):

```sh
OCAMLPATH="$ASIC_LIBDIR${OCAMLPATH:+:$OCAMLPATH}" dune exec bin/emit_bundle.exe -- \
  --source-root /absolute/path/to/consumer-source \
  --output-dir /absolute/path/to/new-or-empty-bundle
```

The built `_build/default/bin/emit_bundle.exe` is also directly invocable with
the same flags. The source root supplies provenance and declared input bytes;
it does not rebuild the executable. Use an executable built from the matching
sources. The explicit root allows fixture-based acceptance to supply a
synthetic committed source checkout without altering the actual project checkout.

The emitter declares the project, resolves Implementation through the public
hardened boundary, elaborates Simulation separately, then calls `Bundle.render`
and `Bundle.write`. The library owns RTL/config/SDC/metadata/manifest emission and
provenance. Success prints one JSON line:

```json
{"identity":"<bundle SHA-256>","output_dir":"<requested path>"}
```

Failures print the library diagnostic plus source-provenance guidance to stderr
and exit 1; missing CLI arguments exit 2. Bundle output must be new or empty;
existing files are not overwritten. A write failure may leave partial output.
Rendering requires a source checkout with at least one commit. **This project's
current no-initial-commit root cannot emit a normal bundle.** The emitter does
not create a commit or fabricate a revision to bypass that requirement.

The explicit `Declaration.source_inputs` inventory is:

```text
dune-project
README.md
lib/dune
lib/controlled_fifo.ml
lib/controlled_fifo.mli
asic/dune
asic/tt_wrapper.ml
asic/tt_wrapper.mli
asic/declaration.ml
asic/declaration.mli
bin/dune
bin/emit_bundle.ml
```

This covers all consumer generation inputs, including wrapper, declaration,
metadata, build stanzas and emitter. Tests/model are not generation inputs;
dependency libraries are not copied into this inventory.

## Bundle and generated RTL acceptance

`acceptance/check_bundle.py` obtains the actual `Declaration.source_inputs` list
from `acceptance/export_trace.exe`, copies just those files into a temporary
source tree, and initializes a **synthetic local repository** there. It never
copies `.git` or `_build` and never commits the consumer checkout. The only fixture
commit has author and committer **`Bundle test <bundle@test.invalid>`**, message
**`baseline`**, and fixed dates. The script enforces identities in the subprocess
environment and per-command configuration, then verifies the recorded identities,
message, and absence of remotes. Inherited Git selectors are removed; system and
shared user configuration are excluded, and signing/hooks are controlled by
temporary test-local configuration. The fixture is removed after the test.

Bundle checks cover:

* Two independent emissions with identical relative paths and bytes, including
  the manifest; JSON response identity/output path agrees with the manifest.
* Exact emitted inventory, every emitted SHA-256, and each declared input's
  copied bytes/hash and tracked status.
* Exact top, TT6x4/CMOS5L target, Hardening operation, separate synthesis and
  simulation source lists, and intentionally empty registered-resource lists.
* Manifest/config agreement, all resolved settings (including the bundle-relative
  floorplan rewrite), generated source/SDC paths, 48 MHz clock and every min/max
  I/O delay, plus TT metadata and 24 pin descriptions.
* Tracked README and OCaml source comment edits change identity and are preserved
  byte-for-byte in copied inputs. The built emitter is unchanged; these probes
  test source provenance, not rebuilding modified logic. Emitted bundles are
  never hand-edited.
* Five actual nonzero failure cases: unborn source with absent/existing output,
  nonempty output refusal, and missing source with absent/existing output.
  Existing output bytes remain intact, and failed renders create no new output.

`acceptance/export_trace.ml` exports expected before/after state directly from
the existing pure list-based `Fifo_test_support`; Python and Verilog contain no
second FIFO model. `acceptance/replay.v` replays the full **7,330-edge directed
trace**, followed by **seed 20261012, 4,096 traffic cycles** plus reset/drain:
**11,429 total edges per source set** with the current toolchain. Icarus compiles
the synthesis source set and simulation source set **separately**, selecting the
same testbench top for both.

The bench checks registered response data/valid, occupancy pin ordering, low output
bits and OE before/after edges. Between edges it crosses reset/enable masks and
toggles ignored upper inputs, then checks that unmasking reveals unchanged state.
Directed coverage includes old-head full replacement, empty no-bypass, disabled
edges, synchronous reset priority, overflow/underflow and pointer wraps. Comparisons
use case-inequality to reject X values, except unspecified pre-initial-reset state.
Failures exit nonzero with trace index, phase, inputs, expected and actual output
bytes. Each compiled source set must also **reject a deliberately corrupted
expected response** at trace index zero; a successful negative run fails acceptance.

### Evidence and remaining limits

The independent `dune build @all`, forced ordinary tests and strict acceptance
passed with the development provider path shown above. Core and wrapper Cyclesim
each passed 7,330 directed plus 20,017 seeded/reset/drain edges (20,000 traffic
cycles); public resolution passed. Both generated RTL source sets passed 11,429
edges and each rejected the negative oracle. Bundle checks passed with two tracked
edits and all five failure cases.

This is deterministic functional RTL simulation, not a gate-level timing test or
formal proof. Bench delays allow combinational settling and do not model board
setup/hold or metastability; the 48 MHz and I/O constraints are analysis assumptions.
No synthesis, physical EDA, PDK validation, area, timing closure or DRC acceptance
has been run. Synthetic fixture revisions establish test provenance only, not a
release revision for this consumer. The real checkout still needs a user-created
initial commit before normal emission, and a committed dependency pin/lock remains
absent. Acceptance selects a local development provider explicitly; it does not
establish reproducibility across unpinned provider/toolchain revisions.
