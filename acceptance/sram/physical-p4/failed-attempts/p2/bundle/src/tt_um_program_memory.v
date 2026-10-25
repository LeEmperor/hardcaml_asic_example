module tt_um_program_memory (
    ui_in,
    uio_in,
    ena,
    clk,
    rst_n,
    uo_out,
    uio_out,
    uio_oe
);

    input [7:0] ui_in;
    input [7:0] uio_in;
    input ena;
    input clk;
    input rst_n;
    output [7:0] uo_out;
    output [7:0] uio_out;
    output [7:0] uio_oe;

    wire [7:0] signal_const;
    wire [7:0] signal_select;
    wire [15:0] signal_const_2;
    wire gnd;
    wire [15:0] signal_const_5;
    wire vdd;
    wire [1:0] signal_const_6;
    wire signal_eq;
    wire signal_and;
    reg [7:0] signal_reg;
    wire [15:0] signal_cat;
    wire [1:0] signal_const_8;
    wire signal_eq_1;
    wire signal_and_1;
    wire signal_not;
    wire [7:0] signal_wire;
    reg [7:0] signal_reg_1;
    wire signal_not_1;
    wire signal_and_2;
    wire [1:0] signal_const_10;
    wire signal_eq_2;
    wire signal_and_3;
    wire signal_eq_3;
    wire [1:0] signal_const_12;
    wire [1:0] signal_select_1;
    wire signal_eq_4;
    wire signal_or;
    wire signal_and_4;
    wire signal_wire_1;
    wire [15:0] signal_inst;
    wire [15:0] signal_wire_2;
    wire [7:0] signal_select_2;
    wire [7:0] signal_wire_3;
    wire signal_select_3;
    wire [7:0] signal_mux;
    wire signal_wire_4;
    wire signal_wire_5;
    wire signal_and_5;
    wire [7:0] signal_mux_1;
    assign signal_const = 8'b00000000;
    assign signal_select = signal_wire_2[15:8];
    assign signal_const_2 = 16'b0000000000000000;
    assign gnd = 1'b0;
    assign signal_const_5 = 16'b1111111111111111;
    assign vdd = 1'b1;
    assign signal_const_6 = 2'b10;
    assign signal_eq = signal_select_1 == signal_const_6;
    assign signal_and = signal_and_5 & signal_eq;
    always @(posedge signal_wire_1) begin
        if (signal_not)
            signal_reg <= signal_const;
        else
            if (signal_and)
                signal_reg <= signal_wire;
    end
    assign signal_cat = { signal_wire,
                          signal_reg };
    assign signal_const_8 = 2'b01;
    assign signal_eq_1 = signal_select_1 == signal_const_8;
    assign signal_and_1 = signal_and_5 & signal_eq_1;
    assign signal_not = ~ signal_wire_4;
    assign signal_wire = uio_in;
    always @(posedge signal_wire_1) begin
        if (signal_not)
            signal_reg_1 <= signal_const;
        else
            if (signal_and_1)
                signal_reg_1 <= signal_wire;
    end
    assign signal_not_1 = ~ signal_eq_2;
    assign signal_and_2 = signal_and_4 & signal_not_1;
    assign signal_const_10 = 2'b11;
    assign signal_eq_2 = signal_select_1 == signal_const_10;
    assign signal_and_3 = signal_and_4 & signal_eq_2;
    assign signal_eq_3 = signal_select_1 == signal_const_10;
    assign signal_const_12 = 2'b00;
    assign signal_select_1 = signal_wire_3[1:0];
    assign signal_eq_4 = signal_select_1 == signal_const_12;
    assign signal_or = signal_eq_4 | signal_eq_3;
    assign signal_and_4 = signal_and_5 & signal_or;
    assign signal_wire_1 = clk;
    RM_IHPSG13_1P_256x16_c2_bm_bist
        hc_resource_7_program
        ( .A_CLK(signal_wire_1),
          .A_MEN(signal_and_4),
          .A_WEN(signal_and_3),
          .A_REN(signal_and_2),
          .A_ADDR(signal_reg_1),
          .A_DIN(signal_cat),
          .A_DLY(vdd),
          .A_BM(signal_const_5),
          .A_BIST_CLK(gnd),
          .A_BIST_EN(gnd),
          .A_BIST_MEN(gnd),
          .A_BIST_WEN(gnd),
          .A_BIST_REN(gnd),
          .A_BIST_ADDR(signal_const),
          .A_BIST_DIN(signal_const_2),
          .A_BIST_BM(signal_const_2),
          .A_DOUT(signal_inst[15:0]) );
    assign signal_wire_2 = signal_inst;
    assign signal_select_2 = signal_wire_2[7:0];
    assign signal_wire_3 = ui_in;
    assign signal_select_3 = signal_wire_3[2:2];
    assign signal_mux = signal_select_3 ? signal_select : signal_select_2;
    assign signal_wire_4 = rst_n;
    assign signal_wire_5 = ena;
    assign signal_and_5 = signal_wire_5 & signal_wire_4;
    assign signal_mux_1 = signal_and_5 ? signal_mux : signal_const;
    assign uo_out = signal_mux_1;
    assign uio_out = signal_const;
    assign uio_oe = signal_const;

endmodule
