from xdis.bytecode import Bytecode
from xdis.op_imports import get_opcode_module
from types import CodeType
from sys import version_info

from scalpyl.code.bytecode import Instruction
from scalpyl.code.block import CodeBlock
from scalpyl.disassemblers.base import Disassembler
from scalpyl.loaders.base import Code


class XdisDisassembler(Disassembler):
    opc: tuple

    def __init__(self, opc=version_info):
        self.opc = opc
        self.op_module = get_opcode_module(opc)

    def disassemble(self, code_obj: CodeType) -> tuple[Instruction, ...]:
        bc = Bytecode(code_obj, self.opc)
        instructions = []
        line_num = 0
        jumps: dict[int, list[int]] = {}
        for i in bc.get_instructions(code_obj):
            obj = Instruction()
            obj.opcode = i.opcode
            obj.opname = i.opname
            obj.offset = i.offset
            if i.starts_line is not None:
                line_num = i.starts_line
                obj.starts_line = True
            obj.line_num = line_num
            obj.arg = i.arg
            obj.argval = i.argval

            instructions.append(obj)

            if self.opc[0] == 3 and self.opc[1] < 13:
                if i.opcode in self.op_module.hasjrel:
                    target = i.offset + 2 + i.arg * 2
                    obj.jump_target = target
                    if target not in jumps:
                        jumps[target] = []
                    jumps[target].append(i.offset)
                elif i.opcode in self.op_module.hasjabs:
                    obj.jump_target = i.arg
                    if i.arg not in jumps:
                        jumps[i.arg] = []
                    jumps[i.arg].append(i.offset)

        for i in range(len(instructions)):
            if instructions[i].offset in jumps:
                instructions[i].jump_from = tuple(jumps[instructions[i].offset])

        return tuple(instructions)

    def load_block(self, code_obj: CodeType | Code) -> CodeBlock:
        if isinstance(code_obj, Code):
            self.opc = code_obj.version_tuple
        return super().load_block(code_obj)
