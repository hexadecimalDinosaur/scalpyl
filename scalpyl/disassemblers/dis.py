import dis
from types import CodeType
from platform import python_version_tuple, python_implementation

from scalpyl.code import Instruction
from scalpyl.disassemblers.base import Disassembler


class DisDisassembler(Disassembler):
    def disassemble(self, code_obj: CodeType) -> tuple[Instruction, ...]:
        instructions: list[Instruction] = []
        line_num = 0
        jumps: dict[int, list[int]] = {}
        for i in dis.get_instructions(code_obj):
            obj = Instruction(offset=i.offset, opcode=i.opcode, opname=i.opname, arg=i.arg,
                              raw=code_obj.co_code[i.offset: i.offset+2])
            if i.starts_line is not None:
                line_num = i.starts_line
                obj.starts_line = True
            obj.line_num = line_num
            obj.arg_value = i.argval

            instructions.append(obj)

            if python_version_tuple()[0] == "3" and int(python_version_tuple()[1]) < 13:
                if i.opcode in dis.hasjrel:
                    target = i.offset + 2 + i.arg*2
                    obj.jump_target = target
                    if target not in jumps:
                        jumps[target] = []
                    jumps[target].append(i.offset)
                elif i.opcode in dis.hasjabs:
                    obj.jump_target = i.arg
                    if i.arg not in jumps:
                        jumps[i.arg] = []
                    jumps[i.arg].append(i.offset)

        for i in range(len(instructions)):
            if instructions[i].offset in jumps:
                instructions[i].jump_from = tuple(jumps[instructions[i].offset])

        return tuple(instructions)
