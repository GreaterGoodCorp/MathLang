from pathlib import Path

import pytest

from Grapher.Core import get_source_signature

test_data_path = Path(__file__).parent.absolute() / "test_data"


class TestLexer:
    @staticmethod
    @pytest.fixture()
    def src1():
        with open(test_data_path / "source1.gp") as fp:
            return fp.read()

    @staticmethod
    @pytest.fixture()
    def src1sgn():
        with open(test_data_path / "source1.signature") as fp:
            return fp.read()

    @staticmethod
    @pytest.fixture()
    def src2():
        with open(test_data_path / "source2.gp") as fp:
            return fp.read()

    @staticmethod
    @pytest.fixture()
    def src2sgn():
        with open(test_data_path / "source2.signature") as fp:
            return fp.read()

    @staticmethod
    def test_simple_source(src1, src1sgn):
        assert get_source_signature(src1) == src1sgn.strip("\n")

    @staticmethod
    def test_conditional_source(src2, src2sgn):
        assert get_source_signature(src2) == src2sgn.strip("\n")
