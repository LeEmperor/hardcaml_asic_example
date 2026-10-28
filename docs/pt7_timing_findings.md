# PT.7 C real-tool findings for A/B/coordinator

## Final native disposition (round r3)

**A-REAL-1 and A-REAL-2 are closed for the tested final candidate.** Renderer
`9c53a5b75313adacd979ea5b559fd17ad0c51d2961c4df6dc0a41813a88d25d2`, provider
generation `74e9a52b43a14c69bff2763325b39522`: both fresh actual bit/scalar SDC
loads complete on OpenSTA 2.7.0, as do buffer and Q/source output-tap controls.
All intended clock/data/reset graph negatives fail before application against
passing baselines. See [pt7_timing_final.md](pt7_timing_final.md) for identities,
commands and remaining qualifications. The reports below describe original
failures in superseded captured providers and remain historical reproducers.

## A-REAL-2: top Pin's direct net is NULL; connected internal net is on its Term

2026-10-28 correction recapture: `06ac3f2956fb4273a822b127f41194f1`, source
SHA-256 `c46cc8a7ca0f9296e708551ca60539d36bbb402920262f4a3f758c7e72f82f8c`.
Fresh bit bundle `088166e58491413f228eee7bf4ab0e03fda160dbd02e70b53e47802ed32dd460`.
Native attempt `acceptance/timing/sta-bit-r2/` fails before application with:

```
mapped clock for capture_first source: disconnected/null net
```

The corrected renderer converts Port to a real top-level Pin successfully, but
then uses `get_nets -of_objects` on it, which calls `$pin net`. In the actual
standalone OpenSTA 2.7.0 network, this is the external side of the top-instance
boundary and is NULL. The internal design net is on the Pin's Term:

```
set port [lindex [get_ports -quiet [list clk]] 0]
set pin [::sta::get_port_pin $port]
get_full_name $pin                  -> clk
get_nets -of_objects $pin           -> NULL
$pin net                           -> NULL
$pin term                          -> non-NULL Term
[$pin term] net                    -> non-NULL Net
```

The same native results occur for `rst_n` and `ui_in[0]`. Reproducer:
`python3 -B timing/probe_port_net.py --label NEW_LABEL`; retained actual script,
inputs/SDC and output are `port-net-probe-r2*`. The probe prints the pinned native
`get_nets` procedure body as well. No emitted SDC or library source was patched.
Request A to use a checked Term-to-internal-Net conversion for top-level source
connectivity and its input-driver cache, then coordinate B renderer replay and a
new capture. Native negatives must reject for their intended mutated
connectivity, not merely this common source conversion failure.

The first exploratory OpenROAD probe (`port-net-openroad-r2*`) stopped because no
technology was loaded; its native ERROR and nominal zero process exit are retained
and it is not acceptance. A follow-up loads only tech/cell LEF to investigate
linked timing-network behavior; this is no placement or routing allocation.
That follow-up (`port-net-openroad-r2b*`) reproduces the same NULL Pin.net and
non-NULL Term.net results, and the unchanged SDC fails with the same diagnostic.

## A-REAL-1: emitted bus-port lookup fails on OpenSTA 2.7.0

Status: **open in captured provider**; reported during C acceptance. No library
source or emitted SDC has been patched by C.

Captured provider generation `da135e7054a3454fa0d822e86d0973bc`, source snapshot
`fab4b4a6d46ca47cf9ee721b16df70081dbf5590f42ae8938e17391c6acc4b43`.
Fresh public bundle identity
`869cb3fd18ae76c83964fa93f31b9643a628595d917e522ce820c5bd47311b30`.

Reproduce from the example checkout:

```sh
python3 -B timing/real_tools.py audit --label NEW_LABEL \
  --bundle acceptance/timing/synth-01-bundle \
  --synthesis acceptance/timing/synth-01
```

Original attempt: `acceptance/timing/sta-01/` and `sta-01-launch/`. Exact generated
SDC hash `95a86202f9016c0afe78686bd79cda9427d3fe4904a496a18e3aa3ef59c218e6`.
All five exact anchors and their Q/D/RESET_B pins resolve, then `read_sdc` raises:

```
hardcaml ASIC timing intent: get_ports ui_in[0]: expected exactly one object, got 0
```

There are zero `applied` records and no complete record; process exits 1.

The generated `::hc_pt7::exact` uses `pattern` to backslash-escape brackets before
calling `get_ports`. In this actual OpenSTA runtime the raw bit spelling works
but escaped brackets do not. Native lookup reproducer is `timing/probe_bus.py`;
retained script/netlist/Liberty and launcher logs are `acceptance/timing/bus-probe-01*`:

```
get_ports -quiet {ui_in[0]}    -> exact ui_in[0]
get_ports -quiet {ui_in\[0\]} -> no objects
get_ports -quiet {ui_in*}      -> all eight bits
get_ports -quiet {ui_in[[]0[]]} -> no objects
```

Request A to qualify exact port queries against the real OpenSTA matcher while
retaining cardinality/full-name checks, regenerate with its public API, and
coordinate B's SDC replay renderer. Synthetic Tcl object fixtures did not catch
this tool-semantic difference. C can recapture/re-emit/retest a corrected provider.

For continued independent bounded acceptance, C will also exercise a scalar
asynchronous source via the same public API, using a separate fresh bundle. This
does not qualify the failing bit-source subset.
