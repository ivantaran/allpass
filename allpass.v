
module allpass #(
    parameter WIDTH = 16, 
    parameter N = 1
)(
    input wire clk, 
    input wire rst, 
    input wire signed [WIDTH-1:0] din, 
    input wire signed [WIDTH-1:0] c, 
    output wire signed [WIDTH-1:0] dout
);
    allpass_section s0 (
        .clk(clk), 
        .rst(rst), 
        .din(din), 
        .c(c), 
        .dout(dout)
    );

endmodule
