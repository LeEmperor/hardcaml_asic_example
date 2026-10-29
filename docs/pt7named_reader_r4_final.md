# PT7 named R4 — independent corrected-reader qualification

**Passed, read-only.** C independently replayed B's existing R4 helper against the
original area/delay execution files. No build, provider capture, EDA, P&R, renderer
or original-evidence/provider mutation was performed.

New C receipt: `acceptance/pt7named/reader-r4-correction-01/summary.json`.
New status index: `acceptance/pt7named/readiness-reader-r4.json`.

## Exact replay and separate execution attribution

Read B's final R4 handoff and source/binary receipts. R4 tightens publisher/reader
validation of frozen external locators and non-null pins; runtime/native
producer/schema2/profile2 are unchanged. C used the already-built helper at:

```text
/tmp/opencode/pt7-r4-real-reader-replay-mt6ieg_5/reader/_build/default/bin/
```

`scripts/pt7named_reader_correction.py --attempt reader-r4-correction-01` invokes
its `flow_cli.exe` for explicit `timing-intent-inspect --kind execution --json` and
`report --json`, plus `api.exe sources`. The new C command receipts retain exact
argv, exits, elapsed times and log hashes. B's build/replay script and broader
suites were not rerun.

Original EDA remains attributed to provider **`ce6be246fafa4d0dbe1dd00da980482b`**,
receipt SHA256 `bebcd8f6b7362fd00265578ed38887c76843a623de5fb0cadbb03205ea94232d`.
The corrected helper is a separate reader, not a new execution-provider capture.

## Independent results

| Check | Area | Delay |
| --- | --- | --- |
| Original attempt | `cb5e7cd92dbf43b4a6c00a74b61c6d72` | `9374823306a64897959e1b2295f52c84` |
| Inspector/report/source API exits |1 /0 /0 |1 /0 /0 |
| Inspection equals original JSON |Yes |Yes |
| **Entire** report equals original JSON |Yes |Yes |
| Report timing equals inspection |Yes |Yes |
| Source API equals original1584 references |Yes |Yes |
| Declared aliases preserved |1062 |1062 |
| Original run files unchanged |168 |168 |

Both views remain completed/unavailable with six relations, seven categories and12
endpoints. Both exact staged floorplan locators match the frozen pin
`b46d9a0ee8352160e48dbc8312f092f985629061df736c7f46d58686535a76f4`.

Before/after ledgers verify SHA256, canonical resolution, device/inode, size,
mtime and ctime for every original run file and advertised source. All match.
The replay also verifies **236 earlier example receipt/evidence files unchanged**
and the original provider receipt unchanged. No original collected result or
accepted public receipt was rewritten.

`reader-r4-correction-01/original-preservation.json` additionally verifies **16,084
original files, zero failures**. Checkpoint identities and native numeric outcomes
remain those in `native-closeout-final-03`: three setup witnesses at+19.432287ns and
three hold violations at−0.044244ns per profile. No waiver, timing closure or named
archive/relocation claim is added; evidence stays path-bound.

## Helper/source identities

Actual executable hashes match B's receipt before and after replay:

| Executable | SHA256 |
| --- | --- |
| `experimental_timing_intent_inspect.exe` | `751496b36b209155869e4a46f6e2984f47b6cebcf2d687480c5502212ba34461` |
| `experimental_report.exe` | `cb590e9950d50d6582a29e31876e5cfd6d4719b2445f3145c180844ea24ba0f7` |
| `flow_cli.exe` | `eb10b137a2df746753fada5556b12a3908e68302057f7861be78aa35117a5d72` |
| `api.exe` | `646a0ef2810fb6c6d3790765834a1628b13e40709aa4eceb20b3989a93568ea3` |

`reader-identities-{before,after}.json` retain actual paths/hashes for all four
binaries and all nine production/test sources in B's `tested-source-receipt.json`;
the before receipt also records C's replay-script hash. All observed source hashes
match B's tested receipt and are unchanged after replay. Corrected
`execution/results/timing_intent_execution.ml` is
`1717a6813d9b299895be6c5f371ff360b610b7b94e37b2ec080f16f8ea685676`.

`runtime-source-comparison.json` independently verifies all **seven** current
runtime/lifecycle/probe/bridge/helper source files byte-match the original executed
provider's installed sources. These are explicit local executable/source identities
and equality checks, **not compiled-source authentication** or attribution of old
EDA to a new provider. B's282-check suite remains B's qualification; C's new result
is this narrowly bounded real-evidence replay.
