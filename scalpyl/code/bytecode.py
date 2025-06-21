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

    def __init__(self):
        self.offset = 0
        self.opcode = 9
        self.opname = "NOP"
        self.raw = b'\x09\x00'
        self.arg = 0
        self.jump_from = tuple()
