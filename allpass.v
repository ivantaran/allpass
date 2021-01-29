
module allpass #(
    parameter WIDTH = 16, 
    parameter N = 5
)(
    input wire clk, 
    input wire rst, 
    input wire signed [WIDTH-1:0] din, 
    input wire signed [WIDTH-1:0] c, 
    output wire signed [WIDTH-1:0] dout
);

    wire signed [WIDTH-1:0] din_s[0:N-1];
    wire signed [WIDTH-1:0] dout_s[0:N-1];

    assign din_s[0] = din;
    assign dout = dout_s[N-1];

    genvar i;
    generate
        for (i = 0; i < N - 1; i = i + 1) begin
            assign din_s[i + 1] = dout_s[i];
        end
        for (i = 0; i < N; i = i + 1) begin: section
            allpass_section u (
                .clk(clk), 
                .rst(rst), 
                .din(din_s[i]), 
                .c(c), 
                .dout(dout_s[i])
            );
        end
    endgenerate

endmodule
