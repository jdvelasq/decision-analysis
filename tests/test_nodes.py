"""Test module
"""

from pydecisiontree.nodes import Nodes

#
#
# T e r m i n a l    n o d e s
#
#


def test_adds_terminal_node():
    """terminal node"""
    name = "node1"
    expr = lambda x: x + 1

    nodes = Nodes()
    nodes.terminal(name=name, expr=expr)

    assert nodes[name].get("type") == "TERMINAL"
    assert nodes[name].get("expr") == expr


def test_repr_terminal_node():
    """Checks repr function"""
    name = "node1"
    expr = lambda x: x + 1

    nodes = Nodes()
    nodes.terminal(name=name, expr=expr)

    assert (
        nodes.__repr__() == "Node 0\n"
        "    Type: TERMINAL\n"
        "    Name: node1\n"
        "    Expr: (User fn)\n"
    )


def test_adds_chance_node():
    """chance node"""
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


def test_repr_chance_node():
    """Checks repr"""
    name = "chance_node"
    branches = [
        (20.0, 100, "next_node"),
        (30.0, 200, "next_node"),
        (50.0, 300, "next_node"),
    ]

    nodes = Nodes()
    nodes.chance(name=name, branches=branches)

    assert (
        nodes.__repr__() == "Node 0\n"
        "    Type: CHANCE\n"
        "    Name: chance_node\n"
        "    Branches:\n"
        "          Chance         Value  Next Node\n"
        "           20.00       100.000  next_node\n"
        "           30.00       200.000  next_node\n"
        "           50.00       300.000  next_node\n"
    )


def test_adds_decision_node():
    """decison node"""
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


def test_repr_decision_node():
    """Checks repr"""
    name = "decision_node"
    branches = [
        (20.0, "next_node"),
        (30.0, "next_node"),
        (50.0, "next_node"),
    ]
    max_ = True

    nodes = Nodes()
    nodes.decision(name=name, branches=branches, max_=max_)

    print(nodes.__repr__())

    assert (
        nodes.__repr__() == "Node 0\n"
        "    Type: DECISION - Maximum Payoff\n"
        "    Name: decision_node\n"
        "    Branches:\n"
        "                         Value  Next Node\n"
        "                        20.000  next_node\n"
        "                        30.000  next_node\n"
        "                        50.000  next_node\n"
    )
