# Scalpyl
Scalpyl is a graphical and scriptable Python bytecode and executable reverse engineering environment intended to be the successor to the [pycDisGUI](https://github.com/hexadecimalDinosaur/pycDisGUI) disassembler GUI. This project is a work-in-progress.

Current Python bytecode and executables reverse engineering has many individual command-line tools with a lack of any tooling focusing on ease-of-use, graphical interfaces, and integrations with other tools. This project aims to integrate all the different tools in the Python reverse engineering ecosystem together.

## Design Goals
The following are the goals for the development of this project, as this project is a work-in-progress, they are still being worked on and may not be completed or implemented yet.
* Work with Python bytecode compiled for any Python version
* Provide wrappers with a standardized API for many different disassemblers and decompilers like [dis](https://docs.python.org/3/library/dis.html), [xdis](https://github.com/rocky/python-xdis/tree/master), [pycdc](https://github.com/zrax/pycdc), [decompyle3](https://github.com/rocky/python-decompile3), and [PyLingual](https://www.pylingual.io/)
* Integrations with unpacker and deobfuscation tools like [pyinstxtractor-ng](https://github.com/pyinstxtractor/pyinstxtractor-ng) to enable the analysis of executable binaries and obfuscated bytecode
* Provide an interface for patching Python on a bytecode level
* Easy to use graphical interface similar to those found in [dnSpy](https://github.com/dnSpy/dnSpy) and [Recaf](https://github.com/Col-E/Recaf)
