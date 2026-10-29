# Independent physical timing: actual first full result

2026-10-29. **Bounded physical timing and portable-source acceptance complete.**
Actual full pipeline, extracted timing, ordinary TT/final functional checks,
independent actual review and corrected archive/hidden-input replay pass. One full
attempt used; no repair rerun or EDA was needed for the archive-only correction.

## Actual implementation

- Run: `.dev/asic-timing-physical/full-runs/20261029T075052976305Z_23a6954b`
- Run ID: `23a6954b852d4205b542d3815634d772`
- Build identity: `ac513e0e7e9cfa935f73d697caebca8f601aeeb4ea62c2a2ccf61c10a10789cd`
- Captured provider: `4856e6af993642988c18c07f47a8c689`, corrected F1–F6 source
  closure and reviewed functional-postcheck capabilities verified before launch.
- Ordinary public coarse full exited0/completed in1477.77 seconds. Container/flow/
  OpenROAD/KLayout limits6. Dedicated all-corner pre/post-PNR and linked STA used
  one thread each. Mid-PNR OpenROAD steps36/38/43 requested6 (step31 requested1).
  All stayed within allocation6; owned cleanup succeeded. Coordinator accepted
  corrected disclosure of the earlier blanket STA1 claim, without physical repeat.
- Physical lineage: placement28 → CTS35 → ordinary post-CTS timing repair37 →
  detailed routing44 → RCX54 → original STAPostPNR55. Linked extracted STA consumes
  that original producer's **input State**, not a replacement synthesis netlist.

## Extracted all-corner timing

| Actual corner | Worst setup ns | Worst hold ns | Setup/hold violations | Slew/cap violations |
| --- | ---: | ---: | --- | --- |
| Fast | +16.058594908 | +0.102353212 | 0 / 0 | 0 / 0 |
| Typical | +15.729073600 | +0.276686071 | 0 / 0 | 0 / 0 |
| Slow | +15.113663637 | +0.590927102 | 0 / 0 | 0 / 0 |

All configured cell-PVT corners actually execute against one nominal extracted RC
view (`nom_*`), not three distinct RC extractions. Native process/log/State metrics,
ns units, exact ordered libraries, selected extracted SPEFs, propagated clocks and
native connected-net annotation filter sources validate. Filtered annotation goals
pass; this is not a blanket claim that every raw reported driver is annotated.
Full-clock-expanded min/max reports retain all three downstream paths per corner.
The detailed findings record actual clock/data/uncertainty/CRPR contributions.

The same five original reset flops remain, with unchanged latency/reset behavior.
Ordinary post-CTS repair inserted nine qualified noninverting delay cells. Native
checked timing paths have maximum depth2 (qualified bound8); exact sequential
inventory remains5. CTS35 is correctly identified as **pre-repair**. Original RTL,
20 ns clock,0.25 ns uncertainty, min/max IO, transition/load/derates are unchanged.
The original negative synthesis baseline remains retained, not relabelled clean.

## Ordinary physical and external checks

- Antenna nets/pins0, routing/Magic DRC0, LVS errors0.
- Normal TT precheck: all nine checks pass, including actual CMOS5L KLayout DRC.
- Normal final-netlist functional replay:512 observations pass using the production
  reviewed used-cell model profile. Exact final netlist matches native STA input.
- Normal public inspect/collect/report agree; original public report exits0.
- Exhaustive native exception-effect/per-check coverage stays unavailable.

`full-native-public-acceptance-01.json` retains independent consumer assertions and
source hashes. `preservation-after-full-01.json` verifies16,377 historical files/
selectors with zero changes. No PDK/bundle patch, protected-provider/config change,
SRAM rerun or Git mutation was made.

## Corrected archive and complete source replay

The earlier seven-report omission and failed restorations remain untouched under
`evidence/full-public-01/` and `evidence/full-restore-*`. Their pre-correction C
documentation is copied byte-for-byte under `evidence/portable-before-01/`.

New archive: `.dev/asic-timing-physical/evidence/full-public-corrected-01/archive-output/`.
It is published from the **same unchanged actual run**, using a distinct corrected
archive-reader generation; it is not a new physical execution.

| Identity | Value |
| --- | --- |
| Original execution provider | `4856e6af993642988c18c07f47a8c689` |
| Original execution source snapshot | `4a821a382619f33eda6be911cb1bddc9d71345a882e97c5fb5b5de68979153a3` |
| Corrected archive-reader provider | `1ba205c2a11c4904b03d98b0e7a3f616` |
| Corrected reader source snapshot | `454be3f35b6183bf5142913e224b5e5665d186a1fa251efbb8e3e31c2eef8512` |
| Captured archive_service.ml | `4c86b6516f31b0c1c18a07364ab85b7c38a9122633debec2cafeac93befb415d` |
| reports.tar.gz SHA256 | `8f2bff91bb171b95f24d05142009619693ac80aa5ce358c4d5a66ba762b4e366` |
| input-bundle.tar.gz SHA256 | `ab91f86aaf778631cb4533b10199c1cb4baab529173d5f0d04e7875915a0759d` |

`full-restore-corrected-01` restores476 files from only the new archive/input bundle
and exact loose records. The original run/example/PDK and ASIC source are hidden;
the restored tree is read-only. Public inspect, collect and report exactly match
the original execution responses, including **all423 raw artifacts**. Every one of
the449 archive members and every advertised source file matches the pre-correction
original byte hash. The seven formerly omitted physical reports are now included
with verified producer/config/State/runtime provenance. No live-run copy fills the
restoration and no response comparison was normalized or weakened.

`portable-verification-01.json` binds all source hashes, actual thread-command
observations, original run identity and corrected archive identity. It verifies all
1196 original run files and the original archive/public evidence are unchanged.
A's independent actual review records1720 assertions and confirms five-stage
preservation, narrow exceptions, all-corner native closure and ordinary gates.
Its thread-accounting discrepancy is explicitly accepted by the coordinator as
within allocation6, with no physical rerun. Actual commands/records are unchanged.

Final receipt and current/snapshotted source inventory are packaged under
`.dev/asic-timing-physical/evidence/portable-package-01/`; the package digest is in
its `closeout.json`. Detailed failed-attempt history and accounting correction:
[`timing_physical_findings.md`](timing_physical_findings.md).
