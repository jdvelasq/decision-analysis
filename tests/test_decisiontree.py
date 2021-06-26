"""
Tests for DecisionTree model
"""


from pydecisiontree.decisiontree import DecisionTree
from pydecisiontree.nodes import Nodes


def test_build_tree():
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
            (40.0, 3, "T"),
            (60.0, 4, "T"),
        ],
    )

    nodes.terminal(
        name="T",
        user_fn=None,
    )

    print(nodes)

    tree = DecisionTree(variables=nodes, initial_variable="D")
    tree.build_tree()

    for tree_node in tree.tree_nodes:
        print(tree_node)

    assert True == 0


#     tree.build_skeleton(initial_variable="D", variables=nodes)

#     for node in tree.tree_nodes:
#         print(node)

#     assert tree.tree_nodes == [
#         {"id": 0, "type": "DECISION", "name": "D", "next": [1, 5]},
#         {"id": 1, "type": "CHANCE", "name": "C", "next": [2, 3, 4]},
#         {"id": 2, "type": "TERMINAL", "name": "T", "next": None},
#         {"id": 3, "type": "TERMINAL", "name": "T", "next": None},
#         {"id": 4, "type": "TERMINAL", "name": "T", "next": None},
#         {"id": 5, "type": "CHANCE", "name": "C", "next": [6, 7, 8]},
#         {"id": 6, "type": "TERMINAL", "name": "T", "next": None},
#         {"id": 7, "type": "TERMINAL", "name": "T", "next": None},
#         {"id": 8, "type": "TERMINAL", "name": "T", "next": None},
#     ]


# def test_fill_node_properties():

#     nodes = Nodes()

#     nodes.decision(
#         name="D",
#         branches=[
#             (1, "C"),
#             (2, "C"),
#         ],
#     )

#     nodes.chance(
#         name="C",
#         branches=[
#             (20.0, 3, "T"),
#             (30.0, 4, "T"),
#             (50.0, 5, "T"),
#         ],
#     )

#     nodes.terminal(
#         name="T",
#         user_fn=None,
#     )

#     tree = DecisionTree()

#     tree.build_skeleton(initial_variable="D", variables=nodes)
#     tree.fill_node_properties(variables=nodes)

#     for node in tree.tree_nodes:
#         print(node)

#     assert tree.tree_nodes == [
#         {
#             "id": 0,
#             "type": "DECISION",
#             "name": "D",
#             "next": [1, 5],
#             "max_": False,
#         },
#         {
#             "id": 1,
#             "type": "CHANCE",
#             "name": "C",
#             "next": [2, 3, 4],
#             "arg": {"D": 1},
#         },
#         {
#             "id": 2,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 20.0,
#             "arg": {"C": 3},
#             "user_fn": None,
#         },
#         {
#             "id": 3,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 30.0,
#             "arg": {"C": 4},
#             "user_fn": None,
#         },
#         {
#             "id": 4,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 50.0,
#             "arg": {"C": 5},
#             "user_fn": None,
#         },
#         {
#             "id": 5,
#             "type": "CHANCE",
#             "name": "C",
#             "next": [6, 7, 8],
#             "arg": {"D": 2},
#         },
#         {
#             "id": 6,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 20.0,
#             "arg": {"C": 3},
#             "user_fn": None,
#         },
#         {
#             "id": 7,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 30.0,
#             "arg": {"C": 4},
#             "user_fn": None,
#         },
#         {
#             "id": 8,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 50.0,
#             "arg": {"C": 5},
#             "user_fn": None,
#         },
#     ]


# def test_prepare_user_fun_args():

#     nodes = Nodes()

#     nodes.decision(
#         name="D",
#         branches=[
#             (1, "C"),
#             (2, "C"),
#         ],
#     )

#     nodes.chance(
#         name="C",
#         branches=[
#             (20.0, 3, "T"),
#             (30.0, 4, "T"),
#             (50.0, 5, "T"),
#         ],
#     )

#     nodes.terminal(
#         name="T",
#         user_fn=None,
#     )

#     tree = DecisionTree()

#     tree.build_skeleton(initial_variable="D", variables=nodes)
#     tree.fill_node_properties(variables=nodes)
#     tree.prepare_user_fn_args()

#     for node in tree.tree_nodes:
#         print(node)

#     assert tree.tree_nodes == [
#         {
#             "id": 0,
#             "type": "DECISION",
#             "name": "D",
#             "next": [1, 5],
#             "max_": False,
#         },
#         {
#             "id": 1,
#             "type": "CHANCE",
#             "name": "C",
#             "next": [2, 3, 4],
#             "arg": {"D": 1},
#             "user_fn_args": {"D": 1},
#         },
#         {
#             "id": 2,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 20.0,
#             "arg": {"C": 3},
#             "user_fn": None,
#             "user_fn_args": {"D": 1, "C": 3},
#         },
#         {
#             "id": 3,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 30.0,
#             "arg": {"C": 4},
#             "user_fn": None,
#             "user_fn_args": {"D": 1, "C": 4},
#         },
#         {
#             "id": 4,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 50.0,
#             "arg": {"C": 5},
#             "user_fn": None,
#             "user_fn_args": {"D": 1, "C": 5},
#         },
#         {
#             "id": 5,
#             "type": "CHANCE",
#             "name": "C",
#             "next": [6, 7, 8],
#             "arg": {"D": 2},
#             "user_fn_args": {"D": 2},
#         },
#         {
#             "id": 6,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 20.0,
#             "arg": {"C": 3},
#             "user_fn": None,
#             "user_fn_args": {"D": 2, "C": 3},
#         },
#         {
#             "id": 7,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 30.0,
#             "arg": {"C": 4},
#             "user_fn": None,
#             "user_fn_args": {"D": 2, "C": 4},
#         },
#         {
#             "id": 8,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 50.0,
#             "arg": {"C": 5},
#             "user_fn": None,
#             "user_fn_args": {"D": 2, "C": 5},
#         },
#     ]


# def test_evaluate_user_fn():

#     nodes = Nodes()

#     nodes.decision(
#         name="D",
#         branches=[
#             (1, "C"),
#             (2, "C"),
#         ],
#     )

#     nodes.chance(
#         name="C",
#         branches=[
#             (20.0, 3, "T"),
#             (30.0, 4, "T"),
#             (50.0, 5, "T"),
#         ],
#     )

#     nodes.terminal(
#         name="T",
#         user_fn=None,
#     )

#     tree = DecisionTree()

#     tree.build_skeleton(initial_variable="D", variables=nodes)
#     tree.fill_node_properties(variables=nodes)
#     tree.prepare_user_fn_args()
#     tree.evaluate_user_fn()

#     for node in tree.tree_nodes:
#         print(node)

#     assert tree.tree_nodes == [
#         {
#             "id": 0,
#             "type": "DECISION",
#             "name": "D",
#             "next": [1, 5],
#             "max_": False,
#         },
#         {
#             "id": 1,
#             "type": "CHANCE",
#             "name": "C",
#             "next": [2, 3, 4],
#             "arg": {"D": 1},
#             "user_fn_args": {"D": 1},
#         },
#         {
#             "id": 2,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 20.0,
#             "arg": {"C": 3},
#             "user_fn": None,
#             "user_fn_args": {"D": 1, "C": 3},
#             "user_fn_value": 4,
#         },
#         {
#             "id": 3,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 30.0,
#             "arg": {"C": 4},
#             "user_fn": None,
#             "user_fn_args": {"D": 1, "C": 4},
#             "user_fn_value": 5,
#         },
#         {
#             "id": 4,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 50.0,
#             "arg": {"C": 5},
#             "user_fn": None,
#             "user_fn_args": {"D": 1, "C": 5},
#             "user_fn_value": 6,
#         },
#         {
#             "id": 5,
#             "type": "CHANCE",
#             "name": "C",
#             "next": [6, 7, 8],
#             "arg": {"D": 2},
#             "user_fn_args": {"D": 2},
#         },
#         {
#             "id": 6,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 20.0,
#             "arg": {"C": 3},
#             "user_fn": None,
#             "user_fn_args": {"D": 2, "C": 3},
#             "user_fn_value": 5,
#         },
#         {
#             "id": 7,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 30.0,
#             "arg": {"C": 4},
#             "user_fn": None,
#             "user_fn_args": {"D": 2, "C": 4},
#             "user_fn_value": 6,
#         },
#         {
#             "id": 8,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 50.0,
#             "arg": {"C": 5},
#             "user_fn": None,
#             "user_fn_args": {"D": 2, "C": 5},
#             "user_fn_value": 7,
#         },
#     ]


# def test_compute_expected_values():

#     nodes = Nodes()

#     nodes.decision(
#         name="D",
#         branches=[
#             (1, "C"),
#             (2, "C"),
#         ],
#     )

#     nodes.chance(
#         name="C",
#         branches=[
#             (20.0, 3, "T"),
#             (30.0, 4, "T"),
#             (50.0, 5, "T"),
#         ],
#     )

#     nodes.terminal(
#         name="T",
#         user_fn=None,
#     )

#     tree = DecisionTree()

#     tree.build_skeleton(initial_variable="D", variables=nodes)
#     tree.fill_node_properties(variables=nodes)
#     tree.prepare_user_fn_args()
#     tree.evaluate_user_fn()
#     tree.compute_expected_values()

#     for node in tree.tree_nodes:
#         print(node)

#     assert tree.tree_nodes == [
#         {
#             "id": 0,
#             "type": "DECISION",
#             "name": "D",
#             "next": [1, 5],
#             "max_": False,
#             "ExpVal": 5.3,
#         },
#         {
#             "id": 1,
#             "type": "CHANCE",
#             "name": "C",
#             "next": [2, 3, 4],
#             "arg": {"D": 1},
#             "user_fn_args": {"D": 1},
#             "ExpVal": 5.3,
#         },
#         {
#             "id": 2,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 20.0,
#             "arg": {"C": 3},
#             "user_fn": None,
#             "user_fn_args": {"D": 1, "C": 3},
#             "user_fn_value": 4,
#             "ExpVal": 4,
#         },
#         {
#             "id": 3,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 30.0,
#             "arg": {"C": 4},
#             "user_fn": None,
#             "user_fn_args": {"D": 1, "C": 4},
#             "user_fn_value": 5,
#             "ExpVal": 5,
#         },
#         {
#             "id": 4,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 50.0,
#             "arg": {"C": 5},
#             "user_fn": None,
#             "user_fn_args": {"D": 1, "C": 5},
#             "user_fn_value": 6,
#             "ExpVal": 6,
#         },
#         {
#             "id": 5,
#             "type": "CHANCE",
#             "name": "C",
#             "next": [6, 7, 8],
#             "arg": {"D": 2},
#             "user_fn_args": {"D": 2},
#             "ExpVal": 6.3,
#         },
#         {
#             "id": 6,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 20.0,
#             "arg": {"C": 3},
#             "user_fn": None,
#             "user_fn_args": {"D": 2, "C": 3},
#             "user_fn_value": 5,
#             "ExpVal": 5,
#         },
#         {
#             "id": 7,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 30.0,
#             "arg": {"C": 4},
#             "user_fn": None,
#             "user_fn_args": {"D": 2, "C": 4},
#             "user_fn_value": 6,
#             "ExpVal": 6,
#         },
#         {
#             "id": 8,
#             "type": "TERMINAL",
#             "name": "T",
#             "next": None,
#             "prob": 50.0,
#             "arg": {"C": 5},
#             "user_fn": None,
#             "user_fn_args": {"D": 2, "C": 5},
#             "user_fn_value": 7,
#             "ExpVal": 7,
#         },
#     ]
