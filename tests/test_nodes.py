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
    user_fn = None

    nodes = Nodes()
    nodes.terminal(name=name, user_fn=user_fn)

    assert nodes[name].get("type") == "TERMINAL"
    assert nodes[name].get("user_fn") is None


#
#
# C h a n c e    n o d e s
#
#
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


#
#
# D e c i s i o n    n o d e s
#
#


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
