from cocotb_test.simulator import run
import cocotb
from cocotb.binary import BinaryValue
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles
from cocotb.handle import SimHandleBase
import pytest
import os
import queue
from numpy import random


tests_dir = os.path.join(os.path.dirname(__file__), '../')
output_dir = os.path.join(tests_dir, '../out')
        
# This is the same test as in test_bcid_counter.py, but with the testbench seperated in utils/
# 
# That makes sense if the testbench becomes larger


#  ======================   simulator invocation   ======================

@pytest.mark.parametrize("prescaler", [0, 1, 3])
@pytest.mark.parametrize("latency", [0, 1, 2, 100, 255])
def test(prescaler, latency):
    params = {"BCID_WIDTH": 8}                            # parameters to the top level module 
    test_parameters = {"PRESCALER":   str(prescaler),     # environemnt variables to pass to the test
                       "LATENCY":     str(latency),}
    defs = ["DUMP_LEVEL1"]                                # definitions passed to the simulator

    
    run(verilog_sources=[os.path.join(tests_dir, "../hdl/bcid_counter.sv")],
        includes=[os.path.join(tests_dir, "../hdl")],
        python_search=[os.path.join(tests_dir, "../util")],
        parameters=params,
        extra_env=test_parameters,
        defines=defs,
        sim_build=os.path.join(output_dir, 'sim_build'),
        toplevel="bcid_counter", 
        module="bcid_counter_utils")



if __name__ == "__main__":
    test()
