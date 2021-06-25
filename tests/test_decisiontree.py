"""
Tests for DecisionTree model
"""

from pydecisiontree.decisiontree import DecisionTree
from pydecisiontree.nodes import Nodes


def test_build_skeleton():
    """Skeleton testing"""

    nodes = Nodes()

    nodes.decision(
        name="D",
        branches=[
            (1, "C"),
            (2, "C"),
        ],
    )

    nodes.chance(
        name="C",
        branches=[
            (20.0, 3, "T"),
            (30.0, 4, "T"),
            (50.0, 5, "T"),
        ],
    )

    nodes.terminal(
        name="T",
        expr=None,
    )

    tree = DecisionTree()

    tree.build_skeleton(initial_variable="D", variables=nodes)

    assert tree.tree_nodes == [
        {"id": 0, "variable_name": "D", "next_nodes": [1, 5]},
        {"id": 1, "variable_name": "C", "next_nodes": [2, 3, 4]},
        {"id": 2, "variable_name": "T", "next_nodes": None},
        {"id": 3, "variable_name": "T", "next_nodes": None},
        {"id": 4, "variable_name": "T", "next_nodes": None},
        {"id": 5, "variable_name": "C", "next_nodes": [6, 7, 8]},
        {"id": 6, "variable_name": "T", "next_nodes": None},
        {"id": 7, "variable_name": "T", "next_nodes": None},
        {"id": 8, "variable_name": "T", "next_nodes": None},
    ]
