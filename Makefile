
MODULE_NAME0=allpass
MODULE_NAME1=allpass_section

build:
	verilator --trace -Wall --cc ${MODULE_NAME0}.v --exe ${MODULE_NAME0}_sim.cpp -CFLAGS -g3 -O0 && make -j4 -C obj_dir -f V${MODULE_NAME0}.mk V${MODULE_NAME0}
	# verilator --trace -Wall --cc ${MODULE_NAME1}.v --exe ${MODULE_NAME1}_sim.cpp -CFLAGS -g3 -O0 && make -j4 -C obj_dir -f V${MODULE_NAME1}.mk V${MODULE_NAME1}
clean:
	rm -rf obj_dir