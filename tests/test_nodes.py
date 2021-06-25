"""Test module
"""

from pyDecisionTree.nodes import Nodes


def test_add_terminal_node():
    """
    Check terminal node addition
    """

    name = "node1"
    expr = lambda x: x + 1

    nodes = Nodes()
    nodes.terminal(name=name, expr=expr)

    assert nodes[name].get("type") == "TERMINAL"
    assert nodes[name].get("expr") == expr


def test_add_chance_node():
    """
    Check chance node addition
    """

    name = "chance_node"
    branches = [
        (20.0, 100, 1),
        (30.0, 200, 1),
        (50.0, 300, 1),
    ]

    nodes = Nodes()
    nodes.chance(name=name, branches=branches)

    assert nodes[name].get("type") == "CHANCE"
    assert nodes[name].get("branches") == branches
