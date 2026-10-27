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
    wire [1:0] signal_const_3;
    wire signal_eq;
    wire [1:0] signal_const_4;
    wire signal_eq_1;
    wire signal_or;
    wire signal_and;
    wire signal_and_1;
    wire [1:0] signal_const_5;
    wire signal_eq_2;
    wire signal_and_2;
    reg [7:0] signal_reg;
    wire [15:0] signal_cat;
    reg [15:0] program_behavioral[0:127];
    wire [1:0] signal_const_7;
    wire signal_eq_3;
    wire signal_and_3;
    wire signal_not;
    wire signal_wire;
    wire [7:0] signal_wire_1;
    reg [7:0] signal_reg_1;
    wire [6:0] signal_select_1;
    wire [15:0] signal_mem_read_port;
    wire [1:0] signal_select_2;
    wire signal_eq_4;
    wire [15:0] signal_mux;
    reg [15:0] signal_reg_2;
    wire [7:0] signal_select_3;
    wire [7:0] signal_wire_2;
    wire signal_select_4;
    wire [7:0] signal_mux_1;
    wire signal_wire_3;
    wire signal_wire_4;
    wire signal_and_4;
    wire [7:0] signal_mux_2;
    assign signal_const = 8'b00000000;
    assign signal_select = signal_reg_2[15:8];
    assign signal_const_2 = 16'b0101010101010101;
    assign signal_const_3 = 2'b11;
    assign signal_eq = signal_select_2 == signal_const_3;
    assign signal_const_4 = 2'b00;
    assign signal_eq_1 = signal_select_2 == signal_const_4;
    assign signal_or = signal_eq_1 | signal_eq;
    assign signal_and = signal_and_4 & signal_or;
    assign signal_and_1 = signal_and & signal_eq_4;
    assign signal_const_5 = 2'b10;
    assign signal_eq_2 = signal_select_2 == signal_const_5;
    assign signal_and_2 = signal_and_4 & signal_eq_2;
    always @(posedge signal_wire) begin
        if (signal_not)
            signal_reg <= signal_const;
        else
            if (signal_and_2)
                signal_reg <= signal_wire_1;
    end
    assign signal_cat = { signal_wire_1,
                          signal_reg };
    always @(posedge signal_wire) begin
        if (signal_and_1)
            program_behavioral[signal_select_1] <= signal_cat;
    end
    initial begin
        program_behavioral[0] <= 16'b0101010101010101;
        program_behavioral[1] <= 16'b1010101010101010;
        program_behavioral[2] <= 16'b0101010101010101;
        program_behavioral[3] <= 16'b1010101010101010;
        program_behavioral[4] <= 16'b0101010101010101;
        program_behavioral[5] <= 16'b1010101010101010;
        program_behavioral[6] <= 16'b0101010101010101;
        program_behavioral[7] <= 16'b1010101010101010;
        program_behavioral[8] <= 16'b0101010101010101;
        program_behavioral[9] <= 16'b1010101010101010;
        program_behavioral[10] <= 16'b0101010101010101;
        program_behavioral[11] <= 16'b1010101010101010;
        program_behavioral[12] <= 16'b0101010101010101;
        program_behavioral[13] <= 16'b1010101010101010;
        program_behavioral[14] <= 16'b0101010101010101;
        program_behavioral[15] <= 16'b1010101010101010;
        program_behavioral[16] <= 16'b0101010101010101;
        program_behavioral[17] <= 16'b1010101010101010;
        program_behavioral[18] <= 16'b0101010101010101;
        program_behavioral[19] <= 16'b1010101010101010;
        program_behavioral[20] <= 16'b0101010101010101;
        program_behavioral[21] <= 16'b1010101010101010;
        program_behavioral[22] <= 16'b0101010101010101;
        program_behavioral[23] <= 16'b1010101010101010;
        program_behavioral[24] <= 16'b0101010101010101;
        program_behavioral[25] <= 16'b1010101010101010;
        program_behavioral[26] <= 16'b0101010101010101;
        program_behavioral[27] <= 16'b1010101010101010;
        program_behavioral[28] <= 16'b0101010101010101;
        program_behavioral[29] <= 16'b1010101010101010;
        program_behavioral[30] <= 16'b0101010101010101;
        program_behavioral[31] <= 16'b1010101010101010;
        program_behavioral[32] <= 16'b0101010101010101;
        program_behavioral[33] <= 16'b1010101010101010;
        program_behavioral[34] <= 16'b0101010101010101;
        program_behavioral[35] <= 16'b1010101010101010;
        program_behavioral[36] <= 16'b0101010101010101;
        program_behavioral[37] <= 16'b1010101010101010;
        program_behavioral[38] <= 16'b0101010101010101;
        program_behavioral[39] <= 16'b1010101010101010;
        program_behavioral[40] <= 16'b0101010101010101;
        program_behavioral[41] <= 16'b1010101010101010;
        program_behavioral[42] <= 16'b0101010101010101;
        program_behavioral[43] <= 16'b1010101010101010;
        program_behavioral[44] <= 16'b0101010101010101;
        program_behavioral[45] <= 16'b1010101010101010;
        program_behavioral[46] <= 16'b0101010101010101;
        program_behavioral[47] <= 16'b1010101010101010;
        program_behavioral[48] <= 16'b0101010101010101;
        program_behavioral[49] <= 16'b1010101010101010;
        program_behavioral[50] <= 16'b0101010101010101;
        program_behavioral[51] <= 16'b1010101010101010;
        program_behavioral[52] <= 16'b0101010101010101;
        program_behavioral[53] <= 16'b1010101010101010;
        program_behavioral[54] <= 16'b0101010101010101;
        program_behavioral[55] <= 16'b1010101010101010;
        program_behavioral[56] <= 16'b0101010101010101;
        program_behavioral[57] <= 16'b1010101010101010;
        program_behavioral[58] <= 16'b0101010101010101;
        program_behavioral[59] <= 16'b1010101010101010;
        program_behavioral[60] <= 16'b0101010101010101;
        program_behavioral[61] <= 16'b1010101010101010;
        program_behavioral[62] <= 16'b0101010101010101;
        program_behavioral[63] <= 16'b1010101010101010;
        program_behavioral[64] <= 16'b0101010101010101;
        program_behavioral[65] <= 16'b1010101010101010;
        program_behavioral[66] <= 16'b0101010101010101;
        program_behavioral[67] <= 16'b1010101010101010;
        program_behavioral[68] <= 16'b0101010101010101;
        program_behavioral[69] <= 16'b1010101010101010;
        program_behavioral[70] <= 16'b0101010101010101;
        program_behavioral[71] <= 16'b1010101010101010;
        program_behavioral[72] <= 16'b0101010101010101;
        program_behavioral[73] <= 16'b1010101010101010;
        program_behavioral[74] <= 16'b0101010101010101;
        program_behavioral[75] <= 16'b1010101010101010;
        program_behavioral[76] <= 16'b0101010101010101;
        program_behavioral[77] <= 16'b1010101010101010;
        program_behavioral[78] <= 16'b0101010101010101;
        program_behavioral[79] <= 16'b1010101010101010;
        program_behavioral[80] <= 16'b0101010101010101;
        program_behavioral[81] <= 16'b1010101010101010;
        program_behavioral[82] <= 16'b0101010101010101;
        program_behavioral[83] <= 16'b1010101010101010;
        program_behavioral[84] <= 16'b0101010101010101;
        program_behavioral[85] <= 16'b1010101010101010;
        program_behavioral[86] <= 16'b0101010101010101;
        program_behavioral[87] <= 16'b1010101010101010;
        program_behavioral[88] <= 16'b0101010101010101;
        program_behavioral[89] <= 16'b1010101010101010;
        program_behavioral[90] <= 16'b0101010101010101;
        program_behavioral[91] <= 16'b1010101010101010;
        program_behavioral[92] <= 16'b0101010101010101;
        program_behavioral[93] <= 16'b1010101010101010;
        program_behavioral[94] <= 16'b0101010101010101;
        program_behavioral[95] <= 16'b1010101010101010;
        program_behavioral[96] <= 16'b0101010101010101;
        program_behavioral[97] <= 16'b1010101010101010;
        program_behavioral[98] <= 16'b0101010101010101;
        program_behavioral[99] <= 16'b1010101010101010;
        program_behavioral[100] <= 16'b0101010101010101;
        program_behavioral[101] <= 16'b1010101010101010;
        program_behavioral[102] <= 16'b0101010101010101;
        program_behavioral[103] <= 16'b1010101010101010;
        program_behavioral[104] <= 16'b0101010101010101;
        program_behavioral[105] <= 16'b1010101010101010;
        program_behavioral[106] <= 16'b0101010101010101;
        program_behavioral[107] <= 16'b1010101010101010;
        program_behavioral[108] <= 16'b0101010101010101;
        program_behavioral[109] <= 16'b1010101010101010;
        program_behavioral[110] <= 16'b0101010101010101;
        program_behavioral[111] <= 16'b1010101010101010;
        program_behavioral[112] <= 16'b0101010101010101;
        program_behavioral[113] <= 16'b1010101010101010;
        program_behavioral[114] <= 16'b0101010101010101;
        program_behavioral[115] <= 16'b1010101010101010;
        program_behavioral[116] <= 16'b0101010101010101;
        program_behavioral[117] <= 16'b1010101010101010;
        program_behavioral[118] <= 16'b0101010101010101;
        program_behavioral[119] <= 16'b1010101010101010;
        program_behavioral[120] <= 16'b0101010101010101;
        program_behavioral[121] <= 16'b1010101010101010;
        program_behavioral[122] <= 16'b0101010101010101;
        program_behavioral[123] <= 16'b1010101010101010;
        program_behavioral[124] <= 16'b0101010101010101;
        program_behavioral[125] <= 16'b1010101010101010;
        program_behavioral[126] <= 16'b0101010101010101;
        program_behavioral[127] <= 16'b1010101010101010;
    end
    assign signal_const_7 = 2'b01;
    assign signal_eq_3 = signal_select_2 == signal_const_7;
    assign signal_and_3 = signal_and_4 & signal_eq_3;
    assign signal_not = ~ signal_wire_3;
    assign signal_wire = clk;
    assign signal_wire_1 = uio_in;
    always @(posedge signal_wire) begin
        if (signal_not)
            signal_reg_1 <= signal_const;
        else
            if (signal_and_3)
                signal_reg_1 <= signal_wire_1;
    end
    assign signal_select_1 = signal_reg_1[6:0];
    assign signal_mem_read_port = program_behavioral[signal_select_1];
    assign signal_select_2 = signal_wire_2[1:0];
    assign signal_eq_4 = signal_select_2 == signal_const_3;
    assign signal_mux = signal_eq_4 ? signal_const_2 : signal_mem_read_port;
    always @(posedge signal_wire) begin
        if (signal_and)
            signal_reg_2 <= signal_mux;
    end
    assign signal_select_3 = signal_reg_2[7:0];
    assign signal_wire_2 = ui_in;
    assign signal_select_4 = signal_wire_2[2:2];
    assign signal_mux_1 = signal_select_4 ? signal_select : signal_select_3;
    assign signal_wire_3 = rst_n;
    assign signal_wire_4 = ena;
    assign signal_and_4 = signal_wire_4 & signal_wire_3;
    assign signal_mux_2 = signal_and_4 ? signal_mux_1 : signal_const;
    assign uo_out = signal_mux_2;
    assign uio_out = signal_const;
    assign uio_oe = signal_const;

endmodule
