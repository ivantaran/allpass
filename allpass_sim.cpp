
#include "Vallpass.h"
#include "verilated.h"
#include "verilated_vcd_c.h"

vluint64_t main_time = 0;

#define SCALE 2.0
// static const int16_t coeff[] = {6914, -7541, 17069, -8251};
// static const int16_t coeff[] = {9111, -4719, 16997, -3783};
static const int16_t coeff[] = {
    5252, 1996, 18211, 4802, 21163, 2953,
};

int main(int argc, char **argv, char **env) {
    Verilated::commandArgs(argc, argv);
    Verilated::traceEverOn(true);

    Vallpass *top = new Vallpass();
    VerilatedVcdC *vcd = new VerilatedVcdC();

    top->trace(vcd, 99);
    vcd->open("sim.vcd");

    top->clk = 1;
    top->rst = 1;
    top->din = 0;
    top->c[0] = (int64_t)coeff[0] & 0xffff;
    top->c[0] |= ((int64_t)coeff[1] & 0xffff) << 16;
    top->c[1] = ((int64_t)coeff[2] & 0xffff);
    top->c[1] |= ((int64_t)coeff[3] & 0xffff) << 16;
    top->c[2] = ((int64_t)coeff[4] & 0xffff);
    top->c[2] |= ((int64_t)coeff[5] & 0xffff) << 16;

    for (int i = 0; i < 4; i++) {
        top->eval();
        vcd->dump(main_time);
        top->clk = top->clk ? 0 : 1;
        main_time++;
    }

    top->rst = 0;
    int i = 0;

    do {
        top->eval();
        vcd->dump(main_time);
        top->clk = top->clk ? 0 : 1;
        if (top->clk) {
            top->din = (i == 1) ? 16384 : 0;
            // top->din = 16383;
            // top->din = sinf(2.0 * M_PI * (float)(i)*0.05) * 16384.0;
            i++;
        }
        main_time++;
    } while (main_time < 200 && !Verilated::gotFinish());

    top->final();

    vcd->close();
    delete top;
    delete vcd;

    printf("Latency: %lu\n", (main_time + 1) / 2);

    exit(0);
}