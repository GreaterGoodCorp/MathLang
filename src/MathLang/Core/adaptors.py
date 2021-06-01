from os import PathLike
from typing import Any

from MathLang.Core import Compiler


def compile_file_to_file(in_file: PathLike, out_file: PathLike) -> None:
    with open(in_file) as fp1:
        with open(out_file, "wb") as fp2:
            fp2.write(Compiler.py_compile(fp1.read()))
    return None


def compile_source_to_file(source: str, out_file: PathLike) -> None:
    with open(out_file, "wb") as fp:
        fp.write(Compiler.py_compile(source))
    return None


def compile_file_to_bytecode(in_file: PathLike) -> bytes:
    with open(in_file) as fp:
        return Compiler.py_compile(fp.read())


def compile_source_to_bytecode(source: str) -> bytes:
    return Compiler.py_compile(source)


def decompile_file_to_file(in_file: PathLike, out_file: PathLike, unsafe: bool = False) -> None:
    with open(in_file, "rb") as fp1:
        with open(out_file, "wb") as fp2:
            fp2.write(Compiler.py_decompile(fp1.read(), unsafe))
    return None


def decompile_bytecode_to_file(bytecode: bytes, out_file: PathLike, unsafe: bool = False) -> None:
    with open(out_file, "wb") as fp:
        fp.write(Compiler.py_decompile(bytecode, unsafe))
    return None


def decompile_file_to_code(in_file: PathLike, unsafe: bool = False) -> Any:
    with open(in_file, "rb") as fp:
        return Compiler.py_decompile(fp.read(), unsafe)


def decompile_bytecode_to_code(bytecode: bytes, unsafe: bool = False) -> Any:
    return Compiler.py_decompile(bytecode, unsafe)
