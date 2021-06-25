"""Test module
"""

from pydecisiontree.nodes import Nodes


def test_adds_terminal_node():

    name = "node1"
    expr = lambda x: x + 1

    nodes = Nodes()
    nodes.terminal(name=name, expr=expr)

    assert nodes[name].get("type") == "TERMINAL"
    assert nodes[name].get("expr") == expr


def test_adds_chance_node():
    #
    name = "chance_node"
    branches = [
        (20.0, 100, "next_node"),
        (30.0, 200, "next_node"),
        (50.0, 300, "next_node"),
    ]

    nodes = Nodes()
    nodes.chance(name=name, branches=branches)

    assert nodes[name].get("type") == "CHANCE"
    assert nodes[name].get("branches") == branches


def test_adds_decision_node():

    name = "decision_node"
    branches = [
        (20.0, "next_node"),
        (30.0, "next_node"),
        (50.0, "next_node"),
    ]
    max_ = True

    nodes = Nodes()
    nodes.decision(name=name, branches=branches, max_=max_)

    assert nodes[name].get("type") == "DECISION"
    assert nodes[name].get("branches") == branches
    assert nodes[name].get("max_") == max_
