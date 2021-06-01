from pathlib import Path

from pytest import fixture

from MathLang.Core import execute

test_data_path = Path(__file__).parent.absolute() / "test_data"


class TestCompiler:
    @staticmethod
    @fixture()
    def quick_src():
        return "f=2*x+1;roots=SOLVE f IN REAL;"

    @staticmethod
    @fixture()
    def demo_src():
        with open(test_data_path / "simple_demo.gp") as fp:
            return fp.read()

    @staticmethod
    @fixture()
    def redirect_stdout():
        return "import sys;import io;sys.stdout=io.StringIO();\n"

    @staticmethod
    def test_compiler(redirect_stdout, quick_src):
        assert execute(quick_src) is None

    @staticmethod
    def test_demo_compiler(redirect_stdout, demo_src):
        assert execute(demo_src) is None
