from pathlib import Path
from json import dumps, loads

from pytest import fixture

from MathLang.Core import deserialise_ast, generate_ast, generate_python_code

test_data_path = Path(__file__).parent.absolute() / "test_data"


class TestCodegen:
    @staticmethod
    @fixture()
    def quick_src():
        return "f=2*x+1;roots=SOLVE f IN REAL;"

    @staticmethod
    @fixture()
    def demo_ast():
        with open(test_data_path / "simple_demo.ast") as fp:
            return dumps(loads(fp.read()))

    @staticmethod
    @fixture()
    def redirect_stdout():
        return "import sys;import io;sys.stdout=io.StringIO();"

    @staticmethod
    def test_codegen(redirect_stdout, quick_src):
        code = redirect_stdout + generate_python_code(generate_ast(quick_src))
        assert exec(code) is None

    @staticmethod
    def test_demo_codegen(redirect_stdout, demo_ast):
        code = redirect_stdout + generate_python_code(deserialise_ast(demo_ast))
        assert exec(code) is None
