from scalpyl.disassemblers.xdis import XdisDisassembler

from test_disassembler_dis import generic_basic_test

def test_xdis_basic():
    xdis = XdisDisassembler()
    generic_basic_test(xdis)
