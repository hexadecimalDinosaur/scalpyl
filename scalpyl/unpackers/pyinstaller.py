from tempfile import TemporaryDirectory
from os import chdir
from os.path import curdir, join as path_join, basename
from shutil import copyfile
from pathlib import Path

from pyinstxtractor_ng import PyInstArchive


def extract_pyinstaller(filepath: str) -> TemporaryDirectory:
    filepath = Path(filepath)
    filepath = filepath.resolve()
    filepath = str(filepath)
    pwd = curdir
    temp = TemporaryDirectory()
    chdir(temp.name)
    dst = path_join(temp.name, basename(filepath))
    copyfile(filepath, dst)

    arch = PyInstArchive(dst)
    arch.open()
    if not arch.checkFile():
        chdir(pwd)
        temp.cleanup()
        raise ValueError("Failed to parse file as pyinstaller binary")
    if not arch.getCArchiveInfo():
        chdir(pwd)
        temp.cleanup()
        raise ValueError("The file is not a pyinstaller archive")
    arch.parseTOC()
    arch.extractFiles(temp.name)
    arch.close()

    chdir(pwd)
    return temp
