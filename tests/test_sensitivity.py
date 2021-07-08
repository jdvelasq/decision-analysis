"""
Risk profile

"""
from smart_choice.decisiontree import DecisionTree
from smart_choice.examples import stguide, stbook, oil_tree_example

from tests.capsys import check_capsys


def test_fig_7_17(capsys):
    """Fig. 7.17 --- Probabilistic Sensitivity"""

    nodes = stguide()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback()
    tree.probabilistic_sensitivity(varname="cost")
    check_capsys("./tests/files/stguide_fig_7_17.txt", capsys)


def test_stbook_fig_3_8_pag_55(capsys):
    """Probabilistic Sensitivity"""

    nodes = stbook()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback()
    sensitivity = tree.probabilistic_sensitivity(varname="cost")
    print(sensitivity.head(21))
    print(sensitivity.tail(63).head(21))
    print(sensitivity.tail(42).head(21))
    print(sensitivity.tail(21))
    check_capsys("./tests/files/stbook_fig_3_8_pag_55.txt", capsys)


def test_oilexample_pag_34a(capsys):
    """Sensitivity"""
    nodes = oil_tree_example()
    tree = DecisionTree(nodes=nodes)
    print(
        tree.value_sensitivity(
            name="oil_found", branch="large-well", values=(2500, 5000)
        )
    )
    check_capsys("./tests/files/oilexample_pag_34a.txt", capsys)


def test_oilexample_pag_34b(capsys):
    """Sensitivity"""
    nodes = oil_tree_example()
    tree = DecisionTree(nodes=nodes)
    print(
        tree.value_sensitivity(
            name="drill_decision", branch="drill", values=(-750, -450)
        )
    )
    check_capsys("./tests/files/oilexample_pag_34b.txt", capsys)
