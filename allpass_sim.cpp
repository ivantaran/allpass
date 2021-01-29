
#include "Vallpass.h"
#include "verilated.h"
#include "verilated_vcd_c.h"

vluint64_t main_time = 0;

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

    for (int i = 0; i < 4; i++) {
        top->eval();
        vcd->dump(main_time);
        top->clk = top->clk ? 0 : 1;
        main_time++;
    }

    top->rst = 0;

    do {
        top->eval();
        vcd->dump(main_time);
        top->clk = top->clk ? 0 : 1;
        main_time++;
    } while (main_time < 100 && !Verilated::gotFinish());

    top->final();

    vcd->close();
    delete top;
    delete vcd;

    printf("Latency: %lu\n", (main_time + 1) / 2);

    exit(0);
}