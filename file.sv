module counter (
    input wire clk,
    input wire res_n,
    output reg [7:0] cnt_out
);

    // Internal signal for counting
    reg [7:0] count;

    // Synchronous counter
    always @(posedge clk or negedge res_n) begin
        if (!res_n) begin
            // Reset condition
            count <= 8'b0;
        end else begin
            // Count up condition
            count <= count + 1;
        end
    end

    // Assign output
    assign cnt_out = count;

endmodule
