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

