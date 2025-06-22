from marshal import loads
from sys import version_info, version
from struct import unpack
from typing import IO
from platform import python_implementation, python_version

from scalpyl.loaders.base import Code, Loader


class MarshalLoader(Loader):
    def load_file(file: IO[bytes], filename="<unknown>") -> Code:
        magic_bytes = file.read(4)
        magic_int = unpack("<Hcc", magic_bytes)[0]
        ts = file.read(4)
        if version_info.major == 3 and version_info.minor >= 7:
            sip_hash = file.read(8)
            timestamp = None
        else:
            source_size = int.from_bytes(file.read(4), byteorder='little')
            timestamp = int.from_bytes(ts, byteorder='little')
        try:
            co = loads(file.read())
        except (ValueError, EOFError):
            raise ValueError("failed to load with marshal, given .pyc file was not built with {} {}".format(
                python_implementation(), python_version()
            ))

        return Code(co, version_info, filename, timestamp, False)
