
#include "Vallpass_section.h"
#include "verilated.h"
#include "verilated_vcd_c.h"

#include <math.h>

vluint64_t main_time = 0;
#define C0 32767

static int16_t ap_section(int16_t din, int16_t c, int rst) {
    static int16_t a;
    static int16_t a0;
    static int16_t b[4];
    if (rst) {
        a = 0;
        a0 = 0;
        b[0] = 0;
        b[1] = 0;
    } else {
        a0 = a;
        a = din - (int16_t)((a0 * c) >> 16);
        b[0] = (int16_t)((a * c) >> 16) + a0;
    }
    return (int16_t)b[0];
}

int main(int argc, char **argv, char **env) {
    Verilated::commandArgs(argc, argv);
    Verilated::traceEverOn(true);

    Vallpass_section *top = new Vallpass_section();
    VerilatedVcdC *vcd = new VerilatedVcdC();

    top->trace(vcd, 99);
    vcd->open("sim.vcd");

    top->clk = 1;
    top->rst = 1;
    top->din = 0;
    top->c = C0;

    for (int i = 0; i < 4; i++) {
        top->ain = top->aout;
        top->eval();
        vcd->dump(main_time);
        top->clk = top->clk ? 0 : 1;
        main_time++;
    }

    top->rst = 0;
    int i = 0;
    int16_t ap = 0;
    do {
        top->eval();
        vcd->dump(main_time);

        top->clk = top->clk ? 0 : 1;
        top->ain = top->aout;
        if (top->clk) {
            ap = ap_section(top->din, top->c, 0);
            printf("%8hd:%8hd:%8hd\n", (int16_t)top->dout, ap, (int16_t)top->dout - ap);
            // top->din = sinf(2.0 * M_PI * (float)(i)*0.05) * 0x7fff;
            top->din = (i == 1) ? 0x7fff : 0;
            i++;
        }

        main_time++;
    } while (main_time < 100 && !Verilated::gotFinish());

    top->final();

    vcd->close();
    delete top;
    delete vcd;

    printf("Latency: %lu\n", (main_time + 1) / 2);

    exit(0);
}