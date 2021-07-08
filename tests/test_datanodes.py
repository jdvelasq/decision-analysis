"""
DataNodes creation tests.

"""
from tests.capsys import check_capsys
from _pytest.pytester import LineMatcher

from smart_choice.decisiontree import DecisionTree
from smart_choice.examples import (
    stguide,
    stguide_dependent_probabilities,
    stguide_dependent_outcomes,
)


def test_stguide_fig_5_4a(capsys):
    """Table of variables"""

    nodes = stguide()
    print(nodes)
    check_capsys("./tests/files/stguide_fig_5_4a.txt", capsys)
