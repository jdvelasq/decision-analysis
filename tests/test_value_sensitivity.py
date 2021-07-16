"""
Risk profile

"""
from smart_choice.decisiontree import DecisionTree
from smart_choice.examples import oil_tree_example
from smart_choice.value_sensitivity import ValueSensitivity

from tests.capsys import check_capsys


def test_oilexample_pag_34a(capsys):
    """Sensitivity"""
    nodes = oil_tree_example()
    tree = DecisionTree(nodes=nodes)
    sensitivity = ValueSensitivity(
        decisiontree=tree,
        varname="oil_found",
        branch_name="large-well",
        values=(2500, 5000),
    )
    print(sensitivity)
    check_capsys("./tests/files/oilexample_pag_34a.txt", capsys)


def test_oilexample_pag_34b(capsys):
    """Sensitivity"""
    nodes = oil_tree_example()
    tree = DecisionTree(nodes=nodes)
    sensitivity = ValueSensitivity(
        decisiontree=tree,
        varname="drill_decision",
        branch_name="drill",
        values=(450, 750),
    )
    print(sensitivity)
    check_capsys("./tests/files/oilexample_pag_34b.txt", capsys)
