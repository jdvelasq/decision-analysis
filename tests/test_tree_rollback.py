"""
Tree evaluation and rollback

"""
from smart_choice.decisiontree import DecisionTree
from smart_choice.examples import stguide

from tests.capsys import check_capsys


def test_stguide_fig_5_6a(capsys):
    """Fig. 5.6 (a) --- Evaluation of terminal nodes"""

    nodes = stguide()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.display()
    check_capsys("./tests/files/stguide_fig_5_6a.txt", capsys)


def test_stguide_fig_5_6b(capsys):
    """Fig. 5.6 (b) --- Expected Values"""

    nodes = stguide()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback()
    tree.display()
    check_capsys("./tests/files/stguide_fig_5_6b.txt", capsys)
