`timescale 1ns / 1ps

module counter_tb;

  // Declare variables for the inputs and outputs of the DUT (Device Under Test)

  reg clk;

  reg res_n;

  wire [7:0] cnt_out;


  // Instantiate the DUT

  counter uut (

    .clk(clk),

    .res_n(res_n),

    .cnt_out(cnt_out)
  );


  // Test vectors

  initial begin
    // Initialize inputs and apply test vectors
    clk = 0;
    res_n = 0;
    // Apply test vectors
    #10;
    res_n = 1;
    #10;
    forever #5 clk = ~clk;
  end

  // Monitor changes

  initial begin
    $monitor("At time %0t:
 clk = %b,
 res_n = %b,
 cnt_out = %b
", $time
, clk
, res_n
, cnt_out
);
  end
  initial begin
    #200 $finish;
  end

endmodule
