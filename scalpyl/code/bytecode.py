from typing import Any


class Instruction:
    offset: int
    starts_line: bool = False
    line_num: int | None = None

    opcode: int
    opname: str
    raw: bytes

    arg: int
    arg_value: Any = None

    jump_target: int = None
    jump_from: tuple[int, ...]

    def __init__(self, offset=0, opcode=9, opname="NOP", raw=b'\x09\x00', arg=0, jump_from: tuple[int, ...]=()):
        self.offset = offset
        self.opcode = opcode
        self.opname = opname
        self.raw = raw
        self.arg = arg
        self.jump_from = jump_from
