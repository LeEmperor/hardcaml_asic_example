# Controlled FIFO ASIC specimen

An independent Dune project containing a fixed Hardcaml FIFO core, a consumer-owned
Tiny Tapeout wrapper, a shared Project declaration and CLI, repeatable
bundle acceptance, and PDK-free Cyclesim and generated-Verilog tests. This is a
**development specimen with an explicit consumer dependency record**.
It uses `core`, `hardcaml`, `ppx_jane`, `ppx_hardcaml`, `yojson`, and a selectable
development build of `hardcaml_asic` exposing the hardened `Resolved_flow.mli` and
the shared `Project.source_inputs`, `describe`, and `emit_bundle` API.
The project declares Dune language 3.17 and has been built with Dune 3.24.2 and
OCaml 5.2.0+ox. The record is not an opam pin. The installed
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

Run from this repository using an already available compiler, Dune, ocamlfind and
dependencies. First obtain and activate a compatible installed `hardcaml_asic`
provider: a normal opam installation (`opam install hardcaml_asic`, then
`eval "$(opam env)"`) suffices when it exposes the required Project API and provision
CLI. The finished consumer needs no ASIC library source checkout. The shared opam
package may currently expose an older API; for this development transition,
explicitly refresh a private installation from a selected checkout and activate it
before ordinary builds:

```sh
python3 scripts/asic_dependency.py refresh --source /absolute/path/to/hardcaml_asic --mode development
. .dev/asic/current/activate.sh
python3 scripts/asic_dependency.py status --json
dune build @all
dune runtest --force
dune build @acceptance-strict --force
dune exec test/fifo_test.exe -- --directed
dune exec test/fifo_test.exe -- --seed 42 --cycles 100000
dune exec asic_test/wrapper_test.exe
dune exec asic_test/resolution_test.exe
```

`db` can replace the plain build command if that local wrapper preserves the
activated environment. No sibling checkout path is assumed by the tool.

### Flow-tool bootstrap (separate from library development refresh)

After installing/activating the provider above, diagnose the selected flow-tool
root without changing it:

```sh
./bootstrap.sh --check --no-container
```

`bootstrap.sh` requires `hardcaml-asic-flow` on PATH and execs its `provision`
subcommand. The installed provider owns provisioning logic, locked versions and
option validation before provisioning. The wrapper neither installs nor refreshes
the provider. `./bootstrap.sh --help` forwards to provider help safely. Running
`./bootstrap.sh` with no arguments is an explicit request to provision.

Once host prerequisites are available, authorize actual provisioning by running:

```sh
./bootstrap.sh --python /absolute/path/to/python3.11
# Or ./bootstrap.sh when the provider's locked base interpreter is already available.
```

Provisioning `--python PATH` selects the **base interpreter for new virtual
environments**, not a flow run's virtual-environment Python. It must match the
provider's locked minor (currently 3.11) and supply `venv`, `ensurepip`, and
headless Tcl via `tkinter.Tcl()`; no graphical display is needed. There is no
fallback to another Python minor. Host Python/Tcl and Docker or Nix are separate
host prerequisites. Docker images and Nix stores remain in their external storage,
not under the selected root. The available local 3.12 tool environment lacks Tk
and does not meet the requested 3.11 prerequisite; this slice has not repaired it
or demonstrated actual provisioning. The current private provider installation
also awaits an explicit refresh/activation of the latest provisioning changes.

Root precedence is a later explicit `--toolchain PATH`, then nonempty `TOOLCHAIN`,
then the absolute `_flow_tools/` directory beside `bootstrap.sh`. For example:

```sh
TOOLCHAIN="/storage/my flow tools" ./bootstrap.sh --check --no-container
./bootstrap.sh --toolchain "../shared flow tools" --check --no-container
```

The wrapper keeps the caller's working directory; explicit relative roots (including
`TOOLCHAIN`) retain that meaning. Only the default root is project-relative.
`/_flow_tools/` is ignored here; ignoring any overridden location is its owner's
policy. The provider puts `tt/`, `pdk/`, LibreLane's `.venv/`, and the precheck
`.venv-precheck/` under the chosen root. `--check` changes nothing; `--offline` forbids fetching
(it is not a read-only mode); `--no-container` skips container-image provisioning
and checks, not TT/PDK/venv requirements. These and `--python` are forwarded without
consumer-side per-tool logic.

Project `describe` and `emit` below work independently of flow-tool provisioning.
For subsequent shared-CLI operations, pass the chosen root explicitly:

```sh
hardcaml-asic-flow preflight /absolute/path/to/bundle --toolchain "$PWD/_flow_tools"
hardcaml-asic-flow run /absolute/path/to/bundle --toolchain "$PWD/_flow_tools" \
  --runs /absolute/path/to/runs --stage synthesis
```

Replace that root when using an override. Sourcing the provider-generated
`_flow_tools/toolchain-env.sh` is optional; the wrapper exports nothing to the calling shell,
and these commands do not rely on `TT` or `FLOW_PY`. LibreLane venv autoactivation
is unnecessary: shared-CLI orchestration uses a separate host Python and selects
the flow interpreters from `--toolchain`. Preflight/run are separate user actions,
not bootstrap tests or evidence of physical EDA success.

Recorder-only bootstrap tests (no provisioning, downloads or nested Dune):

```sh
python3 scripts/test_bootstrap.py
dune runtest scripts --force
```

### Consumer dependency setup

`asic-dependency.json` records schema, package, repository URL and full revision.
Normal **recorded** refresh reads committed bytes at that revision from the
explicit local repository, ignoring working edits. It never fetches. The initial
revision is `1714764859274f80a9f5ad207421a04601824e99`; before recording it, the
read-only command below checked its committed public interfaces for
`Elaborated_project`, `Resolved_flow` and `?simulation_project`, plus its flow
installation stanza. Real refresh/build evidence is recorded below; this command
alone checked source interfaces under the earlier setup contract (historical command):

```sh
python3 scripts/asic_dependency.py validate-source \
  --source /absolute/path/to/hardcaml_asic \
  --revision 1714764859274f80a9f5ad207421a04601824e99
```

**Project API transition:** the recorded `171476...` revision does not yet expose
`Project.source_inputs`, `describe`, `emit_bundle`, and constructor `?source_inputs`.
The strengthened check now rejects that recorded API, including the historical
`validate-source` command above. Keep the record unchanged until its owner advances
it. During this transition, explicitly refresh **development** bytes with the new
API and re-activate. The recorded snapshot is still loaded for comparison, but
API requirements apply to the selected snapshot. `validate-source` remains a
read-only source check and reports `compiled: false` on success.

For this transition and local edits, explicitly select **development** mode:

```sh
python3 scripts/asic_dependency.py refresh --source /absolute/path/to/hardcaml_asic --mode development
. .dev/asic/current/activate.sh
python3 scripts/asic_dependency.py status --json
dune build @all
```

Development captures tracked files and relevant nonignored untracked files,
including deletions and safe internal file symlinks, excluding `.git`, `_build`,
`.toolchain`, `.dev`, Python caches and the selected store. Two capture comparisons
reject observed concurrent edits; this is not an atomic filesystem snapshot or a
clean-checkout claim. Builds use captured bytes in a private temporary directory.
Neither mode changes the baseline record, opam pins or shared source `_build`.
Missing dependencies/revisions and incompatible source fail with no provisioning.

The ignored `.dev/asic/` store contains `.owner`, `writer.lock`, `generations/<id>/`
and an atomically replaced `current` symlink. Each generation contains installed
`lib/`, `bin/hardcaml-asic-flow`, `receipt.json` and `activate.sh`. Installation uses
the final generation prefix; publication follows interface/runtime-file checks,
CLI `--help`, an exact ocamlfind resolution check and compilation of a tiny external
consumer using `Resolved_flow.t`, `Elaborated_project.t`, `Bundle.render`, and the
new Project constructor/inventory/description/emission signatures (including both
optional emission arguments), plus
a Dune executable link probe. Metadata pointing into the temporary capture is rejected.
The release build uses `-p` (which implies `--root .`) in the capture directory and
a relative `_build` directory so installed archive paths remain relocatable.
One writer holds a nonblocking store lock. Failures retain the previous selection;
old and failed generations are retained, with no automatic garbage collection.
An existing unowned store destination is rejected. Global `--store /absolute/path`
(before the subcommand) selects a fresh private store; source that store's
`current/activate.sh`. Global `--record PATH` selects another dependency record.
Symlinked store paths and colons/newlines are rejected.

**Re-source after every successful refresh.** Activation pins OCAMLPATH and PATH
to a specific generation, so an active shell stays on its prior generation until
reactivated. It removes known managed prefixes and preserves unrelated entries.
To explicitly retire the selected source's previous manual override, add
`--remove-source-build-override` to refresh; its exact
`SOURCE/_build/install/default/lib` path is recorded for removal on activation.
Without that flag, manual paths are preserved after the selected generation.
POSIX shell activation supports spaces and apostrophes in paths.

`status --json` is read-only and reports the published generation separately from
the caller's active-generation marker and OCAMLPATH, including an older active
generation, development override, captured differences from its observed base,
and baseline mismatch. Receipt facts describe refresh inputs, not today's checkout.
The snapshot checksum is **local bookkeeping, not P6.5 source stamping**; the CLI
reports unstamped in the validated installations. See the authoritative
[consumer dependency workflow](../hardcaml_asic/docs/development/consumer-dependency-workflow.md)
for scope.

PDK-free setup tests use injected build/install/compiler/CLI processes and
disposable Git fixtures with `Bundle test <bundle@test.invalid>` identities:

```sh
python3 scripts/test_asic_dependency.py
dune runtest scripts --force
```

All 16 setup tests also participate in ordinary `dune runtest`, using injected
processes without nested Dune calls. Real refresh runs its Dune consumer probe
before publication.

The strict alias requires both `iverilog` and `vvp` on PATH. Ordinary `runtest`
still runs bundle acceptance when either is absent, printing an explicit RTL
**SKIP**; it does not count that as RTL acceptance. Python 3 and Git are required
for the synthetic fixture. These commands use existing tools, without installing
dependencies. Both acceptance aliases consume Dune executable dependencies
directly and never invoke nested Dune builds.

### Source-breaking ASIC API migration

The public API now uses `Elaborated_project` (formerly `Build`) and
`Resolved_flow` (formerly `Resolved_build`). The resolved record field is
`.elaborated_project` (formerly `.build`), and `Bundle.render` accepts
`?simulation_project` (formerly `?simulation_build`). There are no compatibility
aliases: consumers must update source and recompile against the renamed provider.
This example uses the new names for both Implementation and Simulation elaboration.
The rename preserves persisted bundle keys, ordering and hashing; it does not
provide binary compatibility. Dependency selection is handled by the setup above.

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
24 pin descriptions, and empty resource inventories in both elaborated projects. It also
checks that a Simulation elaborated project is rejected by the implementation resolution
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

All 24 UI/UO/UIO pin descriptions are declared in `asic/project.ml`.
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
consumer's OCaml dependencies; the explicit consumer record above selects the provider.

## Project entry point and standalone CLI

`Fifo_asic.project ()` returns the generic `Hardcaml_asic.Project.t` declaration.
The façade also retains `Fifo_asic.Tt_wrapper` for wrapper tests. Inventory lives
in `asic/project.ml` and is passed to the generic constructor.

The Dune executable has these subcommands (both emit options required):

```sh
dune exec bin/project.exe -- describe
dune exec bin/project.exe -- emit \
  --source-root /absolute/path/to/consumer-source \
  --output-dir /absolute/path/to/new-or-empty-bundle
```

`describe` prints the shared `Hardcaml_asic.Project.describe` Sexp: local declaration
facts, **not a public Workbench provider schema**. It does not elaborate, inspect
Git, create output directories, or run EDA. No arguments or invalid commands exit
2 with usage; `--help` exits 0. There is no expensive default or legacy CLI shim.

The built `_build/default/bin/project.exe` is also directly invocable with
the same subcommands. The source root supplies provenance and declared input bytes;
it does not rebuild the executable. Use an executable built from the matching
sources. The explicit root allows fixture-based acceptance to supply a
synthetic committed source checkout without altering the actual project checkout.

The emitter creates `Fifo_asic.project ()` and calls `Hardcaml_asic.Project.emit_bundle`.
The shared API owns implementation resolution, default simulation elaboration,
rendering and writing. The library owns RTL/config/SDC/metadata/manifest emission and
provenance. Success prints one JSON line:

```json
{"identity":"<bundle SHA-256>","output_dir":"<requested path>"}
```

Failures print the library diagnostic plus source-provenance guidance to stderr
and exit 1; missing CLI arguments exit 2. Bundle output must be new or empty;
existing files are not overwritten. A write failure may leave partial output.
Rendering requires a source checkout with at least one commit. The owner's checkout
satisfies that prerequisite; real acceptance verifies its current revision using
read-only Git inspection and preserves dirty/untracked input statuses. A revision
alone establishes neither a clean working tree nor a dependency pin. The emitter does not create a commit or
fabricate a revision to bypass the provenance requirement.

The explicit `Hardcaml_asic.Project.source_inputs` inventory has 15 paths:

```text
dune-project
asic-dependency.json
README.md
lib/dune
lib/controlled_fifo.ml
lib/controlled_fifo.mli
asic/dune
asic/tt_wrapper.ml
asic/tt_wrapper.mli
asic/project.ml
asic/project.mli
asic/fifo_asic.ml
asic/fifo_asic.mli
bin/dune
bin/project.ml
```

This covers all consumer generation inputs, including wrapper, declaration,
metadata, build stanzas and emitter. Tests/model are not generation inputs;
dependency libraries are not copied into this inventory. `asic-dependency.json`
captures the consumer's dependency expectation, not proof of linked library identity.
Local refresh receipts and setup scripts are not hardware generation inputs.

## Bundle and generated RTL acceptance

For acceptance against the **actual checkout**, activate and build first, then use
a fresh ignored work directory (the following path is used for slice 3 evidence;
choose another fresh name when rerunning):

```sh
. .dev/asic/current/activate.sh
dune build @all
python3 acceptance/check_bundle.py \
  --emitter _build/default/bin/project.exe \
  --exporter _build/default/acceptance/export_trace.exe \
  --source-root /home/wayne/devel/jane/hardcaml_asic_example \
  --bench acceptance/replay.v --require-rtl --real-checkout \
  --work-dir .dev/emitter-checks/project-entrypoint-slice3
```

This mode performs only read-only Git inspection. It emits `first/` and `second/`,
compares complete trees byte-for-byte, checks every manifest file/input hash and
copied byte, and checks each input's actual Git status and the checkout revision.
`evidence.json` preserves those observations, including whole-checkout status.
The shared trace exporter and replay bench independently compile and simulate the
actual first bundle's synthesis and simulation RTL, including negative-oracle
checks. Traces and both compiled `.vvp` files remain alongside the bundles.

`acceptance/check_bundle.py` obtains the actual `Hardcaml_asic.Project.source_inputs` list
from `acceptance/export_trace.exe`, copies just those files into a temporary
source tree, and initializes a **synthetic local repository** there. It never
copies `.git` or `_build` and never commits the consumer checkout. The only fixture
commit has author and committer **`Bundle test <bundle@test.invalid>`**, message
**`baseline`**, and fixed dates. The script enforces identities in the subprocess
environment and per-command configuration, then verifies the recorded identities,
message, and absence of remotes. Inherited Git selectors are removed; system and
shared user configuration are excluded, and signing/hooks are controlled by
temporary test-local configuration. The fixture is removed after the test.

For before/after API compatibility, optionally supply a saved pre-migration
executable (kept outside the source tree) after verifying its trusted hash:

```sh
python3 acceptance/check_bundle.py \
  --emitter _build/default/bin/project.exe \
  --exporter _build/default/acceptance/export_trace.exe \
  --source-root . --bench acceptance/replay.v --require-rtl \
  --baseline-emitter /absolute/path/to/saved-pre-migration.exe \
  --baseline-source-root /absolute/path/to/saved-consumer-source \
  --baseline-inputs /absolute/path/to/saved-inputs.txt
```

The baseline uses its old
flags; the current executable uses `emit`. The fixture stages the union of both
inventories at one synthetic revision, restoring **only old-only paths** from the
saved source snapshot. Shared paths keep current bytes. Each bundle is inspected
against its own inventory. Comparison requires byte-identical synthesis RTL,
simulation RTL, config, SDC and info, and equal nonprovenance manifest facts.
Different inventories naturally have different manifests/identities. Repeated new
emission still requires whole-tree equality. For an old-CLI baseline with the same
inventory, omit both baseline source/inventory options; whole-bundle equality is
then also required. Ordinary and strict aliases need no baseline executable.

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

On 2026-10-12, slice 3 ran the normal managed refresh:

```sh
python3 scripts/asic_dependency.py refresh \
  --source /home/wayne/devel/jane/hardcaml_asic --mode development
```

It published `.dev/asic/generations/69a5db1892234a28b0884442ab0291f1`, with
`receipt.json` and `activate.sh` in that prefix. The observed provider base was
`82c0d7f7fbaa2d1796427de1037644946ceb2294`; captured snapshot SHA-256 was
`64b10f0e17e348105053f2f0c095d97bf2a8397a096b135b603c45ca43b2b6ce`.
Captured bytes differ from both the observed base and recorded snapshot.
The existing removal of the provider's manual `_build/install/default/lib`
override was carried forward. The refresh compiled the installed API and Dune
probes before publication.

After activation in a child shell, `ocamlfind query hardcaml_asic` and
`command -v hardcaml-asic-flow` selected that same private generation. Status
reported `active_is_published` and `active_library_path_is_first` true, with the
development/dirty/base-mismatch flags true. Running the same refresh command
with `--mode recorded` rejected the actual unchanged `171476...` record with
`incompatible Project.create API`, preserving the successful development selection.

Plain `dune build @all`, `dune runtest --force`,
`dune build @acceptance-strict --force`, and `dune exec bin/project.exe -- describe`
passed in the activated shell without a manual OCAMLPATH override. Core and wrapper
Cyclesim each passed 7,330 directed plus 20,017 seeded/reset/drain edges. Public
resolution, all 16 setup tests, and CLI purity/usage checks passed. Each generated
RTL source set passed 11,429 edges and rejected the negative oracle. Fixture bundle
checks passed with repeat whole-tree equality, two tracked edits and five failure cases.

The saved pre-migration executable at
`/tmp/opencode/project-api-baseline-k9wvcigz/emit_bundle.exe` was verified before use:
SHA-256 `739024f92ae88bf45d48e63ed67673b83a73c5fb4c5078db16efe8bbdcfe7cc1`.
The optional baseline command above passed with its sibling `consumer-source/`
and `inputs.txt`. All five generated artifacts and nonprovenance manifest facts
were equal; inventories differ (13 old inputs, 15 new), so this is not old/new
whole-bundle equality. Both RTL source sets also passed strict replay and negative
oracles. Real-checkout evidence uses the command and preserved directory above;
its `evidence.json` records actual dirty/untracked status rather than a clean-tree claim.
This README is a declared input and must be finalized before capturing that evidence.

The selected installed CLI's `hardcaml-asic-flow --version --json` reports package `0.1.0`,
`source.stamped=false`, state `unknown`, and null revision, inventory digest and
library-artifact match. Receipts are local selection evidence, not generator stamps.

This is deterministic functional RTL simulation, not a gate-level timing test or
formal proof. Bench delays allow combinational settling and do not model board
setup/hold or metastability; the 48 MHz and I/O constraints are analysis assumptions.
No synthesis, physical EDA, PDK validation, area, timing closure or DRC acceptance
has been run. Synthetic fixture revisions establish test provenance only, not a
release revision for this consumer. The owner's initial commit satisfies the
commit prerequisite for normal emission. The consumer dependency record selects
a provider revision; this acceptance does not establish reproducibility across
provider/toolchain revisions or authoritative P6.5 linked-artifact identity.
