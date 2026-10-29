# PT8 C — independent installed example result

2026-10-29. **The bounded independent example acceptance passes**, with the
methodology-plan limitation below explicitly retained. EDA allocation/use **zero**;
exactly **six functional simulations**, five positive and one intentional negative.

## Installed provenance and actual commands

Captured after reading A/B's implementation/qualification handoffs:

- Provider generation: `.dev/asic-pt8/provider/generations/d36e6cd31c894dc384e7757716bb87ee`.
- Provider source snapshot SHA256:
  `9b8a3fa24d3081e6f268e03c868118510e2645fa4b3c36e570c70ab8650d6a86`.
- Provider receipt SHA256:
  `434de8f6ede2662d49188908a492a5bad7021dae4a0f8a12e070e2cd6e8ba752`.
- Exact captured source tree and file hashes:
  `acceptance/pt8/capture-01-nested/source-snapshot{,.json}`.
- Seven capture nested-command receipts retain build/install/query/probe commands.
  Dune build/install/probe explicitly use6 jobs under switch5.2.0+ox and the shared
  ASIC lock. Example builds use `_build_pt8`, explicit `-j6` and the shared example
  lock. No switch install or existing provider selection was changed.

Final emission/build/matrix receipts are `build-05`, `emit-04`, `matrix-03` under
`acceptance/pt8`. Reproduction commands (from the example root) are in
`scripts/pt8_acceptance.py`; pass the exact generation, a fresh attempt name and
explicit source targets. Existing evidence directories are never overwritten.
The final source/provenance seal is `acceptance/pt8/final-seal.json`.

## Real constructor and semantic conformance

The public Hardware_variant declaration is depth128/256, width16, read_latency1.
Project.of_variant passes the checked immutable assignment into the factory;
the same value supplies actual Single_port_ram.Config and address decoding.
The source is `variants/variant_memory.ml`, with independent oracle
`variants/test/conformance.ml`. Core and TT construction share the RAM constructor.

Actual functional receipts: `acceptance/pt8/functional-01/`.

| Case | Actual checks/result |
| --- | --- |
| Flops128, Implementation and Simulation | Each646 edges; actual128×16 request, full capacity/readback, disabled reads/writes, registered latency1, final-address overwrite, address128 aliases0 |
| Flops256, Implementation and Simulation | Each1286 edges; actual256×16 request, all256 words, latency/hold and boundary128 remains independent |
| Exact256, Simulation |1286 edges; selected stock macro and same logical contract/behavior |
| Ignored depth128, Implementation | **Exit1 expected**: actual registered request rejects; independent behavioral check fails at edge642, expected`abcd`, actual`1234` |

Exact128 rejects in both elaboration modes with the real “no exact implementation”
and “flop fallback is not permitted” error. The schema's valid-but-unsupported
depth192 tuple rejects in the adapter factory. No rounding, banking or fallback.

Only pin descriptions and emitter wiring changed after these simulations;
the RAM constructor and behavioral oracle are unchanged. The retained pre-fix
consumer source is `consumer-before-pin-descriptions/`; final build source is
`build-05/consumer-source/`. No additional simulations were run.

## Public emitted bundles and comparisons

All new bundles use the same public `Flow.Catalog.resolve` ->
`Project.render_result ~methodology ~catalog_inputs` -> `Bundle.publish` path.
The existing `asic/flow_profiles.ml` supplies `balanced` and `synth_delay` backend
assignments. Hardware parameters, policy requirements and backend settings remain
separate. There is no new scheduling/launcher system.

`matrix-03` records **204 independent assertions**, entire installed native CLI/API
JSON parity, source-generation-bound digests, source references and retained
identities. All public comparisons are read-only:

- Flops128 vs Flops256: different actual RTL/resource contracts/declarations.
- Flops256 vs Exact256: equal hardware declaration/logical contract, different
  explicit policy/selected representation; Exact256 emission succeeds and
  Exact128 emission rejects.
- Balanced vs synth_delay256: equal declaration/RTL, different backend settings.
- Correct vs ignored Flops128: **valid hashes and equal declarations**, but
  different actual resource contracts. Integrity success is not conformance.
- Original named area/delay: separate attempts/bundle/plan/publication identities,
  equal retained mapped outputs, hardware parameters explicitly unavailable.
  Two authoritative boundary measurements remain small and qualified: cell
  count and an area **estimate**, with no measured delta invented.
- Accepted coarse physical vs itself: original acceptance pass, all three corners,
 18 authoritative native metrics comparable with exact zero deltas. Resource
  metrics lacking required context remain unavailable. Native exhaustive coverage
  stays unavailable; bounded closure pass is not an exhaustive-coverage pass.
- All-corner coarse synthesis vs physical:18 native metrics **confounded**, with
  all deltas null, explicit distinct stages, matching explicit corner identities,
  model/RC context references and stage/RC/environment reasons. Signed negative
  synthesis hold is retained. Named synthesis vs physical is also checked;
  unsupported historical whole-design timing is not manufactured from witnesses.

Historical source paths are explicit in `scripts/pt8_matrix.py`; neither “latest”
nor current catalog/provider selection is used. No historical manifest received
hardware metadata. Workload/firmware/fetch/latency/throughput evidence remains
unavailable; there is no winner or score.

## Negatives and preservation

Clean copied bundle controls pass before corruption. Copies only then reject in
both installed public paths:

- Declared source mutation: `bundle member hash mismatch`.
- Valid donor hardware claim rebound without its identity binding:
  `invalid bundle manifest identity`.
- Donor named methodology rebound to another attempt:
  `methodology reference contract/attempt mismatch`.

Every final-matrix API/CLI invocation has process/file syscall evidence. API runs
one executable; CLI exec-replaces itself with the exact installed native comparison
helper in the **same process**. No fork/clone, external tool or renderer subprocess,
and no write-capable file operations occur. Captured comparison source routes only
through verified retained readers; it calls no project factory or renderer.
The harness writes its own logs/negative copies outside those traced invocations.

`preservation-final.json` rehashes **108,338 pre-existing files and65 symlinks**:
zero changes, including untracked physical/named histories, ignored provider stores,
selectors and tracked app configuration. No Protemu/Workbench/Git mutation,
daemon action or historical provider selection change occurred.

## Retained failures and production finding

- `emit-01`: required TT pin descriptions absent; C fixed the declaration.
- `build-02`: source-evidence copies initially entered Dune traversal; new
  `acceptance/pt8/dune` excludes retained evidence directories from builds.
- `emit-02`/`emit-03`: Exact256 through Methodology_plan.prepare fails with
  `object fields do not match versioned schema`. Its existing manifest whitelist
  omits macro_contract and its generated-source checks assume nonmacro RTL.
  This is reported to A in `pt8_handoff.md`; production code was not edited by C.
  Uniform public render/publication succeeds for the requested bundle comparisons;
  **Exact methodology-plan support is not claimed**.
- `matrix-01`: initial tracer oracle expected one exec, before accounting for the
  documented native CLI helper exec replacement. Tight same-process/absolute-path
  allowlisting fixed the oracle.
- `matrix-02`: test expected inline metric controls; B's published digest-keyed
  metric_contexts dictionary is used by the corrected assertions in matrix-03.

The generation receipt/source inventory are local captured provenance, not a
compiled-source/P6 stamp or general hardware-use attestation. These results do not
complete Protemu consumer selection.
