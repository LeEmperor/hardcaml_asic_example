// Copyright 2024 IHP PDK Authors
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//    https://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


`timescale 1ns/1ps
// Reviewed zero-delay functional view; not SDF/timing evidence.

module sg13cmos5l_a21oi_1 (Y, A1, A2, B1);
		
	output Y;
	input A1, A2, B1;

	// Function

	wire int_fwire_0, int_fwire_1;

	and (int_fwire_0, A1, A2);
	or (int_fwire_1, int_fwire_0, B1);
	not (Y, int_fwire_1);
        
	// Timing

	


endmodule
module sg13cmos5l_and2_1 (X, A, B);
		
	output X;
	input A, B;

	// Function

	and (X, A, B);

        // Timing

	


endmodule
module sg13cmos5l_and3_1 (X, A, B, C);
		
	output X;
	input A, B, C;

	// Function

	and (X, A, B, C);

        // Timing

	


endmodule
module sg13cmos5l_buf_1 (X, A);
		
	output X;
	input A;

	// Function

	buf (X, A);

        // Timing

	


endmodule
module sg13cmos5l_buf_2 (X, A);
		
	output X;
	input A;

	// Function

	buf (X, A);

        // Timing

	


endmodule
module sg13cmos5l_buf_4 (X, A);
		
	output X;
	input A;

	// Function

	buf (X, A);

        // Timing

	


endmodule
module sg13cmos5l_buf_8 (X, A);
		
	output X;
	input A;

	// Function

	buf (X, A);

        // Timing

	


endmodule
module sg13cmos5l_decap_4 ();

        // Timing

	


endmodule
module sg13cmos5l_decap_8 ();

        // Timing

	


endmodule
module sg13cmos5l_dfrbpq_1 (Q, CLK, D, RESET_B);
		
	output Q;
	input CLK, D, RESET_B;
	reg notifier;
	wire delayed_D, delayed_RESET_B, delayed_CLK;

	// Function
	wire int_fwire_IQ, int_fwire_r, xcr_0;

	not (int_fwire_r, delayed_RESET_B);
	buf (xcr_0, 0);
	ihp_dff_r (int_fwire_IQ, notifier, delayed_CLK, delayed_D, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);

        // Timing

	

assign delayed_CLK = CLK;
assign delayed_D = D;
assign delayed_RESET_B = RESET_B;
endmodule
module sg13cmos5l_dlygate4sd3_1 (X, A);
		
	output X;
	input A;

	// Function

	buf (X, A);

        // Timing

	


endmodule
module sg13cmos5l_fill_1 ();
 
       // Timing

	


endmodule
module sg13cmos5l_fill_2 ();

        // Timing

	


endmodule
module sg13cmos5l_inv_1 (Y, A);
		
	output Y;
	input A;

	// Function

	not (Y, A);

        // Timing

	


endmodule
module sg13cmos5l_mux2_1 (X, A0, A1, S);
		
	output X;
	input A0, A1, S;

	// Function

	ihp_mux2 (X, A0, A1, S);

        // Timing

	


endmodule
module sg13cmos5l_nand2_1 (Y, A, B);
		
	output Y;
	input A, B;

	// Function

	wire int_fwire_0;

	and (int_fwire_0, A, B);
	not (Y, int_fwire_0);

        // Timing

	


endmodule
module sg13cmos5l_nor2_1 (Y, A, B);
		
	output Y;
	input A, B;

	// Function

	wire int_fwire_0;

	or (int_fwire_0, A, B);
	not (Y, int_fwire_0);

        // Timing

	


endmodule
module sg13cmos5l_nor2b_1 (Y, A, B_N);
		
	output Y;
	input A, B_N;

	// Function

	wire B_N__bar, int_fwire_0;

	not (B_N__bar, B_N);
	or (int_fwire_0, A, B_N__bar);
	not (Y, int_fwire_0);

        // Timing

	


endmodule
module sg13cmos5l_nor3_1 (Y, A, B, C);
		
	output Y;
	input A, B, C;

	// Function

	wire int_fwire_0;

	or (int_fwire_0, A, B, C);
	not (Y, int_fwire_0);

        // Timing

	


endmodule
module sg13cmos5l_o21ai_1 (Y, A1, A2, B1);
		
	output Y;
	input A1, A2, B1;

	// Function

	wire int_fwire_0, int_fwire_1;

	or (int_fwire_0, A1, A2);
	and (int_fwire_1, int_fwire_0, B1);
	not (Y, int_fwire_1);

        // Timing

	


endmodule
module sg13cmos5l_tiehi (L_HI);
		
	output L_HI;

	// Function

	buf (L_HI, 1'b1);

        // Timing

	


endmodule
module sg13cmos5l_tielo (L_LO);
		
	output L_LO;

	// Function

	buf (L_LO, 1'b0);

        // Timing

	


endmodule
module sg13cmos5l_xor2_1 (X, A, B);
		
	output X;
	input A, B;

	// Function

	xor (X, A, B);

        // Timing

	


endmodule