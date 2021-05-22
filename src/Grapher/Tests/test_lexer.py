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
    def test_simple_source(src1, src1sgn):
        signature = get_source_signature(src1)
        assert signature == src1sgn
