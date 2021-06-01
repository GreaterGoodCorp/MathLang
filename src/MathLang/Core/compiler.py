import os
import hmac
import base64

import dill
from py import code

from MathLang.Core import generate_ast


class Compiler:
    @staticmethod
    def py_compile(source: str) -> bytes:
        """Compiles MathLang source code to MathLang bytecode.

        :param source: MathLang source code.
        :type source: str
        :return: MathLang bytecode.
        :rtype: bytes
        """
        ast = generate_ast(source)
        bytecode = Compiler.__compile(ast.codify())
        signature = Compiler.__sign(bytecode, True)
        return bytecode + signature

    @staticmethod
    def py_decompile(source: bytes, unsafe: bool = False) -> code:
        """Decompile MathLang bytecode to Python bytecode.

        :param source: MathLang bytecode.
        :type source: bytes
        :param unsafe: Whether to enable unsafe decompilation.
        :type unsafe: bytes
        :return: Python bytecode.
        :rtype: code
        """
        bytecode, signature = source[:-64], source[-64:]
        try:
            ctrl_signature = Compiler.__sign(bytecode, False)
            assert hmac.compare_digest(signature, ctrl_signature)
        except UnverifiedSignatureWarning:
            if not unsafe:
                raise UnsafeDecompilationError("No signing key found.")
        except AssertionError:
            if not unsafe:
                raise UnsafeDecompilationError("Signature verification failed.")
        try:
            return Compiler.__decompile(bytecode)
        except (EOFError, ValueError, TypeError):
            raise ValueError("MathLang bytecode cannot be decompiled due to data corruption.")

    @staticmethod
    def get_signing_key():
        return Compiler.__get_random_signature_key()

    @staticmethod
    def __compile(source):
        return dill.dumps(compile(source, "<MathLang>", "exec", optimize=2))

    @staticmethod
    def __decompile(bytecode):
        return dill.loads(bytecode)

    @staticmethod
    def __sign(source, is_compile):
        return hmac.new(Compiler.__get_signature_key(is_compile), source, "sha512").digest()

    @staticmethod
    def __get_signature_key(is_compile):
        s = os.getenv("GRAPHER_SIGNING_KEY")
        if s is not None:
            return base64.b64decode(s)
        if is_compile:
            return Compiler.__get_random_signature_key()
        else:
            raise UnverifiedSignatureWarning

    @staticmethod
    def __get_random_signature_key():
        return os.urandom(32)


class UnverifiedSignatureWarning(Warning):
    def __init__(self, *args):
        super(UnverifiedSignatureWarning, self).__init__(*args)


class UnsafeDecompilationError(BaseException):
    def __init__(self, *args):
        super(UnsafeDecompilationError, self).__init__(*args)


def execute(source) -> None:
    """Executes MathLang source code. This function is dangerous and used for debugging purposes only."""
    s = Compiler.py_compile(source)
    exec(Compiler.py_decompile(s, True))
