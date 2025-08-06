from typing import IO

from xdis.load import load_module_from_file_object

from scalpyl.code.block import CodeBlock
from scalpyl.loaders.base import Loader


class XdisLoader(Loader):
    accepted_file_types = [".py", ".pyc"]
    accepted_versions = None

    @staticmethod
    def load_file(file: IO[bytes], filename="<unknown>") -> CodeBlock:
        tuple_version, timestamp, magic_int, co, is_pypy, source_size, sip_hash = \
            load_module_from_file_object(file, filename)
        return CodeBlock(co, tuple_version, filename, timestamp, is_pypy)
