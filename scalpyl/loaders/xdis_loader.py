from typing import IO

from xdis.load import load_module_from_file_object

from scalpyl.loaders.base import Code, Loader


class XdisLoader(Loader):
    accepted_file_types = [".py", ".pyc"]
    accepted_versions = None

    @staticmethod
    def load_file(file: IO[bytes], filename="<unknown>") -> Code:
        tuple_version, timestamp, magic_int, co, is_pypy, source_size, sip_hash = \
            load_module_from_file_object(file, filename)
        return Code(co, tuple_version, filename, timestamp, is_pypy)
