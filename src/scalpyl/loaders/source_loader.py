from sys import version_info
from typing import IO
from types import CodeType

from scalpyl.code.block import CodeBlock
from scalpyl.loaders.base import Loader


class SourceLoader(Loader):
    @staticmethod
    def load_file(file: IO[bytes], filename="<unknown>") -> CodeBlock:
        source = file.read().decode()
        co: CodeType = compile(source, filename, "exec")

        return CodeBlock(co, version_info, filename, None, False)
