
#include "Vallpass.h"
#include "verilated.h"
#include "verilated_vcd_c.h"

vluint64_t main_time = 0;
#define C0 32000

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
    top->c = C0;

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

        // if (i == 1) {
        //     top->din = 0x7fff;
        // } else {
        //     top->din = 0;
        // }

        main_time++;
        if (main_time % 2 == 0) {
            top->din = sinf(2.0 * M_PI * (float)(i)*0.05) * 0x7fff;
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