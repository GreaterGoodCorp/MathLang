from pathlib import Path

import pytest

from Grapher.Core import get_source_signature

test_data_path = Path(__file__).parent.absolute() / "test_data"


class TestLexer:
    @staticmethod
    @pytest.fixture()
    def demo():
        with open(test_data_path / "demo_source.gp") as fp:
            return fp.read()

    @staticmethod
    @pytest.fixture()
    def demo_sgn():
        with open(test_data_path / "demo_source.signature") as fp:
            return fp.read()

    @staticmethod
    @pytest.fixture()
    def conditional():
        with open(test_data_path / "conditional_source.gp") as fp:
            return fp.read()

    @staticmethod
    @pytest.fixture()
    def conditional_sgn():
        with open(test_data_path / "conditional_source.signature") as fp:
            return fp.read()

    @staticmethod
    def test_demo_source(demo, demo_sgn):
        assert get_source_signature(demo) == demo_sgn.strip("\n")

    @staticmethod
    def test_conditional_source(conditional, conditional_sgn):
        assert get_source_signature(conditional) == conditional_sgn.strip("\n")
