# Initial unadapted timing-model attempt — failed

The actual mapped netlist was compiled with the unchanged PDK SRAM functional
models, standard-cell Verilog and UDP library. Compilation exited 0, but Icarus
reported unsupported timing checks and undriven `delayed_CLK`, `delayed_D` and
`delayed_RESET_B` nets. The first read failed with unknown response data:

```text
low byte addr=19 expected=b62f got=xx
```

This directory retains that failed attempt's raw inputs and compiler/replay logs;
it is **not passing gate acceptance**. The adjacent `cfd39c58-functional/` evidence
uses a documented zero-delay used-cell view derived from the same vendor source,
with unchanged gate netlist and unchanged vendor UDP/SRAM functional models.
