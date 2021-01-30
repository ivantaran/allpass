
#include "Vallpass.h"
#include "verilated.h"
#include "verilated_vcd_c.h"

vluint64_t main_time = 0;

#define SCALE 2.0

#define C0 int16_t(32767 / SCALE)
#define C1 int16_t(-20480 / SCALE)
#define C2 int16_t(29793 / SCALE)
#define C3 int16_t(-1025 / SCALE)
#define C4 int16_t(-2494 / SCALE)
#define C5 int16_t(0 / SCALE)
// #define C0 int16_t(15793 / SCALE)
// #define C1 int16_t(-7293 / SCALE)
// #define C2 int16_t(32767 / SCALE)
// #define C3 int16_t(-9097 / SCALE)
// #define C4 int16_t(17564 / SCALE)
// #define C5 int16_t(0 / SCALE)

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
    top->c[0] = (C1 << 16) | C0;
    top->c[1] = (C3 << 16) | C2;
    top->c[2] = (C5 << 16) | C4;

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

        if (i == 1) {
            top->din = 0x7fff;
        } else {
            top->din = 0;
        }

        main_time++;
        if (main_time % 2 == 0) {
            // top->din = sinf(2.0 * M_PI * (float)(i)*0.05) * 0x7fff;
            i++;
        }

    } while (main_time < 100 && !Verilated::gotFinish());

    top->final();

    vcd->close();
    delete top;
    delete vcd;

    printf("Latency: %lu\n", (main_time + 1) / 2);

    exit(0);
}