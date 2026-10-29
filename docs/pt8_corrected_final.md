# PT8 C corrected installed acceptance — B R1–R4

2026-10-29. **Corrected installed acceptance passes.** This new receipt supersedes
the reader acceptance in `pt8_final.md`; the original generation, matrix, source
snapshots, final receipt and sealed documentation remain retained unchanged.

## Exact captured generation and final sources

After reading B's final R1–R4 handoff and A's no-blocking-defect library review:

- Generation: `.dev/asic-pt8/provider/generations/f205e0d66f8d4f2b8d1e5f098171bb21`.
- Captured source snapshot SHA256:
  `1f5ac45882b29c7d577937b4ba2eb8960a899bd2221eaae5b3e115a111de3213`.
- Provider receipt SHA256:
  `57dcf229e04b8b48654fdcde10ab4782a0a3d31dfea73d274c7e853eb0a287ff`.
- Captured source tree and per-file hashes:
  `acceptance/pt8/capture-corrected-01-nested/source-snapshot{,.json}`.
- Fresh public adapters: `_build_pt8/default/variants/{variant_cli,review_api}.exe`.
  Executable digests, constructor/oracle hashes and the reviewed production-file
  hashes are bound in **`acceptance/pt8/final-corrected-seal.json`**.

Final captured production SHA256 values (checked against B's final handoff):

| Source | SHA256 |
| --- | --- |
| `execution/results/variant_comparison.ml` | `37d593d884f7d093ce3312dcce69bfedce03e6a2a4c1e4dada82bab0b93f2bed` |
| `execution/results/resource_inspection_service.ml` | `53bd488c040859cef6c6f7178ac7265f8d79bd6a6ba671b50122459654f46b1d` |
| `execution/results/report_service.ml` | `83e4981d97ce92fd257f3c6fdbe4424194ff852e9469187a44a54a41eb53b0b5` |
| `execution/results/retained_file.ml` | `c858c5f4c772150095d3066e3831aac679d3ab158fe3abfff8e7aa8889a5ec39` |
| `execution/retained_file_stubs.c` | `5247984585b41510e3ae301713e9b7d2956f5c378b256ec683d3667bd23d09b0` |
| `execution/archive/archive_service.ml` | `dab674a84fa07d8cdf4ae16594d7016eee37b129e0a83c84ed37c342f52aef2d` |

The complete12-file reviewed list, `.mli` files and Evidence_json implementation
hashes are in the new final receipt. These are captured-source observations/local
provenance, not a P6 or compiled-source attestation.

Capture/build receipts retain switch5.2.0+ox, explicit6-job nested Dune build,
install and consumer probe, shared `/tmp/opencode/asic-pt7-build.lock`, and example
`_build_pt8`/`-j6` under `/tmp/opencode/example-pt7-build.lock`. Seven nested capture
commands are retained. No existing provider/configuration selection was changed.

## Hardware unchanged; no repeated functional simulations

`variants/variant_memory.ml` and `variants/test/conformance.ml` have exactly the
same hashes as the original final build's source copies. The full constructor,
schema, factory and oracle also match the actually simulated source after removing
only the subsequently added required TT pin descriptions. The new seal performs
those byte comparisons, rather than trusting hardware metadata.

The original six functional simulations are reused: five positive cases and the
one deliberate ignored-depth request/behavior failure. **Additional simulations0;
EDA runs0.** New code is only the public archive/report review shim and acceptance
scripts. No production parser/comparison engine or renderer is implemented here.

## Repeated installed public204 matrix

`build-corrected-01` and `emit-corrected-01` freshly build the adapters and emit
the five bundle cases with the corrected installed provider. Exact128 still
rejects; no fallback is introduced. `matrix-corrected-01/assertions.json` records
**all204 assertions passing**, with26 traced native API/CLI invocations:

- Actual depth128/256 resource/RTL differences; same logical hardware under
  Flops/Exact256 policy; existing backend profile differences; ignored-depth
  integrity success remains distinct from semantic conformance failure.
- Original area/delay executions remain separate identities with equal mapped
  output bytes and unavailable historical hardware parameters.
- Original accepted physical self-comparison retains18 native comparable zero
  deltas and separate closure/exhaustive-coverage outcomes.
- Original all-corner synthesis versus physical retains18 confounded native
  metrics with null deltas and explicit stage/corner/model/environment/RC context.
- Source/claim/attempt substitution negatives, unavailable workload, no winner,
  complete responses and entire installed public API/CLI parity still pass.

Exact comparison digests for the original targets:

| Pair | Corrected digest |
| --- | --- |
| Named area/delay | `7cf3dd62688e5835fcb30437380d280c401243f9a4535803f1801022a0c2d991` |
| Coarse physical self | `755ffb7a8b8dc6caeda8eceda4c432d0957bc2c377c807ecce0ced1857f342e3` |
| Coarse synthesis/physical | `0969f1b9450053eda28502bad1a964b5fb60a8e31deac127c6a7f268092e00d7` |

## Actual correction controls and intended diagnostics

`scripts/pt8_corrected_controls.py` calls the installed public comparison API/CLI
and public Report_service/Archive_service through a small compiled shim. Every
mutation is on disposable copies; originals and historical metadata are untouched.
Final controls: **`controls-corrected-04/controls.json`**,18 case receipts.

1. **R1 actual coarse declared inputs.** A clean copy of the original physical run
   first passes18 native self metrics and full bundle-source verification. Changing
   its actual declared `inputs/asic-dependency.json` then rejects API/CLI with
   `bundle member hash mismatch`; deleting it reaches the exact missing-file path.
2. **R2 actual descriptor consumers.** The original run has no stored
   `results.json`. The harness captures its actual public report result and stores
   that unmodified projection only on a copy. Its clean stored-results control
   passes. FIFO, symlink, directory and32MiB+1 sparse replacements reject in both
   comparison and **actual Report_service**, with regular-file, retained_open,
   directory-channel admission and byte-bound diagnostics respectively. No local
   precheck stands in for the service. Valid JSON padded to **exactly32MiB** passes
   with identical metrics and an actual32MiB consulted-metadata reference.
3. **R3 raw generation.** A stable formatting-only change alters the raw results
   SHA256, source digest and comparison digest while leaving metrics identical.
   Inotify then mutates results after left capture, synchronized to the other copy's
   actual manifest open: API and CLI both reach `comparison source generation
   changed`, with mutation completion and both raw hashes recorded. Separate
   actual-open results-to-FIFO races complete their mutations and reach `retained
   source changed during read` in both public paths, without blocking.
4. **R4 actual archive raw duplicate admission.** The unmodified actual run copy
   first passes Archive_service.inspect with genuine metadata absence. Negative-only
   malformed optional fields are then injected on the copy, binding the run's raw
   manifest SHA and the last-wins outer payload identity. Optional-field duplicates
   and escaped-key aliases reach **`duplicate key: hardware_variant`**; assignment
   duplicates and escaped aliases reach **`duplicate key: depth`**. Raw injected
   manifest bytes are retained. No successful hardware declaration is added to
   historical evidence, and no archive publication or EDA occurs.

The three earlier harness failures remain under `controls-corrected-01..03`:
initially expecting a stored results file, expecting a specific directory error
wording, and expecting compact rather than pretty staged-manifest formatting.
They are harness assumptions corrected in the passing04 attempt, not hidden or
rewritten provider acceptance results. Per-case receipts now survive partial runs.

## Limits, final read-only trace and preservation

- Actual stored metadata limit: **32MiB/file**; report aggregate limit **64MiB**.
  The inclusive file boundary and +1 rejection are exercised; no independent
  aggregate-boundary acceptance is claimed.
- Comparison response: **1MiB**, complete or rejected. Exact response byte sizes
  and maximum observed stdout are retained in the final seal.
- Existing comparison bounds remain4096 inventory/difference rows and256 metrics
  per side; no new sweep, paging or workload contract.
- Correction-control subprocess deadlines are180s each. FIFO/race rejections
  finish without timeouts; this is a harness deadline, not a service-wide runtime
  guarantee. All captured commands retain elapsed times and limits.
- Final API/CLI query against the untouched original physical run has file/process/
  **network** syscall traces: one process, exact native CLI/helper exec replacement,
  zero child tools/renderers, zero write-capable opens/mutation syscalls and zero
  network syscalls. Correction-control queries have the same trace checks; harness
  mutations are outside the traced service process.
- One final full verification of the original baseline checks108,338 pre-existing
  files and65 symlinks. The original PT8 final receipt's evidence files, original
  installed generation and sealed documentation are independently checked as well.
  Results are in `preservation-corrected-final.json` and `final-corrected-seal.json`.

**Exact macro Methodology_plan.prepare is a confirmed pre-existing unsupported
named-macro boundary, not a new PT8 defect. It remains unsupported and was not
enabled.** All new bundle comparisons continue through the existing uniform
catalog-resolution/render/publication path. No Protemu/Workbench/Git mutation,
daemon action, EDA or historical provider/configuration selection change occurred.
