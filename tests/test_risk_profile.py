"""
Risk profile

"""
from smart_choice.decisiontree import DecisionTree
from smart_choice.examples import oil_tree_example, stguide
from smart_choice.risk_profile import RiskProfile

from tests.capsys import check_capsys


def test_stguide_fig_5_8a(capsys):
    """Fig. 5.8 (a) --- Plot distribution"""

    nodes = stguide()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback()
    risk_profile = RiskProfile(decisiontree=tree, idx=0, cumulative=False, single=True)
    print(risk_profile)
    check_capsys("./tests/files/stguide_fig_5_8a.txt", capsys)


def test_stguide_fig_5_8b(capsys):
    """Fig. 5.8 (b) --- Plot distribution"""

    nodes = stguide()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback()
    risk_profile = RiskProfile(decisiontree=tree, idx=0, cumulative=True, single=True)
    print(risk_profile)
    check_capsys("./tests/files/stguide_fig_5_8b.txt", capsys)


def test_stguide_fig_5_8c(capsys):
    """Fig. 5.8 (c) --- Plot distribution"""

    nodes = stguide()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback()
    risk_profile = RiskProfile(decisiontree=tree, idx=0, cumulative=False, single=False)
    print(risk_profile)
    check_capsys("./tests/files/stguide_fig_5_8c.txt", capsys)


def test_stguide_fig_5_10(capsys):
    """Fig. 5.10 --- Cumulative plot distribution"""

    nodes = stguide()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback()
    risk_profile = RiskProfile(decisiontree=tree, idx=0, cumulative=True, single=False)
    print(risk_profile)
    check_capsys("./tests/files/stguide_fig_5_10.txt", capsys)


def test_stguide_fig_7_15(capsys):
    """Fig. 7.15 --- Plot distribution"""

    nodes = stguide()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback()
    risk_profile = RiskProfile(decisiontree=tree, idx=23, cumulative=True, single=True)
    print(risk_profile)
    check_capsys("./tests/files/stguide_fig_7_15.txt", capsys)


def test_oilexample_pag_32(capsys):
    """Typical risk profile"""
    nodes = oil_tree_example()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback()
    risk_profile = RiskProfile(decisiontree=tree, idx=0, cumulative=False, single=False)
    print(risk_profile)
    check_capsys("./tests/files/oilexample_pag_32.txt", capsys)


def test_oilexample_pag_33(capsys):
    """Typical risk profile"""
    nodes = oil_tree_example()
    tree = DecisionTree(nodes=nodes)
    tree.evaluate()
    tree.rollback()
    tree.display(policy_suggestion=True)
    check_capsys("./tests/files/oilexample_pag_33.txt", capsys)
