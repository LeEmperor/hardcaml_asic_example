# PT7c final LF-only reader correction — durable C qualification

2026-10-28. **A-NATIVE-R1b is closed for the exact corrected inspector below.**
The retained native-v2 execution, prior restored evidence and standalone audit
replay identically. Raw-CR semantic negatives reject before tokenization. This
continuation performed **zero EDA launches, zero bundle emissions, and no design
rerender**. It does not attribute historical native execution to a newer reader.

## Two distinct tested identities

| Role | Durable identity |
| --- | --- |
| Original native execution provider | `.dev/asic-pt7c/provider/generations/4d4316e3a33942c2a577d6f55acaa34a` |
| Original execution receipt SHA-256 | `ec00d5619805de324201a23446a0dd5129eb2a8ef02713ed87bd5e1299809310` |
| Original source snapshot SHA-256 | `8d3fa9270712a47473c22615c2a7005d975b361db5f569dfbe8e911055ccbe89` |
| Original native run | `83a02bdcb4b34f22bbc03b0ec5223b41` |
| Original run-record SHA-256 | `19544cba877349511e055a2d74e9c84571f33490007f1a52f89bb0424850d2d6` |
| Executed emitted native-v2 producer SHA-256 | `8d886b2bde7e50f7781ef7f3f73bfdfa47a8d7beba947119dd66129a2d48b03e` |
| Corrected inspector generation | `.dev/asic-pt7c/reader-r1b-provider/generations/4c9ae1a7a50444179c8ab69469443c19` |
| Corrected inspector receipt SHA-256 | `24be25d1041477025792a92f0cca3268a85e2ce64f1650b6dbcf9e0a1f3de56a` |
| Corrected source snapshot SHA-256 | `5a6bd3664828e0d28c9b0ad3d7eb084486fad45c41251c08136c59b45a3ed033` |
| Tested installed parser SHA-256 | `f141b57575d48c4c09678fea34aa499f1adfc797a20b0839c3269928fd9b9f07` |
| Corrected public CLI executable SHA-256 | `87245c98b4ebb3f3df9ef4353909ca7ed9c35a4a768e36145fdd458e4e94fbc9` |

The original execution root remains
`.dev/asic-pt7c/runs/20261028T183412758171Z_83a02bdc`.
Its build identity, mapped netlist, emitted SDC/native producer, native-v2 data,
reports and process receipts are unchanged. The original provider/current pointer
still names the execution generation. Only a **separate reader-specific store**
was created. A's `/tmp` capture is corroborating prior evidence; C independently
captured the corrected reader into this durable example-local store.

Capture `reader-r1b-capture-01/` uses the existing development capture/install
mechanism under switch `5.2.0+ox`, the ASIC checkout lock, and `--jobs 6`. All
nested Dune builds/install/API validation are sequential, explicitly six jobs or
lower. There was no new example emitter/adapter build or tool invocation.
These are local captured-byte/build receipts, not authenticated execution,
clean-checkout claims, or replacement identities for the original run.

The installed producer source and runtime helper were directly compared between
the two generations and are byte-identical:

* `timing_coverage_tcl.ml`: `4240095a12a44c9f30a085b5713f7db3dfcc02967a9dfb2efdba5818c096e33a`
* `timing_intent_runtime.py`: `6648a8c8b897facf563d81c62ef229369f5c5e2b7ee858bcb22b707c3fed31f8`

## Corrected public replay and archive

`reader-r1b-replay-03/commands.json` retains exact argv, exit status and hashed
stdout/stderr for **11 positive replay/archive commands**:

* Original coarse inspect: exit **1**, completed/unavailable, JSON identical to
  `public-v2-01/inspect/stdout.log`.
* Original collect **with `--stdout`** and report: exit **0/0**, identical retained
  collection JSON. The original source root is read-only in the child namespace.
* Prior restored coarse inspect/collect/report: **1/0/0**, exact same JSON, with
  that source root also read-only.
* Original standalone native audit inspection: **1**, equal to the baseline
  coarse envelope's inner native view.
* Public archive publication from a **new retained-source copy**: **0**. Original
  evidence is never a write target; no collect operation writes its results file.
* The newly published reports/input-bundle archives are restored into a new root.
  Corrected public inspect/collect/report return **1/0/0**, identical to original
  results, in a private namespace with the original example root (including PDK,
  original run and bundle) and ASIC source hidden. Only the corrected installed
  generation and new restored evidence are rebound read-only.

The unchanged native view still records six exact stored relations, all seven
category-bound diagnostic groups, the verified top and 12 endpoints. The original
three **−0.044244 ns hold violations** remain retained timing facts. Reader replay
does not create a new timing run or improve its closure verdict.

## Byte-exact CR counterexamples against actual audit sources

The new script `scripts/pt7c_reader_r1b.py` derives diagnostic copies from the
actual accepted/restored native-v2 audit, writes native SDC **in binary mode**, and
reseals inner source hashes, runtime audit references and companion source hashes.
The original audit is never edited. These invalid diagnostic assertions are not
presented as newly executed native results. There is no consumer-local SDC parser.

**14 cases × 5 public routes = 70 intended assertions** cover coarse inspection,
standalone native audit inspection, collection (`--stdout`), report and archive:

| Case family | Expected interpretation |
| --- | --- |
| Original LF bytes; ordinary LF comment | Valid supported dimensions |
| Bare CR in comment before extra relation | Reject `CR in native SDC` |
| Bare CR before timing disable | Reject `CR in native SDC` |
| Bare CR before new design selection | Reject `CR in native SDC` |
| CRLF whole file; mixed CRLF; CR-only | Reject `CR in native SDC` |
| CR inside braced or quoted value | Reject `CR in native SDC` |
| CRLF native command continuation | Reject `CR in native SDC` |
| LF-exposed extra relation | Reject `extra exception relations` |
| LF-exposed timing disable | Reject unsupported `set_disable_timing` |
| LF-exposed design selection | Reject repeated/ambiguous design selection |

All nine CR forms reject on the intended LF-only grammar diagnostic, rather than
an incidental hash mismatch. Both LF positives retain the baseline native view;
the three LF semantic negatives demonstrate that ordinary comment handling does
not hide an exposed command. Invalid inspection/archive returns **2**, collection
returns **0 with explicit timing evidence error**, and report returns **1**.

Three independent real `tclsh` **source-channel** controls retain exact binary CR
fixtures. Inert command counters confirm that Tcl sees the bare-CR extra relation
(two false paths), masking command (one disable), and changed top (two design
selections). These are language checks, not STA execution. Inspection itself never
executes the retained Tcl. CRLF/CR-containing syntax can be valid Tcl but remains
outside the deliberately qualified LF-only native serialization grammar.

## Preserved attempts and protection

`reader-r1b-replay-01` and `-02` retain successful read-only inspection/collection/
report replay followed by an empty-diagnostic gzip failure under C's restrictive
bubblewrap archive environment. Dropping PID isolation alone did not resolve it.
No provider defect or particular low-level gzip cause is inferred. Attempt 03
uses ordinary supervised gzip **only on new source copies**, retaining read-only
namespaces for original public readers and the hidden-source restore replay.
Archive publication then passes. Neither earlier attempt was overwritten.

Full before/after inventories prove **199 original run files and 115 prior
restored files unchanged**. `r1b-history-baseline-01/` protects all earlier C
evidence, successful/failed runs and installed execution generations before this
continuation. The final closeout rechecks that inventory and the original
**10,398-file** protected-input/history baseline with zero changes. Native-v1
success and all preliminary failures remain their original historical outcomes.

`closeout-reader-r1b-01/` retains separate original-producer and corrected-inspector
identities, complete installed file hashes for both generations, the exact tested
parser source, final handoff/review snapshots, source/evidence checksums and both
protection verifications. `reader-r1b-replay-03/summary.json` is the machine-readable
replay/negative/oracle/protection summary.

**No new EDA, P&R, design emission, source override, Git mutation, old provider
selection, Workbench/Protemu, daemon, pin or application-config change occurred.**
Only the capture build consumed C's bounded six-job allocation. Remaining coverage
qualifications are unchanged: exhaustive exception effects, reset-effect/CDC
adequacy and post-PNR behavior are unavailable; timing closure is not established.
