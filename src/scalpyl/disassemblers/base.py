from abc import abstractmethod, ABCMeta
from types import CodeType

from scalpyl.code.block import DisassembledCode, CodeFlags
from scalpyl.code.bytecode import Instruction
from scalpyl.loaders.base import CodeBlock


class Disassembler(metaclass=ABCMeta):
    @abstractmethod
    def disassemble(self, code_obj: CodeType) -> tuple[Instruction, ...]:
        ...

    def load_block(self, code_obj: CodeType | CodeBlock, recursive: bool=True) -> DisassembledCode:
        block = DisassembledCode()
        if isinstance(code_obj, CodeBlock):
            block.version_tuple = code_obj.version_tuple
            block.timestamp = code_obj.timestamp
            block.is_pypy = code_obj.is_pypy

            code_obj = code_obj.code

        block.filename = code_obj.co_filename
        block.name = code_obj.co_name
        block.firstlineno = code_obj.co_firstlineno

        block.consts = code_obj.co_consts
        block.varnames = code_obj.co_varnames
        block.nlocals = code_obj.co_nlocals
        block.freevars = code_obj.co_freevars
        block.names = code_obj.co_names

        block.argcount = code_obj.co_argcount
        block.posonlyargcount = code_obj.co_posonlyargcount
        block.kwonlyargcount = code_obj.co_kwonlyargcount

        block.stacksize = code_obj.co_stacksize
        block.flags = CodeFlags(code_obj.co_flags)

        block.instructions = self.disassemble(code_obj)
        if recursive:
            block.children = tuple(self.load_block(c) for c in code_obj.co_consts if isinstance(c, CodeType))
        else:
            block.children = tuple()

        return block
