from abc import abstractmethod
from typing import IO, Optional
from types import CodeType
from platform import python_version_tuple


class Code:
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


class Loader:
    accepted_file_types: list[str]
    accepted_versions: Optional[list[str]] = None


    @staticmethod
    @abstractmethod
    def load_file(file: IO[bytes], filename="<unknown>") -> Code:
        ...
