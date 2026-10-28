# PT.7 corrected-provider native run: new blocking source bug

**Historical r2 failure report.** Round r3 subsequently completed actual native
bit/scalar acceptance and closed A-REAL-2. Latest results and exact identities:
[pt7_timing_final.md](pt7_timing_final.md). The r2 failure bytes remain unchanged.

2026-10-28, correction round r2. **Both fresh bit and scalar native audits failed
before validation/application. Corrected-provider acceptance is blocked by
A-REAL-2, not complete.** The prior scalar success remains historical evidence
for its original provider only; it is not reused as corrected acceptance.

## Actual capture, emission and synthesis

Read the updated A/B ready handoffs, then executed the isolated capture with the
shared ASIC lock, switch `5.2.0+ox` and nested explicit six-job Dune limits:

```sh
python3 -B timing/record_command.py --output acceptance/timing/capture-02 \
  --timeout 1200 -- opam exec --switch=5.2.0+ox -- \
  flock /tmp/opencode/asic-pt7-build.lock \
  python3 -B scripts/asic_dependency.py --store .dev/asic-pt7/provider \
  refresh --source /home/wayne/devel/jane/hardcaml_asic --mode development --jobs 6
```

Generation: `.dev/asic-pt7/provider/generations/06ac3f2956fb4273a822b127f41194f1`.
Observed base: `e46bfd7609e0b119ad74a8b412a3e866da5297de`.
Captured source SHA-256:
`c46cc8a7ca0f9296e708551ca60539d36bbb402920262f4a3f758c7e72f82f8c`.
Receipt SHA-256:
`d23dc2910ca6e4e436e9c2e501175ec43dce1dc81488895de0e2b8c265068d08`.
The installed source files **exactly match A's published final correction hashes**:

* `timing_tcl.ml`: `55349fe8b06c11111bdb0027a90b1949b03c732a9baa618a7bbe895220a98902`
* `timing_intent.ml`: `514f4e47c8723fe770a098fa1996a5cfab928d7f917f535d1ae1ad806eded6bc`

Emitter SHA-256: `01a6f04c7e96d7fc5f4b7adfd31a99b7e23d4a6c6158281f92ccdbb8d4b5bd2c`.
Corrected native inspector SHA-256:
`c8fef497c11ea5ede6e8a5a0599f8f9c1bb5f526c5a6be9aa5276951213d8973`.
All installed binary identities and actual installed A sources are retained in
`acceptance/timing/closeout-r2/`.

`emitter-build-05` uncovered an owned-example packaging bug: Dune scanned the
retained source snapshot in `closeout-01/consumer-sources/dune` and saw a duplicate
library. Added new `acceptance/timing/dune` with `(data_only_dirs *)`; no old
snapshot was edited. `emitter-build-06` then passed using:

```sh
python3 -B timing/record_command.py --output acceptance/timing/emitter-build-06 \
  --generation .dev/asic-pt7/provider/current -- \
  opam exec --switch=5.2.0+ox -- \
  flock /tmp/opencode/example-pt7-build.lock \
  dune build --build-dir _build_pt7 -j6 timing/timing_cli.exe
```

Fresh `timing_cli emit` / `emit-scalar` created `bundle-bit-r2` / `bundle-scalar-r2`
under `.dev/asic-pt7`. The full public copies are retained as
`synth-bit-r2-bundle/` and `synth-scalar-r2-bundle/`:

| Identity | Bit source | Scalar source |
| --- | --- | --- |
| Bundle identity | `088166e58491413f228eee7bf4ab0e03fda160dbd02e70b53e47802ed32dd460` | `d815eda1cdf003e453156301f7405eec387a53434ca49971738e4752a16a26a4` |
| Manifest SHA-256 | `1811bda3c47b4dbbab8906cf0d8884c46822c5bdfd60429d49a824d708bc2bcc` | `a2f25e86717dd6481f5d1bee7ebf3a7b6a7c0fa14f5e5adaa10349aefc89a0cf` |
| Emitted SDC SHA-256 | `7222f9fca112ad31fe053e2d24b97a5d0900b7bdbfd1622a1d4a128f30574753` | `5e7c3ab7c4649cc680c419e65bc4e59003dd3f4b407997dd3b3d1cc525d65fb2` |
| Mapped Verilog SHA-256 | `d3858042fe1672eb9ba2fb97e7deaacf30b80385dc719ecde9d262c29d82f132` | `8d6459a26eda8a65c1a9d729ff2031cb675295f8449e5421f446e30822984e0b` |

Both **actual Yosys synthesis runs passed**. Their inventories assert five distinct
`sg13cmos5l_dfrbpq_1` stages, exact Q nets, chain D connections and actual mapped
primary CLK/reset connectivity. RTL and Liberty/script/input hashes are retained.

## Actual native failures and reproducer

Executed sequentially (new output names required for reruns):

```sh
python3 -B timing/real_tools.py synth --label synth-bit-r2 \
  --bundle .dev/asic-pt7/bundle-bit-r2
python3 -B timing/real_tools.py audit --label sta-bit-r2 \
  --bundle acceptance/timing/synth-bit-r2-bundle \
  --synthesis acceptance/timing/synth-bit-r2
python3 -B timing/real_tools.py synth --label synth-scalar-r2 \
  --bundle .dev/asic-pt7/bundle-scalar-r2
python3 -B timing/real_tools.py audit --label sta-scalar-r2 \
  --bundle acceptance/timing/synth-scalar-r2-bundle \
  --synthesis acceptance/timing/synth-scalar-r2
```

Both OpenSTA 2.7.0 processes exited **1**, reading the **unmodified emitted SDC**:

```
mapped clock for capture_first source: disconnected/null net
```

Both have one `begin` event and zero validated/applied/complete records. No native
downstream reports were reached; none were fabricated or borrowed from older
audits. Raw driver/receipt/log/process results and exact inputs remain in `sta-*-r2`.

`port-net-probe-r2` demonstrates the cause on the exact pinned native runtime:
`sta::get_port_pin` returns a real Pin, but `$pin net` / `get_nets -of_objects`
returns `NULL` at the top boundary. `$pin term` is valid and `[$pin term] net`
returns the connected internal Net. This occurs for `clk`, `rst_n`, `ui_in[0]`.
The generated input-net cache has the same issue as `port_net`.

OpenROAD diagnostic `port-net-openroad-r2b` loads tech/cell LEF and reproduces the
same result; this is not merely standalone-OpenSTA behavior. No placement/routing
was performed. Earlier `port-net-openroad-r2` omitted tech and emitted `ORD-2010`;
its nominal process exit 0 and actual ERROR are preserved, not called success.

Full source report and native commands: [A-REAL-2](pt7_timing_findings.md).
No emitted SDC, library source or native command implementation was patched or
overridden to make the audit pass. A needs a checked top Pin → Term → internal
Net operation in source tracing/cache, followed by coordinated B replay recapture.

## Prepared checks and explicit skips

`timing/connectivity_cases.py` prepared **17** mapped-netlist fixtures from the
new bit product, with exact new hashes and unchanged SDC in
`connectivity-bit-r2-prepared/`: direct positive, buffered clock/data/reset
positive, wrong-input/constant/disconnected/inverted clock/data/reset negatives,
interstage-rewire negative, eight-buffer positive and nine-buffer negative.
Its runner requires the direct positive to pass before any negative can qualify.
These fixtures are **prepared, not run or passing**; a common baseline source
failure must not be counted as intended negative rejection.

`timing/check_semantic_evidence.py` is ready to exercise B's complete-SDC prefix
binding, unsupported/minimal/full-manifest closure, fatal/ANSI diagnostics and
line budget, plus nonfatal INFO/object-order controls. It also requires an actual
valid/unavailable baseline before running mutations. This suite is **not run**
because no corrected native positive audit exists yet.

A targeted actual B CLI negative did run: the corrected installed provider
inspecting the unchanged old `sta-scalar-02` exits **2** with `SDC timing intent
differs from library serializer replay` (`inspect-old-scalar-with-r2/`). Thus the
old audit is not silently relabelled as current acceptance. The intended successful
native inspection still must be exit **1 / unavailable**, never passing coverage.

No unrelated broad example suite was repeated. Historical successes, failures
and limitations are retained. `closeout-r2/prior-evidence-verification.json`
verifies every file in the prior closeout checksum inventory remains unchanged.

## Resource and preservation policy

All builds: existing switch, `_build_pt7`, explicit `-j6` and example flock;
provider capture uses the ASIC flock and its private six-worker build. All native
tools serialized, explicit STA `-threads 1`, Docker one CPU / 4 GiB / 128 PIDs,
no network and read-only image root; default timeout 180 seconds. Same exact image
`sha256:d109140b8f17fc54f4fca998beb8124f4949404ec52e339eebd2250854a18b5a`.
P&R allocation/use is zero. No Git mutation, old evidence overwrite, app/provider
selection change outside the new PT.7 store, Workbench or Protemu change.
