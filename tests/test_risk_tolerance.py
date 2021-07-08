from smart_choice.decisiontree import DecisionTree
from smart_choice.examples import stguide

from tests.capsys import check_capsys


def test_fig_7_19(capsys):
    """Fig. 7.19 --- Risk Tolerance"""

    nodes = stguide()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback()
    tree.risk_sensitivity(utility_fn="exp", risk_tolerance=75)
    check_capsys("./tests/files/stguide_fig_7_19.txt", capsys)
