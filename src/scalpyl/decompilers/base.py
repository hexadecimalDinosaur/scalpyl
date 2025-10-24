from abc import abstractmethod, ABCMeta
from typing import Literal, Optional

from scalpyl.code import DisassembledCode, DecompiledCode, CodeBlock


CodeFormats = Literal[
    "code-fragments",
    "dict-comprehension",
    "exec",
    "generator",
    "lambda",
    "list-comprehension",
    "set-comprehension",
]

class Decompiler(metaclass=ABCMeta):
    @abstractmethod
    def decompile_instructions(self, co: CodeBlock, dis: Optional[DisassembledCode]=None, code_format: CodeFormats="exec") -> DecompiledCode:
        pass
