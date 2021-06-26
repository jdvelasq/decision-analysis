"""Tests
"""
from decisions_tree.decision_tree import DecisionTree


def test_terminal_node_creation():
    """test"""

    tree = DecisionTree()
    tree.terminal_node()

    assert tree.data[0].type == "TERMINAL"
    assert tree.data[0].expr is None
    assert tree.data[0].id == 0
