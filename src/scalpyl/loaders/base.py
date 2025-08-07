from abc import abstractmethod, ABCMeta
from typing import IO, Optional
from types import CodeType
from platform import python_version_tuple

from scalpyl.code.block import CodeBlock


class Loader(metaclass=ABCMeta):
    accepted_file_types: list[str]
    accepted_versions: Optional[list[str]] = None


    @staticmethod
    @abstractmethod
    def load_file(file: IO[bytes], filename="<unknown>") -> CodeBlock:
        ...
