# Independent named synthesis acceptance (C)

**Status: actual bounded native acceptance completed for two fresh named synthesis
profiles, area and delay.** See [native final acceptance](pt7named_native_final.md)
and `acceptance/pt7named/native-closeout-final-03/acceptance.json`. Public execution
inspection/report/source-files agree; checkpoint bytes remain unchanged through
supplementary STA; the complete real PDK alias closure is retained. Negative hold
remains visible. No P&R or timing-closure qualification is claimed. Earlier blocked
attempts below remain historical evidence and are not repaired or relabelled.

**Latest reader correction:** [independent R4 reader replay](pt7named_reader_r4_final.md)
qualifies frozen-external-pin validation against both unchanged executions. New
receipt: `acceptance/pt7named/reader-r4-correction-01/summary.json`. The original
native execution generation and receipts retain their identities.

## Scope and source inputs

`named_timing/named_catalog.ml` declares a synthesis-only named methodology with
two distinct profiles (`area`, `delay`). `named_timing/named_timing_cli.ml` uses
public `Methodology_plan.prepare` and `Bundle.publish`. It reuses the original
timing specimen/project via Dune `copy_files`; original hardware and emitter input
bytes remain intact. The original project source inventory is retained and the
three named catalog/adapter/Dune files are explicitly added as catalog inputs.
There is no local timing parser. `named_timing/reader/named_sources.ml` is a
pass-through to B's public verified-source API.

All new dependency captures and runtime work belong to `.dev/asic-pt7named`;
example builds use `_build_pt7named`. Evidence uses `acceptance/pt7named`, with
exclusive new attempt directories and retained command failures. Existing PT7c
histories and source inputs are sealed in `original-history.json` and the
supplementary snapshot. Provider captures use the ASIC shared build lock;
consumer builds use the example shared lock, switch `5.2.0+ox`, explicit `-j6`.
Nested capture build/install/probe calls receive `--jobs 6`. Work is sequential
within C's six-job allocation; linked STA must use one thread, with explicit
runtime CPU/container/worker budgets in A's launch evidence. P&R allocation is zero.

## Prepared public procedure

`scripts/pt7named_acceptance.py` captures commands, environment thread limits,
elapsed time, exit status, log hashes and exact captured-provider receipt hash.
Timeouts terminate the command process group, retaining the failed receipt.

1. After A/B final readiness, `capture --attempt capture-N` creates a fresh provider.
2. `build --attempt build-N --generation EXACT_GENERATION` builds the consumer.
3. `prepare --attempt area-prepare-N --generation EXACT_GENERATION --profile area`
   runs separate public catalog plan/emit, requires plan equality, validates emitted
   member hashes, and freezes the exact plan and bundle inventory.
4. `run --attempt area-run-N --generation EXACT_GENERATION --prepared PREPARED_JSON
   --runtime-confirmation A_CONFIRMATION_JSON` invokes public `stages` on that frozen
   exact bundle/plan. There is no implicit rerender. The gate requires A's explicit
   confirmation of preflight/probe/synthesis/publication/analysis worker counts
   (each at most six), `sta_threads:1`, and `confirmed_by:"A"`.
5. `public --attempt area-public-N --generation EXACT_GENERATION --execution
   EXACT_EXECUTION_JSON` invokes `timing-intent-inspect --kind execution` and
   named `report`, checking read-only behavior. Final checks will assert parity,
   five original stages/six native relations/seven diagnostic categories/12
   endpoints, one executed default corner, retained negative hold, verified source
   closure and checkpoint byte identity across linked STA.
6. A sequential second profile/attempt may provide real substitution controls.
   Controls must preserve original successful evidence, use real associations,
   and exercise the public inspector/report. No invented coarse records.

The checkpoint/publication association is path-bound. No named archive/export,
relocation, hidden-root replay, exhaustive exception-effect coverage or timing
closure is claimed. Native schema2/profile2 remain unchanged. This document is
readiness evidence only until actual bounded execution receipts are appended.

## Executed preliminary integration (no EDA)

`capture-integration-01` successfully captured/installed isolated generation
`79dba53255354b6eb5dcb63d8b0c3da1` (snapshot
`1b0cf14f7e3b19832602a1c518e8d444b636face58e26cdb69d1d7f9281aa740`).
This is explicitly a preliminary, concurrently developed provider, not a final
candidate. Its nested builds/install/consumer probe used six jobs under the ASIC
lock. `build-integration-01` successfully compiled the named catalog CLI and both
public reader/source adapters under the example lock, switch5.2.0+ox, `-j6`.

`area-prepare-integration-01/plan` failed with exit1 and
`(Invalid_argument "object fields do not match versioned schema")`. Provider
`lib/methodology_plan.ml:163-185` enumerates manifest fields strictly and currently
only conditionally admits `resource_snapshot`. The timing producer adds timing
manifest fields, which this decoder does not yet admit. The failure occurs in the
actual public `Methodology_plan.prepare`, before emit/synthesis. C has not changed
provider source or bypassed this decoder. The original failed receipt/logs are
retained. A/B/coordinator must correct this production seam before fresh final
capture. Final capture, two profile preparations, synthesis and public acceptance
remain blocked; no EDA has been launched.

`preservation-preflight.json` verifies 16,079 original tracked/history files with
zero failures. `original-history-supplement.json` additionally includes pre-existing
untracked documentation. Python syntax checks and CLI help passed.

## Executed final integration checkpoint — closure blocker

After A/B final READY and the user's explicit six-job EDA allocation, C read both
final handoffs and captured a **new** provider in `capture-final-01`:

- Generation: `e71a18b5a5ba45e0b8783951af10ce6d`
- Captured source snapshot SHA256:
  `5380f1a61af63184423352fc61d2791dfff25566b0c52163fbdc4eea5cc9215d`
- Provider receipt SHA256:
  `3c938a88705e12d62b431916c8d79a31f57a5a0df4fa30c8d4f8dafee74164bc`

`build-final-01` passed, compiling the consumer and both public API adapters under
switch `5.2.0+ox`, example lock and `-j6`. Capture's nested build/install/probe
remained six-job bounded under the ASIC lock. All work was sequential.

The manifest decoder correction is confirmed by successful actual public plan
then emit for **both** profiles, including exact plan equality and emitted-member
hash checks. Frozen plan/bundle identities are:

| Profile | Plan identity | Bundle identity |
| --- | --- | --- |
| area | `85b949035d025689a14f72b0698440becc52224fdb785e710d16cd53d9d73687` | `d102a1866f7033be317a96ef01ec4ade0f3074f862d7ba2bdecdafaf7b160669` |
| delay | `673350dd8606ec6c8be49385eb8f109780dd1aae3df0452980efc2a8d94b7888` | `b778f25e704354c1bc7084b4de69076378fc084b2c8820dc6c3dede8c34ecdce` |

The respective `area-prepare-final-01/prepared.json` and
`delay-prepare-final-01/prepared.json` retain exact paths, frozen plan hashes and
complete bundle inventories. These are two genuine prepared profiles, **not two
executed synthesis attempts**.

### Concrete actual-toolchain blocker

A's final handoff requires checking whether the conservative checkpoint closure
fits B's bounds before launch. `scripts/pt7named_precheck.py` walks the entire
target PDK tree using the bridge's recursive path semantics, including symlink
targets and cycle detection. The actual provisioned
`_flow_tools/pdk/ihp-sg13cmos5l` contains:

- **1,486 mandatory source paths**, versus **512 sources total** allowed by
  `Timing_intent_execution.verify_sources`;
- **165,433,805 bytes** in total (within the 512MiB total byte limit);
- an individual **67,485,696-byte**
  `libs.ref/sg13cmos5l_io/gds/sg13cmos5l_io.gds`, exceeding the **67,108,864-byte
  (64MiB)** per-source limit;
- 589 symlink files, additionally relevant to the reader's canonical regular-file
  policy; no aliases have been silently removed from the mandatory inventory.

These are mandatory under `librelane_bridge.closure`: it recursively inventories
the **entire target PDK tree**, not merely the two STA Liberty inputs. A's
`Timing_intent_named_service.capture` adds all non-`/nix/store` checkpoint external
files to publication sources. B verifies the same bounded source closure before
publishing/reading the companion. The PDK alone therefore cannot fit this route,
even before adding the bundle, checkpoint, native reports and transport evidence.

`area-run-final-01` accepted A's final bounds confirmation and verified the frozen
plan/bundle, then the integrated closure precheck exited1 before workspace
creation or any synthesis/STA. Exact argv/stdout/stderr/exit/time/log hashes are in
`area-run-final-01/closure-precheck/command.json`; its full actual inventory is
`area-run-final-01/pdk-precheck.json`. The separate initial precheck is retained
at `pdk-precheck-final-01.json`. No declared files were omitted or PDK bytes changed.

**Actual synthesis/STA jobs launched: zero. P&R jobs: zero.** There is consequently
no new checkpoint, numeric setup/hold result, execution inspect/report parity,
verified execution source list or substitution-negative acceptance to report.
No waiver or timing outcome is invented. Provider owners/coordinator must reconcile
the bounded named inventory with the real conservative PDK closure (including its
path/symlink semantics) before a new capture and real sequential profile executions.
C has not patched provider validation or altered provisioned tools to force a pass.

Final preservation checks (`preservation-final-01.json`) verify **16,084 original
files with zero failures**; preliminary histories/provider generation remain
retained. Python syntax checks pass. Machine-readable final readiness/blocker:
`acceptance/pt7named/readiness-final-01.json`.

## Executed latest integration — final-02 actual PDK alias blocker

Read A's R1/R2 and B's R1/R2/R3 final closeouts, including the4096-source,
128MiB-per-file,512MiB-total named outer contract and public
`Timing_intent_execution.precheck_sources`. `capture-final-02` captured combined
generation `774d85d08b8b4b7a9998f1723f5e2e1b`, source snapshot
`4e7a3cf65623fb7fadc2d0848770352a5c9c59713dc35be4301f093d04ece635`,
provider receipt SHA256
`c4ea1cdf2cc6d9202d128742b192055964cc58c8119032b0e69eae5cf0defbd1`.
`build-final-02` passed with a new public stat-admission adapter
`named_timing/reader/named_precheck.ml`. Both `area-prepare-final-02` and
`delay-prepare-final-02` public plan/emit passed and retain their exact frozen
plan/bundle/provider association. Switch5.2.0+ox, explicit-j6, shared locks,
sequential six-job allocation throughout.

The local stale512/64MiB gate was removed. The enumerator now only lists complete
existing PDK, frozen bundle, frozen plan and selected support-reference paths;
all limits/admission belong to the freshly captured public API. It resolves the
public Bundle.publish root symlink for current frozen object enumeration (the
runtime copies this into its canonical project). It does not rewrite internal
PDK aliases or drop required sources.

`area-run-final-02/public-precheck` exited2 with
`PT7 named inventory: linked/noncanonical source`. Its first enumeration also
included the public bundle-root alias. After resolving that root, a fresh retained
`area-run-final-03/public-precheck` still rejected the actual PDK for the same
reason. No stages command or EDA was launched by either attempt.

### Isolated real-path positive and negative

`path-diagnostics-final-03` exercises the same captured public API:

- Actual declared mandatory source
  `_flow_tools/pdk/ihp-sg13cmos5l/libs.qa/README.md`: **exit2**, linked/noncanonical.
- Its actual canonical193-byte target
  `_flow_tools/pdk/ihp-sg13g2/libs.qa/README.md`: **exit0**, admitted.
- All canonical target files from the complete1505-path input list, deduplicated
  **for diagnosis only**: **exit0**,1409 sources,165,350,582 bytes, largest
  67,485,696 bytes. API reports4096/134,217,728/536,870,912 limits and
  `hashes_verified:false` as expected for stat-only admission.

The actual declared inventory contains1062 paths whose `realpath` differs, including
internal directory aliases as well as file symlinks. The bridge's conservative
closure uses lexical `path.absolute()` keys when it walks the entire target PDK;
it follows symlinks to hash their bytes without replacing their declared keys.
A's capture retains those checkpoint external keys. B's
`Timing_intent_inventory.regular` requires `Unix.realpath path = path`, and its
`admit_checkpoint` also admits the unchanged external keys. Thus canonicalizing
only the precheck list would hide a later production rejection; the diagnostic
canonical-target inventory was **not substituted** into the runtime or production
source closure. Provisioned PDK, bridge, provider and earlier evidence were not
changed.

Provider owners must reconcile the actual declared-alias/canonical-target closure
association across bridge/checkpoint/publication/publisher/reader before native
execution. This is a distinct path-policy blocker, **not the repaired numeric
bounds**. Full alias mappings and exact command receipts are retained in
`path-diagnostics-final-03/diagnosis.json` and sibling command directories.

No synthesis/STA/P&R ran, so no new native numeric timing, checkpoint byte-preservation,
execution parity/source inventory or cross-execution negative result is claimed.
Both distinct profiles are genuinely prepared, not executed. Latest machine-readable
status is `acceptance/pt7named/readiness-final-02.json`; preservation-final-02 verifies
16,084 original files with zero failures. All prior failed/preliminary attempts remain.
