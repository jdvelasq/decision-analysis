"""
Creation of tree without evaluation

"""
from smart_choice.decisiontree import DecisionTree
from smart_choice.examples import (
    stguide,
    stguide_dependent_probabilities,
    stguide_dependent_outcomes,
    stbook_dependent_outcomes,
)

from tests.capsys import check_capsys


def test_stguide_fig_5_1(capsys):
    """Example creation from Fig. 5.1"""

    nodes = stguide()
    tree = DecisionTree(nodes=nodes)
    tree.display()
    check_capsys("./tests/files/stguide_fig_5_1.txt", capsys)


def test_stguide_fig_5_4(capsys):
    """Example creatioin from Fig. 5.4"""

    nodes = stguide()
    tree = DecisionTree(nodes=nodes)
    print(tree)
    check_capsys("./tests/files/stguide_fig_5_4.txt", capsys)


def test_stguide_fig_7_3b(capsys):
    """Change probabilities"""

    nodes = stguide_dependent_probabilities()
    tree = DecisionTree(nodes=nodes)
    print(tree)
    check_capsys("./tests/files/stguide_fig_7_3b.txt", capsys)


def test_stguide_fig_7_6b(capsys):
    """Dependent outcomes"""

    nodes = stguide_dependent_outcomes()
    tree = DecisionTree(nodes=nodes)
    print(tree)

    check_capsys("./tests/files/stguide_fig_7_6b.txt", capsys)


def test_stbook_fig_4_5_pag_81(capsys):
    """Dependent outcomes"""

    nodes = stbook_dependent_outcomes()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback()
    tree.display()
    check_capsys("./tests/files/stbook_fig_4_5_pag_81.txt", capsys)
