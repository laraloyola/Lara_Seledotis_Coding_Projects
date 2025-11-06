module UMBRELLA(input logic [1:0]KEY, //reset clk (BUTTONS) (activelow)
					 input logic [5:0]SW, //north, east, south, west, up, down (SWITCHES)
					 output logic [3:0]LEDG, //e1, e2, fn0, fn1 
					 output logic [2:0]LEDR, //w1, w2, V
					 output logic [6:0]HEX7, HEX6, HEX5, HEX4, HEX3, HEX2, HEX1, HEX0); // decoder
					 //HEX3[6:0] through HEX0[6:0] decoded location state
					 //HEX5[6:0] through HEX4[6:0] decoded elevator state
					 //HEX7[6:0] and HEX6[6:0] decoded weapons state
					 //LEDG[0] - LEDG[3] - e1, e2, fn0, fn1
					 //LEDR[0] - LEDR[2] - w1, w2, V
					 
					 // create local variables to store data from fsm to fsm
					 logic E1, E2, FN0, FN1, W1, W2, V; 
					 logic [7:0]LOC_STATE; 
					 logic [2:0]ELEVATOR_STATE; 
					 logic [2:0]WEAPON_STATE; 
					 
					 // MAPS OUR OUTPUTS TO LEDS
					 assign LEDG[0] = E1; 
					 assign LEDG[1] = E2; 
					 assign LEDG[2] = FN0;
					 assign LEDG[3] = FN1; 
					 assign LEDR[0] = W1; 
					 assign LEDR[1] = W2; 
					 assign LEDR[2] = V; // output on showing V = 1
					 
// debug switches for decoders 
				/*	
					always_comb 
					if (SW[2] == 0 & SW[1] == 0 & SW[0] == 1) begin
						weapon_state_global[2:0] = 3'b001; // weapon decoder works 
						// checking if weapons fsm works
						elevator_state_global[2:0] = 3'b001; 
						loc_state_global[7:0] = 8'b0000_0001; 
						end
					else if (SW[2] == 0 & SW[1] == 1 & SW[0] == 0) begin
						weapon_state_global[2:0] = 3'b010;
						elevator_state_global[2:0] = 3'b010;
						loc_state_global[7:0] = 8'b0000_0010;
						end
					else if (SW[2] == 1 & SW[1] == 0 & SW[0] == 0) begin
						weapon_state_global[2:0] = 3'b100;
						elevator_state_global[2:0] = 3'b100;
						loc_state_global[7:0] = 8'b0000_0100;
						end
					else if (SW[2] == 0 & SW[1] == 1 & SW[0] == 1) begin
					weapon_state_global[2:0] = 3'b000; 
						elevator_state_global[2:0] = 3'b000;
						loc_state_global[7:0] = 8'b0000_1000;
					end	
					else if (SW[2] == 1 & SW[1] == 0 & SW[0] == 1) begin
					weapon_state_global[2:0] = 3'b000; 
						elevator_state_global[2:0] = 3'b000;
						loc_state_global[7:0] = 8'b0001_0000;
					end
					else if (SW[2] == 1 & SW[1] == 1 & SW[0] == 0) begin
					weapon_state_global[2:0] = 3'b000; 
						elevator_state_global[2:0] = 3'b000;
						loc_state_global[7:0] = 8'b0010_0000;
					end
					else if (SW[2] == 1 & SW[1] == 1 & SW[0] == 1) begin
					weapon_state_global[2:0] = 3'b000; 
						elevator_state_global[2:0] = 3'b000;
						loc_state_global[7:0] = 8'b0100_0000;
					end
					else if (SW[2] == 0 & SW[1] == 0 & SW[0] == 0) begin
					weapon_state_global[2:0] = 3'b000; 
						elevator_state_global[2:0] = 3'b000;
						loc_state_global[7:0] = 8'b1000_0000;
					end
					else begin
				   	weapon_state_global[2:0] = 3'b000; 
						elevator_state_global[2:0] = 3'b000;
						loc_state_global[7:0] = 8'b0000_0000;
						end
					*/
// CREATE ALL OF OUR FSMS
					 // weapons
//// testing our fsms 
	/*				always_comb
						if (SW[0] == 0 & SW[1] == 0) begin
							W1 = 0; 
							W2 = 0; // output should be NW
							end 
						else if (SW[0] == 1 & SW[1] == 0) begin
							W1 = 1; 
							W2 = 0; // output should be OW
							end
						else if (SW[0] == 1 & SW[1] == 1) begin
							W1 = 1; 
							W2 = 1; // output BW
							end
						else begin
							W1 = 0; 
							W2 = 0; // output should be NW
						end
					*/
// end fsm testing

// instantiating our sub-modules in the top module
// reset is active low so pass ~KEY[0] to each module, that way if reset == 0 ~reset == 1 and the system will reset, 
					 WEAPONS_FSM mod3(~KEY[0], KEY[1], // reset, clk
					 W1, W2, // input from location
					 V, // output to location
					 WEAPON_STATE[2:0]); // output to weapons_decode fsm
					 
					 // elevator
					 ELEVATOR_FSM mod2(~KEY[0], KEY[1], // reset, clk, buttons
					 SW[5], SW[4], //ud switches
					 E1, E2, // input to elevator fsm
					 FN0, FN1, // output to location
					 ELEVATOR_STATE[2:0]);
					 
					 //location
					 LOCATION_FSM mod1(~KEY[0], KEY[1], // reset, clk, buttons
					 SW[3], SW[2], SW[1], SW[0], SW[5], SW[4], //nesw ud switches
					 FN0, FN1, // input to location
					 V, // input to location from weapons
					 WEAPON_STATE[2:0],
					 E1, E2, // output to elevator fsm
					 W1, W2, // output to weapons
					 LOC_STATE[7:0]); 
					 
					 //decoders
					 //loc_decode
					 LOC_DECODE mod4(LOC_STATE[7:0], 
					 HEX0[6:0], HEX1[6:0], HEX2[6:0], HEX3[6:0]);
					 
					 //elevator_decode
					 ELEVATOR_DECODE mod5(ELEVATOR_STATE[2:0], 
					 HEX4[6:0], HEX5[6:0]); 
					 
					 //weapons decode
					 WEAPON_DECODE mod6(WEAPON_STATE[2:0], 
					 HEX6[6:0], HEX7[6:0]);	
					 
endmodule
// first module
/*
	Location FSM uses asynchronous reset and goes through all the different states, outputs LOC_STATE to decoder and W1, w2 to weapons fsm, 
	and e1, e2 to elevator fsm. runs on clock cycle. input are from elevato9r fsm and weapons and top module. 
	also imported weapon_state to determine where the weapons state is at for the WIN/LOSE states (UAW UAL)
*/
module LOCATION_FSM(input logic RESET, CLOCK, //from top module
						  input logic NORTH, EAST, SOUTH, WEST, UP, DOWN, //from top module
						  input logic FN0, FN1, // from elevator fsm
						  input logic V, // input from weaponsFSM
						  input logic [2:0] WEAPON_STATE,
						  output logic E1, E2,  // to elevator fsm
						  output logic W1, W2, // to weapons fsm
						  output logic [7:0]LOC_STATE); // to LOC_DECODE fsm
						  
//state encodings
typedef enum logic [7:0] {EA = 8'b0000_0001, L = 8'b0000_0010, EB = 8'b0000_0100, WBS = 8'b0000_1000, ST = 8'b0001_0000, 
EC = 8'b0010_0000, UAW = 8'b0100_0000, UAL = 8'b1000_0000} statetype;	 
//(*fsm_encoding = "one_hot"*)
statetype state, nextstate; 

//state register (asynchronous reset)
always_ff @ (posedge CLOCK, posedge RESET) // INPUT ACTIVELOW?
	if (RESET) state <= EA; // does ~reset cause issues? check with Dr. Streeter
	else		  state <= nextstate; 

// next state logic
always_comb
	case (state) 
		EA: 
		begin
		    if (NORTH) nextstate = L;
			 else if (~FN1 & FN0 & UP) nextstate = EB;
			 else nextstate = EA; 
	   end 	
		L: 
		begin
		    if (SOUTH) nextstate = EA;
			 else nextstate = L; 
	   end 
		EB:
		begin
			if (~FN0 & DOWN & FN1) nextstate = EA; 
			else if (WEST) nextstate = WBS;
			else if (NORTH) nextstate = ST;
			else if (FN1 & UP & ~FN0) nextstate = EC;
			else nextstate = EB; 
		end
		WBS:
		begin
			if (EAST) nextstate = EB; 
			else nextstate = WBS; 
		end
		ST:
		begin
			if (SOUTH) nextstate = EB; 
			else nextstate = ST; 
		end
		EC:
		begin
		if (WEAPON_STATE[2:0] == 3'b100) // means Bo state
			nextstate = UAW;
		else nextstate = UAL;
				//if (V & FN1 & FN0) nextstate = UAW; 
				//	else nextstate = UAL; 
		end
		UAL:
		begin
			nextstate = UAL; // set it this way or "if (UAL) nextstate = UAL;"
		end
		UAW: 
		begin
			nextstate = UAW; 
		end	
		default: nextstate = EA; 
	endcase					  
		// output logic
	assign E1 = (state == EA); // does this set equal to 1 or set equal to bit vector?
	assign W2 = (state == L); // output to weapons
	assign E2 = (state == EB); /// output to elevator
	assign W1 = (state == WBS); // 
	assign LOSE = (state == UAL); //these don't go anywhere
	assign WIN = (state == UAW); 
	assign LOC_STATE[7:0] = state; // send to decoder
endmodule
// elevator fsm uses reset, clock, up, down input from top
// takes input of e1, e2 from location
module ELEVATOR_FSM(input logic RESET, CLOCK, 
						  input logic UP, DOWN, 
						  input logic E1, E2, 
						  output logic FN0, FN1, 
						  output logic [2:0]ELEVATOR_STATE); 
		// state encodings
		typedef enum logic [2:0] {FA = 3'b001, FB = 3'b010, FC = 3'b100} statetype; 
		//(*fsm_encoding = "one_hot"*)
		statetype state, nextstate; 
		// state register (asynchronous reset)
		always_ff @ (posedge CLOCK, posedge RESET)
			if (RESET) state <= FA; 
			else state <= nextstate; 
		// next state logic
		always_comb
			case (state)
				FA:
				begin
					if (E1 & UP) nextstate = FB; 
					else nextstate = FA; 
				end
				FB:
				begin
					if (E2 & DOWN) nextstate = FA; 
					else if (E2 & UP) nextstate = FC; 
					else nextstate = FB; 
				end
				FC:
				begin
					if (FC) nextstate = FC; 
				end
				default: nextstate = FA;
			endcase
			//output logic
			assign FN1 = ((state == FB) | (state == FC));
			assign FN0 = ((state == FA) | (state == FC));
			assign ELEVATOR_STATE[2:0] = state; 
		
endmodule
// weapons fsm takes input reset, clock from top. input w1, w2 from location, outputs V to location and weapon state to decoder
module WEAPONS_FSM(input logic RESET, CLOCK,
						 input logic W1, W2, 
						 output logic V, 
						 output logic [2:0]WEAPON_STATE);
// state encodings
		typedef enum logic [2:0] {NW = 3'b001, OW = 3'b010, BW = 3'b100} statetype; 
		//(*fsm_encoding = "one_hot"*)
		statetype state, nextstate; 
		logic will_lose; 
// state register (asynchronous reset)
		always_ff @ (posedge CLOCK, posedge RESET)
			if (RESET) state <= NW; 
			else state <= nextstate; 
		always_comb
			case (state)
				NW: 
				begin 
					if (W1) 
						nextstate = OW;
					else nextstate = NW; // else is both W zero
				end
				OW:
				begin 
					if (W2) nextstate = BW;
					else nextstate = OW;
				end
				BW:
				begin
					 nextstate = BW;
				end
				default: nextstate = NW;
			endcase
		// output logic
		assign V = (state == BW);
		assign WEAPON_STATE[2:0] = (state);
		 
		 
endmodule
// decoders take input from their respective fsm to determine which state they are in
// and use a series of binary values to display on decoder. outputs are HEX0-HEX3 which are pin maped to 7 segment display
module LOC_DECODE(input logic [7:0]LOC_STATE, 
						output logic [6:0]HEX0, 
						output logic [6:0]HEX1, 
						output logic [6:0]HEX2, 
						output logic [6:0]HEX3);
			// local variables to check where LOC_STATE is
				logic [7:0]s0, s1, s2, s3, s4, s5, s6, s7;
				assign s0 = 8'b0000_0001, s1 = 8'b0000_0010, s2 = 8'b0000_0100, s3 = 8'b0000_1000,
				s4 = 8'b0001_0000, s5 = 8'b0010_0000, s6 = 8'b0100_0000, s7 = 8'b1000_0000; 
				// combinational logic for decoder
				always_comb
					if (LOC_STATE == s0)
						begin
							HEX3[6:0] = 7'b111_1111; // nothing lit up
							HEX2[6:0] = 7'b111_1111; // nothing lit up
							HEX1[6:0] = 7'b0000_110; // b c unlit
							HEX0[6:0] = 7'b0001_000; // d unlit
						end
					else if (LOC_STATE == s1)
						begin
							HEX3[6:0] = 7'b100_0111; // f, e, d lit
							HEX2[6:0] = 7'b000_0011; // a, b unlit
							HEX1[6:0] = 7'b000_0011; // a, b unlit
							HEX0[6:0] = 7'b0011_001; // d, e, a unlit
						end
					else if (LOC_STATE == s2)
						begin
							HEX3[6:0] = 7'b111_1111; // nothing lit up
							HEX2[6:0] = 7'b111_1111; // nothing lit up
							HEX1[6:0] = 7'b000_0110; // b, c unlit
							HEX0[6:0] = 7'b000_0011; // a, b unlit
						end
					else if (LOC_STATE == s3)
						begin
							HEX3[6:0] = 7'b001_0010; // b, e unlit
							HEX2[6:0] = 7'b000_0110; // b, c unlit
							HEX1[6:0] = 7'b010_0111; // e, g, d lit
							HEX0[6:0] = 7'b000_1111; // f, e, g lit
						end
					else if (LOC_STATE == s4)
						begin
							HEX3[6:0] = 7'b011_0000; // f, e unlit 
							HEX2[6:0] = 7'b000_1111; // f, g, e lit
							HEX1[6:0] = 7'b000_0011; // a, b unlit
							HEX0[6:0] = 7'b001_0010; // b, e unlit
						end
					else if (LOC_STATE == s5)
						begin
							HEX3[6:0] = 7'b111_1111; // nothing lit up
							HEX2[6:0] = 7'b111_1111; // nothing lit up
							HEX1[6:0] = 7'b000_0110; // b, c unlit
							HEX0[6:0] = 7'b100_0110; // b, c, g unlit
						end
					else if (LOC_STATE == s6)
						begin
							HEX3[6:0] = 7'b111_1111; // nothing lit up
							HEX2[6:0] = 7'b011_0000; // f, e unlit
							HEX1[6:0] = 7'b111_1001; //b, c lit
							HEX0[6:0] = 7'b010_1011; // g, e, c lit
						end
					else if (LOC_STATE == s7)
						begin
							HEX3[6:0] = 7'b100_0111; // f, e, d lit
							HEX2[6:0] = 7'b100_0000; // g unlit
							HEX1[6:0] = 7'b001_0010; // b, e unlit
							HEX0[6:0] = 7'b000_0110; // b, c unlit
						end
					else 
						begin
							HEX3[6:0] = 7'b111_1111; // nothing lit up
							HEX2[6:0] = 7'b111_1111; // nothing lit up
							HEX1[6:0] = 7'b0000_110; // b c unlit
							HEX0[6:0] = 7'b0001_000; // d unlit
						end
endmodule

module ELEVATOR_DECODE(input logic [2:0]ELEVATOR_STATE, 
							  output logic [6:0]HEX4, 
							  output logic [6:0]HEX5); 
	// local variables to compare elevator_state to for decoder						  
	logic [2:0]s0, s1, s2;
	assign s0 = 3'b001, s1 = 3'b010, s2 = 3'b100; 
		always_comb 
			if (ELEVATOR_STATE == s0) // input this so that it corresponds
				begin
					 HEX5[6:0] = 7'b000_1110; // b, c, d unlit
					 HEX4[6:0] = 7'b000_1000; // d unlit
				end
			else if (ELEVATOR_STATE == s1)
				begin
					HEX5[6:0] = 7'b000_1110; // b, c, d unlit
					HEX4[6:0] = 7'b000_0000; // all lit
				end
			else if (ELEVATOR_STATE == s2)
				begin
					HEX5[6:0] = 7'b000_1110; // b, c, d unlit
					HEX4[6:0] = 7'b100_0110; // b, g, c unlit 
				end
			else 
				begin
					HEX5[6:0] = 7'b000_1110; // b, c, d unlit
					HEX4[6:0] = 7'b000_1000; // d unlit
				end 
endmodule

module WEAPON_DECODE(input logic [2:0]WEAPON_STATE, 
							output logic [6:0]HEX6, 
							output logic [6:0]HEX7); 
		// local variables 
		logic [2:0]s0, s1, s2; 
		assign s0 = 3'b001, s1 = 3'b010, s2 = 3'b100; 
		always_comb
				if (WEAPON_STATE == s0)
				begin
					HEX7[6:0] = 7'b1_000000; // zero, only g unlit
					HEX6[6:0] = 7'b1111_00_1; // one, only b and c lit
				end
				else if (WEAPON_STATE == s1)
				begin
					HEX7[6:0] = 7'b1_000000; // zero, only g unlit
					HEX6[6:0] = 7'b0_1_00_1_00; // 2, only c and f unlit
				end
				else if (WEAPON_STATE == s2)
				begin
					HEX7[6:0] = 7'b00000_11; // b, only a and b unlit
					HEX6[6:0] = 7'b0_1_000_11; // 2, only f a b unlit
				end
				else 
				begin
					HEX7[6:0] = 7'b1_000000; // zero, only g unlit
					HEX6[6:0] = 7'b1111_00_1; // one, only b and c lit
				end                                                                                                                                                                                                                                                                                                                                 

endmodule




