# Final corrected-provider acceptance

The authoritative passing result is **`verified/receipt.json`**: 20 tests passed,
0 failures/errors/skips, using corrected provider generation
`dd1ec9002cdc40f2936488cedd9eb0fe`.

The parent `receipt.json` and numbered outputs retain the initial corrected-provider
attempt: its sole failure was an obsolete harness assumption that an undefined
wrong-type module would yield a complete `unexpected_instances` inventory. The
corrected provider rejects that module before complete inventory construction.
The final harness instead asserts unresolved evidence, unavailable realization,
and the precise non-leaf/non-library parser reason. No ASIC change was needed.

Old `../installed-04/` remains preserved and explicitly superseded. Final capture,
build, FIFO and full-suite logs are `../*-final.*`; the final closeout is
`../closeout-final.json`. All 276 original historical SRAM files remain unchanged.
