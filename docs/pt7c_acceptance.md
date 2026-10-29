# PT7c independent example continuation

**Final reader correction recorded:** [LF-only R1b reader closeout](pt7c_reader_r1b_final.md)
replays the existing native-v2 execution with a separately captured corrected
inspector. The original producer/run identity is unchanged. No new EDA or bundle
emission was required; raw-CR semantic negatives now reject before tokenization.

**Latest status: completed bounded native-v2/coarse acceptance after review.** See
[reviewed native-v2 acceptance](pt7c_native_v2_final.md) for the current provider,
successful fresh run, public archive/restore, native controls and protection
receipts. The preliminary checkpoint below remains historical failed evidence.
The earlier [native-v1 success](pt7c_native_final.md) remains historically successful
and byte-preserved; current readers explicitly require recapture for that profile.

2026-10-28. C owns only new example scripts, documentation and
`acceptance/pt7c/`, `.dev/asic-pt7c/`, `_build_pt7c/`. Hardware/emitter changes
have not been necessary. Original tracked inputs, r3 histories and protected
old provider pointers are inventoried in `acceptance/pt7c/original-history.json`.
The initial example status was the four pre-existing untracked directories
`_build_pt7/`, `acceptance/resource-inspector/`, `acceptance/resource-measurements/`,
and `acceptance/timing/`.

## Early real qualification

See [live native findings](pt7c_native_findings.md). Actual native API probes,
diagnostics and counterfactuals are retained under new attempt names, including
failures. No old SDC was edited; old netlist/SDC/Liberty inputs were mounted
read-only. `scripts/pt7c_probe.py` records exact image, argv, limits and before/
after input hashes; checks require native completion, not process exit alone.

`scripts/pt7c_producer_probe.py --attempt producer-probe-01` qualified A's actual
literal producer early. Its receipt explicitly distinguishes source qualification
from final emitted-member/provider acceptance. Eight sequential native controls
preserve exact reports and negative hold. Parser/producer ownership stays in the
generic provider: `acceptance/pt7c/native_reader.ml` is only a pass-through adapter.

## Final fresh-flow procedure (pending final A/B provider)

Do not capture an in-progress provider as the final candidate. After the final
handoffs, use a **new attempt** for every invocation, including failures:

```sh
python3 -B timing/record_command.py --output acceptance/pt7c/capture-01 -- \
  opam exec --switch=5.2.0+ox -- flock /tmp/opencode/asic-pt7-build.lock \
  python3 -B scripts/asic_dependency.py --store .dev/asic-pt7c/provider \
  refresh --source /home/wayne/devel/jane/hardcaml_asic --mode development --jobs 6
python3 -B scripts/pt7c_flow.py build --attempt build-01
python3 -B scripts/pt7c_flow.py emit --attempt emit-01
python3 -B scripts/pt7c_flow.py run --attempt coarse-01 \
  --run .dev/asic-pt7c/bundle-emit-01
python3 -B scripts/pt7c_flow.py public --attempt public-01 --run EXACT_RETURNED_RUN
```

The public phase invokes real `timing-intent-inspect --kind coarse_run`, `collect
--stdout`, `report`, `archive --list`, `archive --output`, restores both retained
archives into a new directory, and reruns public readers. It hashes original run
files before/after to check reader immutability. Provider-defined evidence and
exact source association are authoritative; no recency search or local rerender
is used. Ordinary coarse synthesis runs first; no named execution or P&R.

All build/install/nested validation calls run switch `5.2.0+ox`, explicit six jobs
or fewer, under the designated checkout locks. Builds and EDA run sequentially
within C's six-job allocation. Native probes are single-thread/one-CPU with
explicit worker environment, memory/PID/time bounds and serialized tool lock.
The final provider is responsible for the coarse runtime's explicit CPU/worker
limits and serialized single-thread linked STA; receipts must confirm them.

Overall exhaustive exception-effect coverage remains unavailable. Native stored
scope and complete returned algorithm groups are separate supported dimensions.
Timing violations remain violations; bounded suppression is not exhaustive effect,
and reset-effect qualification remains unavailable. Final results will be appended
after actual completed execution; this procedure alone claims no acceptance.

## Executed integration checkpoint

The explicitly preliminary snapshot installed successfully in
`.dev/asic-pt7c/probe-provider/generations/ca45ad3ba4e9456880b177e5a753f5f5`.
Its receipt hash is
`86868912723ba49f8a23fc7775b2870aaec07c02e82024afd1e173d96efa3456`.
Capture's nested builds used `--jobs 6`; the fresh `_build_pt7c` emitter and
generic reader adapter built successfully under the example lock with `-j6`.
All corresponding argv/stdout/stderr/result records are retained.

Actual native baseline reader integration **failed**, with the native writer's
no-space backslash-newline command continuation parsed as `set_false_path -from`.
This is a generic-provider reader issue, not a reason to modify old SDC or
introduce a consumer parser. Additional real baseline forms needing qualification
are `set_timing_derate` and `[current_design]`; see the live findings.

Fresh public emission `emit-integration-01` succeeded. Actual ordinary public
coarse execution `coarse-integration-02` completed synthesis and automatically
attempted separate linked STAPrePNR in:

```
.dev/asic-pt7c/probe-runs/20261028T164800799130Z_44ded577
```

The native linked process **failed** because the wrapper reads `PT7_RECEIPT`
before sourcing LibreLane's `_TCL_ENV_IN`. Actual runtime API probes establish
the bootstrap requirement; all failed native inputs/logs/companion remain intact.
Public coarse inspection of that failed run executed, returning exit 1 with
explicit `status=failed` and `verdict=unavailable`. This is **not passing native
scope coverage**, final capture, or successful end-to-end flow acceptance.

Final provider capture is intentionally pending the A/B corrections/final handoff.
Successful-run public collect/report/archive/restore and final generic-reader
positive/negative suites have runnable continuation scripts but are **not yet
claimed as executed**. Failed-run public collection executed (exit 0), report
executed (exit 1), and archive correctly refused the failed run (exit 2); these
are retained as `collect-failed-integration-01`, `report-failed-integration-01`
and `archive-failed-integration-01`. No successful archive/restore is implied.
The early eight native source-producer controls completed; the expanded final
control suite adds hold-only, rise-only and extra-relation cases.

`preservation-integration-01.json` verified **10,398 original files** with zero
changes. `git diff --check` passed; example changes remain new PT7c files only.
P&R allocation/use remains zero. This checkpoint preserves failures and the exact
remaining blockers rather than promoting a successful synthesis to STA acceptance.
