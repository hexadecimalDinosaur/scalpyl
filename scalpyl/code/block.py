from typing import Any
import inspect

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
    filename: str = None
    name: str = None
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

    instructions: tuple[Instruction, ...]
    children: tuple["CodeBlock", ...]

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
