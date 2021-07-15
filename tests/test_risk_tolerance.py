"""
Risk sensitivity tests

"""

from smart_choice.decisiontree import DecisionTree
from smart_choice.examples import stguide
from smart_choice.risk_sensitivity import RiskAttitudeSensitivity

from tests.capsys import check_capsys


# def _test_fig_7_19(capsys):
#     """Fig. 7.19 --- Risk Tolerance"""

#     nodes = stguide()
#     tree = DecisionTree(nodes=nodes)
#     tree.evaluate()
#     tree.rollback()
#     tree.risk_sensitivity(utility_fn="exp", risk_tolerance=75)
#     check_capsys("./tests/files/stguide_fig_7_19.txt", capsys)


def test_fig_7_19(capsys):
    """Fig. 7.19 --- Risk Tolerance"""

    nodes = stguide()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback()
    risk_sensitivity = RiskAttitudeSensitivity(
        tree, utility_fn="exp", risk_tolerance=75
    )
    print(risk_sensitivity)
    check_capsys("./tests/files/stguide_fig_7_19.txt", capsys)
