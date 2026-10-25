(* blackbox *)
module RM_IHPSG13_1P_256x16_c2_bm_bist (
input A_CLK, A_MEN, A_WEN, A_REN,
input [7:0] A_ADDR,
input [15:0] A_DIN,
input A_DLY,
output [15:0] A_DOUT,
input [15:0] A_BM,
input A_BIST_CLK, A_BIST_EN, A_BIST_MEN, A_BIST_WEN, A_BIST_REN,
input [7:0] A_BIST_ADDR,
input [15:0] A_BIST_DIN, A_BIST_BM
);
endmodule
