from sys import version_info
from typing import IO

from scalpyl.loaders.base import Code, Loader


class SourceLoader(Loader):
    def load_file(file: IO[bytes], filename="<unknown>") -> Code:
        source = file.read().decode()
        co: CodeType = compile(source, filename)

        return Code(co, version_info, filename, None, False)
