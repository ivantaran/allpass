
module allpass_section #(
    parameter WIDTH = 16
)(
    input wire clk, 
    input wire rst, 
    input wire signed [WIDTH-1:0] din, 
    input wire signed [WIDTH-1:0] c, 
    output reg signed [WIDTH-1:0] dout = 0 
);
    
    reg signed [WIDTH-1:0] a0 = 0;
    reg signed [WIDTH-1:0] b0 = 0;

    wire signed [WIDTH*2-1:0] ca_mul = c * a0;
    wire signed [WIDTH-1:0] ca = ca_mul[WIDTH*2-1:WIDTH];
    wire signed [WIDTH-1:0] a = din - ca;
    wire signed [WIDTH*2-1:0] cb_mul = c * a;
    wire signed [WIDTH-1:0] cb = cb_mul[WIDTH*2-1:WIDTH];
    wire signed [WIDTH-1:0] b = a0 + cb;

    always @(posedge clk) begin
        if (rst) begin
            a0 <= 0;
            dout <= 0;
        end else begin
            a0 <= a;
            b0 <= b;
            dout <= b0;
        end
    end

    wire _unused = &{ca_mul[WIDTH-1:0], cb_mul[WIDTH-1:0]};

endmodule
