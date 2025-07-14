from types import CodeType
from sys import version_info

from scalpyl.disassemblers.dis import DisDisassembler
from scalpyl.disassemblers.base import Disassembler


FILENAME = "test.py"
NAME = "test"


def generic_basic_test(dis: Disassembler):
    nop = b"\x09\x00"
    load_const = b"d\x00"
    return_value = b"S\x00"
    consts = (None,)

    if version_info.minor >= 11:
        co = CodeType(0, 0, 0, 0, 1, 0,
                      nop + load_const + return_value, consts, (), (),
                      FILENAME, NAME, NAME, 1,
                      b'\xf0\x03\x01\x01\x01\xd8\x00\x04\x80\x04', b'', (), ())
    elif version_info.minor >= 10:
        co = CodeType(0, 0, 0, 0, 1, 0,
                      nop + load_const + return_value + consts, consts, (), ()
                      FILENAME, NAME, 1,
                      b'\xf0\x03\x01\x01\x01\xd8\x00\x04\x80\x04', (), ())
    block = dis.load_block(co)

    assert block.filename == FILENAME
    assert block.name == NAME
    assert block.consts == consts
    assert block.argcount == 0
    assert block.posonlyargcount == 0
    assert block.kwonlyargcount == 0
    assert block.nlocals == 0
    assert block.stacksize == 1

    assert block.instructions[0].opname == "NOP"
    assert block.instructions[0].raw == nop
    assert block.instructions[0].line_num == 0
    assert block.instructions[0].starts_line == True
    assert block.instructions[1].opname == "LOAD_CONST"
    assert block.instructions[1].raw == load_const
    assert block.instructions[1].arg == 0
    assert block.instructions[1].arg_value == consts[0]
    assert block.instructions[2].opname == "RETURN_VALUE"
    assert block.instructions[2].raw == return_value


def test_dis_basic():
    dis = DisDisassembler()
    generic_basic_test(dis)
