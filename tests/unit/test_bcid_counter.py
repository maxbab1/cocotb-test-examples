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
        
# Basic test of the bcid_counter module
# 
# Tests monothonic counting after a reset and
# delayed startup in save mode


#  ======================   test functions   ======================

async def expect_normal_counting(dut, PRESCALER):
    for time in range(500 * (1+PRESCALER)):
        await ClockCycles(dut.Clk, PRESCALER)
        assert dut.BcidOut.value == time     & (1 << dut.BCID_WIDTH.value)-1   # truncate integer for comparison
        await ClockCycles(dut.Clk, 1)
        assert dut.BcidOut.value == (time+1) & (1 << dut.BCID_WIDTH.value)-1


async def slave_control_process(dut, PRESCALER):
    await ClockCycles(dut.Clk, 2)

    if PRESCALER == 0:
        await ClockCycles(dut.Clk, 1)

    for time in range(500):
        await ClockCycles(dut.Clk, PRESCALER)
        dut.BcidIn.value = time & (1<<dut.BCID_WIDTH.value)-1
        await ClockCycles(dut.Clk, 1)


#  ======================   test flow   ======================

@cocotb.test()
async def bcid_counter(dut):    
    LATENCY = int(os.environ.get('LATENCY', 0))
    PRESCALER = int(os.environ.get('PRESCALER', 1))
    
    cocotb.fork(Clock(dut.Clk, 50, units='ns').start())
    if LATENCY != 0:   # slave mode
        cocotb.fork(slave_control_process(dut, PRESCALER))

    dut.ResetLatency.value = 0
    dut.BcidIn.value = 0
    dut.CONF_LATENCY.value = LATENCY
    dut.CONF_PRESCALER.value = PRESCALER
    
    
    # Reset DUT
    dut.Reset.value = 1
    await ClockCycles(dut.Clk, 3)
    dut.Reset.value = 0

    await ClockCycles(dut.Clk, 1 + LATENCY*(1+PRESCALER))
    assert dut.BcidOut.value == 0

    await expect_normal_counting(dut, PRESCALER)


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
        module="test_bcid_counter")



if __name__ == "__main__":
    test()
