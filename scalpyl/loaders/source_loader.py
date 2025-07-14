from sys import version_info
from typing import IO
from types import CodeType

from scalpyl.loaders.base import Code, Loader


class SourceLoader(Loader):
    @staticmethod
    def load_file(file: IO[bytes], filename="<unknown>") -> Code:
        source = file.read().decode()
        co: CodeType = compile(source, filename, "exec")

        return Code(co, version_info, filename, None, False)
