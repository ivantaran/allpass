
module allpass_section #(
    parameter WIDTH = 16
)(
    input wire clk, 
    input wire rst, 
    input wire signed [WIDTH-1:0] c, 
    input wire signed [WIDTH-1:0] ain, 
    input wire signed [WIDTH-1:0] din, 
    output wire signed [WIDTH-1:0] aout,
    output wire signed [WIDTH-1:0] dout
);
    
    reg signed [WIDTH-1:0] a0 = 0;

    wire signed [WIDTH*2-1:0] ca_mul = c * a0;
    wire signed [WIDTH-1:0] ca = ca_mul[WIDTH*2-1:WIDTH];
    wire signed [WIDTH*2-1:0] cb_mul = c * ain;
    wire signed [WIDTH-1:0] cb = cb_mul[WIDTH*2-1:WIDTH];
    assign aout = din - ca;
    assign dout = a0 + cb;

    always @(posedge clk) begin
        if (rst) begin
            a0 <= 0;
        end else begin
            a0 <= ain;
        end
    end

    wire _unused = &{ca_mul[WIDTH-1:0], cb_mul[WIDTH-1:0]};

endmodule
