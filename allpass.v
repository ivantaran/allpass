
module allpass #(
    parameter WIDTH = 16, 
    parameter FIXEDPOINT = 14,
    parameter N = 7
)(
    input wire clk, 
    input wire rst, 
    input wire signed [WIDTH-1:0] din, 
    input wire signed [WIDTH*(N-1)-1:0] c, 
    output wire signed [WIDTH-1:0] dout
);

    integer i;

    wire signed [WIDTH-1:0] cc[0:N-2];
    reg signed [WIDTH-1:0] az[0:N-2];
    reg signed [WIDTH-1:0] bz[0:N-2];
    reg signed [WIDTH*2-1:0] sum;
    reg signed [WIDTH*2-1:0] ma[0:N-2];
    reg signed [WIDTH*2-1:0] mb[0:N-2];
    wire signed [WIDTH*2-1:0] sum0 = sum / 2**(FIXEDPOINT-1);
    wire _unused = &{sum0[WIDTH*2-1:WIDTH]};

    always @(*) begin
        sum = din * cc[0];
        for (i = 0; i < N - 2; i = i + 1) begin
            ma[i] = az[i] * cc[N-2-i];
            mb[i] = bz[i] * cc[i+1];
            sum = sum + mb[i] - ma[i];
        end
        ma[N-2] = az[N-2] * cc[0];
        mb[N-2] = bz[N-2] * 2**(FIXEDPOINT-1);
        sum = sum + mb[N-2] - ma[N-2];
    end

    always @(posedge clk) begin
        if (rst) begin
            bz[0] <= 0;
            az[0] <= 0;
        end else begin
            bz[0] <= din;
            az[0] <= sum0[WIDTH-1:0];
        end
    end

    genvar g;
    generate
        for (g = 0; g < N - 1; g = g + 1) begin
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
