from typing import Any, Optional, Sequence
from types import CodeType
import inspect
from platform import python_version_tuple

from scalpyl.code.bytecode import Instruction

class CodeFlags:
    """Class representing the bitmap of the `co_flags` attributes in CodeType objects

    Attributes:
        optimized:          The code object is optimized, using fast locals
        newlocals:          If set, a new dict will be created for the frame's `f_locals` when the code object is executed
        varargs:            The code object has a variable positional parameter (`*args`-like)
        varkeywords:        The code object has a variable keyword parameter (`**kwargs`-like)
        nested:             The code object is a nested function
        generator:          The code object is a generator function, i.e. a generator object is returned when the code object is executed
        coroutine:          The code object is a coroutine function. When the code object is executed it returns a coroutine object. See PEP 492 for more details
        iterable_coroutine: The flag is used to transform generators into generator-based coroutines. Generator objects with this flag can be used in `await` expression, and can `yield from` coroutine objects. See PEP 492 for more details
        async_generator:    The code object is an asynchronous generator function. When the code object is executed it returns an asynchronous generator object. See PEP 525 for more details
    """

    optimized: bool
    newlocals: bool
    varargs: bool
    varkeywords: bool
    nested: bool
    generator: bool
    coroutine: bool
    iterable_coroutine: bool
    async_generator: bool

    def __init__(self, co_flags: int):
        self.optimized = bool(co_flags & inspect.CO_OPTIMIZED)
        self.newlocals = bool(co_flags & inspect.CO_NEWLOCALS)
        self.varargs = bool(co_flags & inspect.CO_VARARGS)
        self.varkeywords = bool(co_flags & inspect.CO_VARKEYWORDS)
        self.nested = bool(co_flags & inspect.CO_NESTED)
        self.generator = bool(co_flags & inspect.CO_GENERATOR)
        self.coroutine = bool(co_flags & inspect.CO_COROUTINE)
        self.iterable_coroutine = bool(co_flags & inspect.CO_ITERABLE_COROUTINE)
        self.async_generator = bool(co_flags & inspect.CO_ASYNC_GENERATOR)

    def __int__(self) -> int:
        f = 0
        f += inspect.CO_OPTIMIZED if self.optimized else 0
        f += inspect.CO_NEWLOCALS if self.newlocals else 0
        f += inspect.CO_VARARGS if self.varargs else 0
        f += inspect.CO_VARKEYWORDS if self.varkeywords else 0
        f += inspect.CO_NESTED if self.nested else 0
        f += inspect.CO_GENERATOR if self.generator else 0
        f += inspect.CO_COROUTINE if self.coroutine else 0
        f += inspect.CO_ITERABLE_COROUTINE if self.iterable_coroutine else 0
        f += inspect.CO_ASYNC_GENERATOR if self.async_generator else 0
        return f


class CodeBlock:
    code: CodeType
    version_tuple: tuple = python_version_tuple()
    filename: Optional[str] = None
    timestamp: Optional[int] = None
    is_pypy: bool = False

    def __init__(self, code: CodeType, version_tuple: tuple = python_version_tuple(),
                 filename: Optional[str] = None, timestamp: Optional[int] = None, is_pypy: bool = False):
        self.code = code
        self.version_tuple = version_tuple
        self.filename = filename
        self.timestamp = timestamp
        self.is_pypy = is_pypy


class DisassembledCode:
    filename: Optional[str] = None
    name: Optional[str] = None
    firstlineno: int

    consts: tuple[Any, ...]
    varnames: tuple[str, ...]
    nlocals: int = 0
    freevars: tuple[str, ...]
    names: tuple[str, ...]

    argcount: int
    posonlyargcount: int
    kwonlyargcount: int

    stacksize: int
    flags: CodeFlags

    _instruction_store: dict[str, Instruction]
    _order: list[str]

    children: tuple["DisassembledCode", ...]

    version_tuple: tuple = python_version_tuple()
    timestamp: Optional[int] = None
    is_pypy: bool = False

    def __init__(self):
        self.firstlineno = 1
        self.consts = tuple()
        self.varnames = tuple()
        self.nlocals = 0
        self.freevars = tuple()
        self.names = tuple()
        self.argcount = 0
        self.posonlyargcount = 0
        self.kwonlyargcount = 0
        self.stacksize = 0
        self.flags = CodeFlags(0)
        self.children = tuple()
        self._instruction_store = {}
        self._order = []

    @property
    def instructions(self) -> tuple[Instruction]:
        return tuple(self._instruction_store[instruction_id] for instruction_id in self._order)

    @instructions.setter
    def instructions(self, value: Sequence[Instruction]):
        self._order.clear()
        for i in value:
            self._instruction_store[i.id] = i
            self._order.append(i.id)

    def __bytes__(self) -> bytes:
        b = bytes()
        for instruction_id in self._order:
            b += self._instruction_store[instruction_id].raw
        return b

    @property
    def code(self):
        return bytes(self)
