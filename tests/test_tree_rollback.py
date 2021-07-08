"""
Tree evaluation and rollback

"""
from smart_choice.decisiontree import DecisionTree
from smart_choice.examples import stguide, stbook, oil_tree_example

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


def test_stbook_fig_3_7_pag_54(capsys):
    """Example creation from Fig. 5.1"""

    nodes = stbook()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback()
    tree.display()
    check_capsys("./tests/files/stbook_fig_3_7_pag_54.txt", capsys)


def test_stbook_fig_5_13_pag_114(capsys):
    """Expected utility"""

    nodes = stbook()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback(utility_fn="exp", risk_tolerance=1000)
    tree.display(view="ce")
    check_capsys("./tests/files/stbook_fig_5_13_pag_114.txt", capsys)


def test_stbook_fig_5_11_pag_112(capsys):
    """Dependent outcomes"""

    nodes = stbook()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback(utility_fn="exp", risk_tolerance=1000)
    tree.display(view="eu")
    check_capsys("./tests/files/stbook_fig_5_11_pag_112.txt", capsys)


def test_oilexample_pag_43(capsys):
    """Basic oil tree example"""

    nodes = oil_tree_example()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback()
    tree.display()
    check_capsys("./tests/files/oilexample_pag_43.txt", capsys)


def test_oilexample_pag_56(capsys):
    """Basic oil tree example"""

    nodes = oil_tree_example()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback()
    tree.display(max_deep=3)
    check_capsys("./tests/files/oilexample_pag_56.txt", capsys)
