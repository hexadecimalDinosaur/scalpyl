from collections import OrderedDict
from typing import Sequence, Optional

from scalpyl.code.block import DisassembledCode
from scalpyl.code.bytecode import Instruction


class DecompiledCode:
    code: list[str]
    block: DisassembledCode
    line_mappings: dict[int, list[str]]
    header: str

    def __init__(self, code: str | Sequence[str], code_block: DisassembledCode):
        if isinstance(code, str):
            self.code = code.splitlines()
        else:
            self.code = list(code)
        self.block = code_block
        self.line_mappings = {}
        self.header = ""

    def _mapping_from_block(self):
        for instruction_id in self.block._order:
            instruction = self.block._instruction_store[instruction_id]

            if instruction.line_num not in self.line_mappings:
                self.line_mappings[instruction.line_num] = []

            if instruction.starts_line:
                self.line_mappings[instruction.line_num].insert(0, instruction_id)
            else:
                self.line_mappings[instruction.line_num].append(instruction_id)

    def __str__(self) -> str:
        return self.header + "\n".join(self.code)

    def __dict__(self) -> dict[str, tuple[Instruction, ...]]:
        d = OrderedDict()
        for line_num, instruction_ids in self.line_mappings.items():
            d[self.code[line_num-1]] = tuple(self.block._instruction_store[i] for i in instruction_ids)
        return d
