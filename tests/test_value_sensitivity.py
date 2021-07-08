"""
Risk profile

"""
from smart_choice.decisiontree import DecisionTree
from smart_choice.examples import oil_tree_example

from tests.capsys import check_capsys


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
        tree.value_sensitivity(name="drill_decision", branch="drill", values=(450, 750))
    )
    check_capsys("./tests/files/oilexample_pag_34b.txt", capsys)
