Run from `hardcaml_asic_example` in your existing `5.2.0+ox` shell. After a
development refresh has succeeded, select it **in that same shell**:

```bash
source .dev/asic/current/activate.sh
ocamlfind query hardcaml_asic
python3 scripts/asic_dependency.py status --json
dune runtest . -j 20
```

The query should name `.dev/asic/generations/<selected-id>/lib/hardcaml_asic`,
not `~/.opam/5.2.0+ox/lib/hardcaml_asic`. An unactivated shell can find the old
`0.1.0` package there, causing unbound `Elaborated_project`, `Project.source_inputs`
or `Project.describe`, and rejection of `Project.create ~source_inputs`.
Refresh and bootstrap are child processes; neither can activate your calling
shell. Re-source after refresh or after switching/resetting the opam environment.

To capture current provider edits (including relevant untracked files):

```bash
python3 scripts/asic_dependency.py refresh \
  --source /home/wayne/devel/jane/hardcaml_asic \
  --mode development

source .dev/asic/current/activate.sh
dune runtest . -j 20
```

Refresh bounds its provider build/install and external Dune link probe to `-j 20`.
It publishes a private ignored installation and retains old generations. It
does not change the shared opam installation/pin or `asic-dependency.json`.

Historical contract-3 integration verified 2026-10-13: selected generation
`90770d6ce6f04696b3b0082fb3898944`, snapshot SHA-256
`be2db93d3f1b92a8b240167ebadd0b4c0a81484e78356c56cec867f5b19f8e4a`.
After actual activation, library and CLI selected that generation, status reported
`active_is_published` / `active_library_path_is_first` true, and exact
`dune runtest . -j20` passed (18 setup and 11 routing tests, bundle/RTL acceptance).
Provider full forced tests and 53 installed-prefix tests passed. Installed human
and complete JSON inspection of retained placement/observation and accepted
finalization matched domain results; SHA-256 verified 531 retained files unchanged.
The provider's [full closeout](../../hardcaml_asic/docs/development/human-readable-flow-output.md#slice-3--independent-integration-2026-10-13)
records exact paths, commands and output. The recorded dependency pin remains
`1714764859274f80a9f5ad207421a04601824e99`. Re-source in your own shell:

```bash
source /home/wayne/devel/jane/hardcaml_asic_example/.dev/asic/current/activate.sh
```

Current provider interface is CLI contract 4 (package version remains 0.1.0,
persisted records retain their versions). Setup/project dispatch accepts exactly
integer contracts 2, 3 or 4, not arbitrary future versions. The consumer's
`run --endpoint` requires contract 4 before emission; Classic `--stage` retains
its existing behavior on all three. Machine callers must request `--json`;
`stages` journals by default and emits allocation/terminal JSONL, as does
`finalize`. `observation watch` emits reader updates/status JSONL; other observation
queries and inspectors return complete single objects. See the
[ordinary run quickstart](../README.md#explicit-stage-run-and-independent-progress-reader)
and [slice-3 evidence](../../hardcaml_asic/docs/development/flow-journal.md).

Contract-4 activation verified 2026-10-13: generation
`f4c4ae2efeec4e34951102587149f4bc`, captured snapshot SHA256
`33468cfda8fb0845310df2ab7409495b324939cf3a51026d5592f3c9fe8f84da`, observed
provider base `31ad2441ac12ce57123a1f37ed5e2bbf5f508d6c`. Status confirmed both active
selection flags; ocamlfind selected this generation. Exact `dune runtest . -j20`
passed, with 14 routing and 18 dependency tests verified, plus existing RTL/bundle
acceptance. The provider fresh installed-prefix suite passed 55 tests before refresh.
One actual `dune exec -j 20 bin/project.exe -- run --endpoint synthesis --json`
completed exit 0; installed watch attached during preparation, stopped with Ctrl-C
without stopping execution, and reconnected after cursor 2 through final cursor 7.
Stream `45fec45f50b5498192de35d79423b9b8`, attempt
`_flow_results/observations/20261013T184318828201Z_45fec45f`. Curated/raw evidence and
bounded source/pin/global-package nonmutation hashes are in the linked feature record.
The receipt names a local dirty development capture, not a release/source stamp;
evidence documentation was added after capture. The recorded pin remains unchanged.

Historical recovery verified 2026-10-13 (before CLI contract 3): development refresh published generation
`8e42b6dd928842c9b3865b75497ff063`, with receipt at
`.dev/asic/current/receipt.json`. It captured dirty provider bytes at observed
base `ebdcfbfec88cc05f433bec8d289d98b7ad76d4cf`, snapshot checksum
`1ad6407097657acd7160080a7b27a96e0012b753d2703e77e1689d571c96fa4c`.
After activation, library and CLI resolved that generation; exact
`dune runtest . -j 20` and `dune build @all -j 20` exited 0, including compilation
of the stage-recipe companion. These are local receipt facts, not a release stamp.

Recorded mode selects exactly the revision in `asic-dependency.json`. The current
`1714764859274f80a9f5ad207421a04601824e99` lacks the required Project API and is
rejected before publication; use development mode until the owner adopts a
compatible committed revision. Once that record is updated, the command is:

```bash
python3 scripts/asic_dependency.py refresh \
  --source /home/wayne/devel/jane/hardcaml_asic \
  --mode recorded

source .dev/asic/current/activate.sh
```
