module testbench();
	logic [3:0]ALU_CTL;
	logic [7:0]A, B, Z, FLAGS;
	logic clk, reset; // clock (reset not included)
	logic [7:0]FLAGS_Expected, Z_Expected;
	// expected vs compare
	// records number of testvector and error
	logic [31:0] vectornum, errors;
	logic [7:0] testvectors[70:0]; //column, row (is it 8 columns or extra including underscores?)
	
	//instantiate dut
	ALU dut(ALU_CTL, A, B, Z, FLAGS);
	
	// generate clock
	always
		begin
			clk = 1; #5; clk = 0; #5;
		end
	
	// start of test, load vectors in
	initial 
		begin
			$readmemh("testvectors.tv", testvectors);
			vectornum = 0; errors = 0;
			// no reset?
		end
	// apply testvectors on rising edge of clock
	always @(posedge clk)
		begin
			#1; {ALU_CTL, A, B, Z, Z_Expected, FLAGS, FLAGS_Expected} = testvectors[vectornum];
		end
	// check results on falling edge of clock
	always @(negedge clk)
		if (~reset) begin
		if (Z !== Z_Expected) begin // checking result
			$display("Error: inputs = %h", {ALU_CTL, A, B});
			$display(" outputs = %h (%h expected)", Z, Z_Expected);
			// replace with correct value?
			Z = Z_Expected;
			errors = errors + 1;
		end
		if (FLAGS !== FLAGS_Expected) begin // checking result
			$display("Error: inputs = %h", {ALU_CTL, A, B});
			$display(" outputs = %h (%h expected)", FLAGS, FLAGS_Expected);
			// replace with correct value?
			FLAGS = FLAGS_Expected;
			errors = errors + 1;
		end
		vectornum = vectornum + 1; 
		// does 4 relate to the column size or row size? or the end of the array?
		// array[index] should equal 
		if (testvectors[vectornum] === 4'bx) begin // should 4 be changed to a different value?
		
			$display("%d testss completed with %d errors", vectornum, errors);
			$finish; 
		end
		end
endmodule
			
			
			
			

		