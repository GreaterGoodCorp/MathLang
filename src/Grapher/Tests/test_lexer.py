from pathlib import Path

from pytest import fixture

from Grapher.Core import get_source_signature

test_data_path = Path(__file__).parent.absolute() / "test_data"


class TestLexer:
    @staticmethod
    @fixture()
    def demo():
        with open(test_data_path / "simple_demo.gp") as fp:
            return fp.read()

    @staticmethod
    @fixture()
    def demo_sgn():
        with open(test_data_path / "simple_demo.signature") as fp:
            return fp.read()

    @staticmethod
    @fixture()
    def conditional():
        with open(test_data_path / "simple_conditional.gp") as fp:
            return fp.read()

    @staticmethod
    @fixture()
    def conditional_sgn():
        with open(test_data_path / "simple_conditional.signature") as fp:
            return fp.read()

    @staticmethod
    def test_demo_parsing(demo, demo_sgn):
        assert get_source_signature(demo) == demo_sgn.strip("\n")

    @staticmethod
    def test_conditional_parsing(conditional, conditional_sgn):
        assert get_source_signature(conditional) == conditional_sgn.strip("\n")
