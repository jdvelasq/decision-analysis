"""
Creation of tree without evaluation

"""
from smart_choice.decisiontree import DecisionTree
from smart_choice.examples import stguide

from tests.capsys import check_capsys


def test_stguide_fig_5_1(capsys):
    """Example creation from Fig. 5.1"""

    nodes = stguide()
    tree = DecisionTree(nodes=nodes)
    tree.display()
    check_capsys("./tests/files/stguide_fig_5_1.txt", capsys)


def test_stguide_fit_5_4(capsys):
    """Example creatioin from Fig. 5.4"""

    nodes = stguide()
    tree = DecisionTree(nodes=nodes)
    print(tree)
    check_capsys("./tests/files/stguide_fig_5_4.txt", capsys)
