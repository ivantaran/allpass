
module allpass #(
    parameter WIDTH = 16, 
    parameter N = 5
)(
    input wire clk, 
    input wire rst, 
    input wire signed [WIDTH-1:0] din, 
    input wire signed [WIDTH*N-1:0] c, 
    output wire signed [WIDTH-1:0] dout
);

    integer i;

    wire signed [WIDTH-1:0] cc[0:N-1];
    reg signed [WIDTH-1:0] az[0:N-2];
    reg signed [WIDTH-1:0] bz[0:N-2];
    reg signed [WIDTH*2-1:0] sum;

    always @(*) begin
        sum = din * cc[0];
        for (i = 0; i < N - 1; i = i + 1) begin
            sum = sum + bz[i] * cc[i+1] - az[i] * cc[N-1-i];
        end
    end

    always @(posedge clk) begin
        if (rst) begin
            bz[0] <= 0;
            az[0] <= 0;
        end else begin
            bz[0] <= din;
            az[0] <= sum[WIDTH*2-1:WIDTH];
        end
    end

    genvar g;
    generate
        for (g = 0; g < N; g = g + 1) begin
            assign cc[g] = c[WIDTH*(g+1)-1:WIDTH*g];
        end
        for (g = 0; g < N - 2; g = g + 1) begin
            always @(posedge clk) begin
                if (rst) begin
                    bz[g + 1] <= 0;
                    az[g + 1] <= 0;
                end else begin
                    bz[g + 1] <= bz[g];
                    az[g + 1] <= az[g];
                end
            end
        end
    endgenerate

    assign dout = az[0];

endmodule
