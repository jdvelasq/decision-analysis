"""
Risk profile

"""
from smart_choice.decisiontree import DecisionTree
from smart_choice.examples import stguide

from tests.capsys import check_capsys


def test_fig_7_17(capsys):
    """Fig. 7.17 --- Probabilistic Sensitivity"""

    nodes = stguide()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback()
    tree.probabilistic_sensitivity(varname="cost")
    check_capsys("./tests/files/stguide_fig_7_17.txt", capsys)
