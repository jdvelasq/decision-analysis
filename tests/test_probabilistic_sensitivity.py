"""
Risk profile

"""
from smart_choice.decisiontree import DecisionTree
from smart_choice.probabilistic_sensitivity import ProbabilisticSensitivity
from smart_choice.examples import stguide, stbook

from tests.capsys import check_capsys


def test_stguide_fig_7_17(capsys):
    """Fig. 7.17 --- Probabilistic Sensitivity"""

    nodes = stguide()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback()
    sensitivity = ProbabilisticSensitivity(decisiontree=tree, varname="cost")
    # tree.probabilistic_sensitivity(varname="cost")
    print(sensitivity)
    check_capsys("./tests/files/stguide_fig_7_17.txt", capsys)


def test_stbook_fig_3_8_pag_55(capsys):
    """Probabilistic Sensitivity"""

    nodes = stbook()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback()
    sensitivity = ProbabilisticSensitivity(decisiontree=tree, varname="cost")
    print(sensitivity.df_.head(21))
    print(sensitivity.df_.tail(63).head(21))
    print(sensitivity.df_.tail(42).head(21))
    print(sensitivity.df_.tail(21))
    check_capsys("./tests/files/stbook_fig_3_8_pag_55.txt", capsys)
