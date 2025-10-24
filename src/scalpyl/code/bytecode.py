from typing import Any
from uuid import uuid4


class Instruction:
    id: str
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
        self.id = uuid4().hex

        self.offset = offset
        self.opcode = opcode
        self.opname = opname
        self.raw = raw
        self.arg = arg
        self.jump_from = jump_from

    def __repr__(self) -> str:
        return f"Instruction(offset={self.offset}, opname={self.opname}, arg={self.arg})"