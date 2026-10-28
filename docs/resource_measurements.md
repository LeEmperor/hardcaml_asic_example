# PT.5b resource measurements: independent example acceptance

## Status and boundary

**Installed public-provider acceptance completed 2026-10-27.** Final focused
receipt: `acceptance/resource-measurements/installed-final/receipt.json`, **15 passing
tests, zero failures/errors/skips**. `closeout-final.json` verifies focused results,
full example-suite/FIFO logs, identities, preservation and archive hashes.
The earlier `installed-02` and `closeout-01` remain unchanged but are superseded
by corrected A/B source recapture after independent review.

C owns `scripts/check_resource_measurements.py` and the new
`acceptance/resource-measurements/` capture and receipts. This continues
[`resource_realization.md`](resource_realization.md); the existing 20-test PT.5
acceptance is historical schema-1 acceptance, not PT.5b acceptance.

The implementation contract is
`../hardcaml_asic/docs/development/resource-measurements-plan.md`. A owns physical
measurements and schema-2 integration; B owns sampled timing/electrical links.
Both early handoffs appeared during capture; their completed integrated versions
were read before provider capture: `resource-physical-handoff.md` and
`resource-timing-handoff.md`. The capture satisfies B's requested raw layout,
including stage-53 input netlist, root preflight and full stage-56 metadata.
Assertions consume the final ASIC-owned schema-2 contract.

## Executed capture checks

`acceptance/resource-measurements/accepted-live-01/capture.json` records **333 files,
111847065 bytes**, with source/destination digests recorded at capture time.
`acceptance/resource-measurements/raw-01.json` records **4 passing tests, no
failures/errors/skips**. All 276 historical files, application configuration and
existing provider-current symlink targets/timestamps remained unchanged.
Checks verify every retained byte against its original source, complete historical
base preservation, accepted run identity, placed geometry/gross-bbox arithmetic,
and selected original timing path rows plus available unit declarations.
These four tests are raw evidence checks, distinct from later public acceptance.
That initial phase performed no build or provider capture.

Generated unit `.lib` files are **plaintext ASCII Liberty**, retained unchanged.
`Timing_report_units` parses plaintext; no gzip decoder is involved. Metadata may
contain stale state metrics; only actual post-route reports provide the sampled
observations.

**Encoding correction — 2026-10-27:** the earlier gzip-without-extension claim
was incorrect. A file-reading tool's binary-file refusal was not evidence of
compression. Direct Python binary inspection of all three original and captured
unit libraries found identical bytes beginning
`6c 69 62 72 61 72 79 20 28 74 74 5f 75 6d 5f 70` (`library (tt_um_p`),
not gzip magic `1f 8b`. Fast/slow/typical library sizes are respectively
**40188 / 40188 / 40187 bytes**. The three stage-56 SDFs are also identical
original/captured ASCII text, beginning `28 44 45 4c 41 59 46 49 4c 45`
(`(DELAYFILE`), with sizes **138638 / 138601 / 138636 bytes**. None of the nine
captured `.lib`/`.sdf` files has gzip magic; the compression claim was not a
confusion with compressed SDFs in this capture.

This correction supersedes the earlier descriptive claim and the raw verifier's
misleading comment about gzip unit libraries. Its gzip branch is conditional on
actual magic bytes and was not exercised by these libraries; the tests assert
unit declarations, not gzip encoding. Synthetic gzip **report** negatives remain
intentional tests of unsupported report bytes, not claims about native encoding.
The original capture/research receipts contain no gzip/encoding assertion and
remain unchanged, as do all raw bytes, scripts, tested-script snapshots and
acceptance receipts. No provider recapture or broader test repeat was needed.

## Raw evidence capture

Exact original execution:
`_flow_results/sram-physical/runs/20261025T034710180883Z_be961b2c/`.
Run `be961b2c95f74c81ad6af81ca4d2b269`, build
`fa38d9064dffdf2ec1578c79c2e8890eba81bf704af460e85fcc6031b707d53c`,
completed full. Failed executions sharing the build identity are not substitutes.

The new capture copies the complete `acceptance/sram/physical-p4` tree and adds:

- Entire `flow/56-openroad-stapostpnr/`: three corners' max/min/check reports,
  scalar reports, logs, config/state/commands and generated unit libraries/SDFs.
- Contained inputs named by STA input state: actual netlist, SDC, DEF/ODB, SPEF,
  powered netlist/header and historical input SDFs. Input-state metrics and old
  input SDFs are not post-route completion measurements.
- Actual SDC and macro blackbox named by STA logs, unchanged in `bundle/`.
- Floorplan producer metadata/log/metrics for gross core/die bounds.
- Live run/preflight/results/manifest copies under `capture-origin/`.

All source bytes are copied unchanged, with explicit source-to-destination hashes.
The original absolute references remain historical data. No external current PDK
models are discovered or copied; recorded model references differ from retained
verified model bytes. No new producer record, original hash rebinding or EDA occurs.
IR voltage files are outside this slice.

## Independent oracles asserted through public APIs

Geometry: exact `program` / `hc_resource_7_program` /
`RM_IHPSG13_1P_256x16_c2_bm_bist`; 1000 DBU/µm; DEF placement `(40000,81000) N`,
R0; LEF origin zero; width/height 236.8/118.78 µm; bounds
`[40,81,276.8,199.78]` µm; footprint **28127.104 µm²**.

Complete DEF plus bound LEF classes must yield separate rectangle sums:

| Scope | Count | Area, µm² |
| --- | ---: | ---: |
| Nonspacer | 389 | 4793.6448 |
| Spacer/fill/decap | 68539 | 866655.4176 |
| Macro | 1 | 28127.104 |
| All components | 68929 | 899576.1664 |
| Nonspacer + macro | 390 | 32920.7488 |

Gross core bbox `[2.88,3.78,1286.4,706.86]` gives **902417.2416 µm²**;
die bbox `[0,0,1289.28,710.64]` gives **916213.9392 µm²**. Assertions
calculate ratios from independently asserted numerators/denominators, using
precision-aware comparisons: macro/core ≈ 0.03116862434,
nonspacer+macro/core ≈ 0.03648062923, all-components/core ≈ 0.99685170554.
These are component rectangle sums over gross rectangles, not geometric unions,
usable placement sites, routed occupancy or a derivation of native utilization.
Halo, routing/bridges and nearby repair cells do not belong to macro footprint.

Sampled post-route report oracles (ns; reported load pF):

- Slow max: macro `A_DOUT[11] → uo_out[3]`; arrival 7.336773,
  required 18.583334, slack 11.246561; output slew 0.067838, load 0.004815.
- Fast min: `_203_/Q → macro A_ADDR[6]`; arrival 0.949038,
  required 0.725504, slack 0.223533; input slew 0.167545; blank Cap stays absent.
- Clock observations retain launch/capture role and cannot create a data link.
- Fast analysis label `nom_fast_1p32V_m40C` is distinct from the loaded SRAM
  model `fast_1p32V_m55C`; retain both without temperature relabeling.

The original curated snapshot has no `56-openroad-stapostpnr` reports. Its global
slack and zero slew/cap counts cannot supply resource timing/electrical links.
Sampled path points do not establish exhaustive coverage, per-pin compliance
limits/margins, timed SRAM conformance, resource power, IR/EM or flop ownership.

## Executed installed acceptance

After A/B completion, captured with
`scripts/asic_dependency.py --store .dev/asic-pt5b refresh --source
/home/wayne/devel/jane/hardcaml_asic --mode development --jobs 6` in the existing
5.2.0+ox environment, using a private captured source/build. Record source and
executable digests from that actual capture, not the moving checkout.
Example Dune uses `_build_pt5b` and explicit `-j6`, serialized. Any ASIC checkout
Dune uses shared `flock /tmp/opencode/asic-pt5b-build.lock` and explicit `-j6`.
All nested builds count within C's six-job allocation. Existing provider pointers
and application configuration remain intact; no Workbench operation is involved.

Isolated generation: `.dev/asic-pt5b/generations/4848a66eeda54751b12d645ee9bcd5c4`.
Observed ASIC base: `e46bfd7609e0b119ad74a8b412a3e866da5297de`.
Captured source SHA-256:
`03b13eb7dd2b2918594754c19b41cbc5fe5042f309a9f2f91eae221b6aed4f4f`.
Provider executable SHA-256:
`63657a8d4f51fb4be8249498357515cc2bd9e417ecd270538a9e7000855cf1f4`.
Installed API consumer SHA-256:
`edb23745eb57f295a9c7c05b9b87ad3f8e44a14ef7e25968359b6795a305219f`.
The dispatcher hash above is unchanged across captures; the final native
resource-inspection companion is
`84e2c061cf9aa45ee1fc2c232481ab0268a6555d8196f4340cbb13a8ee167ac9`.
`provider-final-binaries.json` records every installed binary's hash, bound to
the focused receipt and final generation.
This records dirty development bytes, not historical producer authentication or a
clean-source/P6 stamp. Closeout's read-only source observation matches the moving
checkout to this tested snapshot. Further corrections require new capture/build/
acceptance receipts.

Exercised CLI/library agreement, validation, full source replay, collection/report
and archives with no tools available. Both original physical-p4 and augmented
capture yield exact geometry, class sums and six ratios. Original snapshot timing
remains unavailable. The augmented capture yields **186 sampled resource-linked
paths / 372 macro electrical points, zero diagnostics**. Units/roles/master
ownership and each path's run/build/stage/report span are asserted. Fast −40°C
analysis and −55°C recorded SRAM model remain separately visible; external models
are not advertised as retained bytes.

The original strict schema-1 assertion at
`acceptance/resource-realization/installed-final/037.stdout` validates and
source-replays against original physical-p4. For archive compatibility the frozen
PT.5 provider emits genuine schema 1 over a disposable staged copy; the new
provider validates/replays it. Report renders fresh schema 2 in memory while stored
schema-1 results stay unchanged. Actual tar bytes preserve all **56** advertised
schema-1 references; the schema-2 archive verifies all **76** references.

Disposable staging copies the complete bundle/flow, places retained metrics/GDS,
runtime scripts and synthesis JSON at ordinary run paths, and explicitly relocates
the run's bundle path. Mappings/new run digests are recorded. No missing synthesis
stat is fabricated; collection's global result is not a replacement for historical
accepted global results. Report tests preserve retained global results in copies
while adding freshly inspected resource evidence.

### Independent negatives and changed-value checks

Checker/run hash-rebound negatives reach semantics for wrong/duplicate/missing
instance/master, wrong DBU, rotated/moved geometry, malformed DEF, bound LEF
class/size/origin conflicts, zero core denominator and native count disagreement.
Missing optional LEF yields unavailable exact sums while proved geometry remains
available. Ordinary unbound DEF tamper separately fails hash integrity.

Malformed/near-prefix/wrong-master/clock-pin paths, truncated/nonfinite reports and
missing/conflicting units cannot create resource links. Contradictory run/input
netlist/producer/log corner fails final evidence with CLI 1 rather than silently
passing optional attribution. Strict wire validation rejects false geometry
ownership, gross-area units, electrical compliance and timing stage.

Changed raw slew/load **0.081234 ns / 0.006321 pF**, required time **6 ns** and
signed slack **−1.336773 ns** with `VIOLATED` status are parsed and source-replayed.
Macro retention still passes: negative timing is valid measured evidence, not a
fabricated retention failure. Varied actual gross core bounds change ratios as
expected. Coherent timing required/slack and core bounds/area/ratio forgeries over
unchanged hashes pass shape validation but fail source replay. Stored timing
forgery makes report reject and archive refuse publication. These disposable
mutations are diagnostic, not newly qualified geometry or STA.

`installed-01` honestly records **5 assertion failures + 1 error across 10 tests**:
the harness expected CLI 0 instead of 1 for provenance contradictions, old-schema
report rendering instead of fresh schema 2, and retained `MET` on its negative
slack fixture. Correcting those produced passing `installed-02`; C made no ASIC
source workaround. Each passing run freezes `tested-script.py` and retains raw
command stdout/stderr, exits, mutation digests and structured outcomes.

After focused acceptance, serialized `dune runtest --build-dir _build_pt5b -j6
--force .` passed with explicit isolated-provider routing. Logs include unittest
groups **11 + 24 + 21**, directed/seeded FIFO/wrapper, three memory replay modes,
bundle/CLI and synthesis/simulation RTL replay with corrupted-response rejection.
Standalone `scripts/test_flow_emit.py` passed **5** FIFO-emission tests. Both were
rerun on the corrected provider (`suite-final` / `fifo-final` logs). Exact commands,
logs and FIFO/memory executable identities are in `closeout-final.json`.

All **276 historical files**, augmented capture bytes, application configuration
and pre-existing provider selections remain unchanged. Capture/build used private
sources; example Dune was explicit `-j6`. No ASIC checkout build/edit, EDA,
Workbench action or checkout Git mutation was performed by C. Full-suite bundle
tests use disposable synthetic Git fixtures. Remaining limits: sampled
coverage, no per-pin compliance limits/margins, no timed SRAM/IR-EM/resource-power/
flop-ownership qualification, and unavailable historical executable authentication.

### Final independent-review regressions

Read the completed/frozen A/B handoffs before recapturing. The final 15-test run
passes all earlier acceptance plus four independent review regression groups:

* Remove the actual primary data-arrival marker from an original min path, with
  and without its true macro data endpoint. Only the valid max path remains;
  min-report diagnostics are explicit, and no `A_CLK` point acquires data role.
* Put otherwise valid unit declarations only inside a nested Liberty cell:
  no timing/electrical links are fabricated. Empty, garbage and gzip min-report
  bytes produce diagnostics while retaining the valid sampled max path.
* Remove the macro LEF while contradicting known standard-cell native area,
  and remove the standard-cell LEF while contradicting independently proved macro
  area. Both reject even with partial exact coverage; truthful failed observations
  remain source-replayable.
* Hash-rebound LEFs with duplicate direct SIZE after a closed PIN, unclosed PIN
  and mismatched nested PORT reject; a checker/run-rebound DEF with the prefix
  terminator `END COMPONENTS_WRONG` also rejects semantically.

Final real evidence remains exactly **186 paths / 372 points**, zero diagnostics,
and the exact area/ratio oracles above. No new harness failure occurred on the
corrected capture. A/B's 56/73 feature cases cover additional parser/budget edges;
C does not count those provider-owned tests as independent example acceptance.

Final acceptance and closeout verify earlier `installed-02`, `closeout-01`, all
333 raw capture files and the original capture receipt remain unchanged. The
276 historical files and protected app/configuration/provider pointers still
match the original capture inventory. Only the isolated PT5b current pointer was
advanced. The approved application provider remains explicitly PT.5.
