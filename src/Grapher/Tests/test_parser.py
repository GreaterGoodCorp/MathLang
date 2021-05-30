from pathlib import Path
from json import loads, dumps

from pytest import fixture

from Grapher.Core import generate_ast, serialise_ast, deserialise_ast

test_data_path = Path(__file__).parent.absolute() / "test_data"


class TestParser:
    @staticmethod
    @fixture()
    def quick_src():
        return "PRINT \"Hello World\";"

    @staticmethod
    @fixture()
    def demo():
        with open(test_data_path / "simple_demo.gp") as fp:
            return fp.read()

    @staticmethod
    @fixture()
    def demo_ast():
        with open(test_data_path / "simple_demo.ast") as fp:
            return dumps(loads(fp.read()))

    @staticmethod
    def test_serialisation_and_deserialisation(quick_src):
        original_ast = generate_ast(quick_src)
        ast_str = serialise_ast(original_ast)
        assert original_ast == deserialise_ast(ast_str)

    @staticmethod
    def test_demo_serialisation(demo, demo_ast):
        assert serialise_ast(generate_ast(demo)) == demo_ast

    @staticmethod
    def test_demo_deserialisation(demo, demo_ast):
        assert deserialise_ast(demo_ast) == generate_ast(demo)
