"""
Decision tree examples
===============================================================================

"""

from .decisiontree import DecisionTree
from .nodes import Nodes


def stguide():
    """Supertree userguide bid example (2 branches)"""

    def payoff_fn(**kwargs):
        values = kwargs["values"]
        return (values["bid"] - values["cost"]) * (
            1 if values["bid"] < values["compbid"] else 0
        )

    nodes = Nodes()
    nodes.decision(
        name="bid", branches=[(500, "compbid"), (700, "compbid")], maximize=True
    )
    nodes.chance(
        name="compbid",
        branches=[(0.35, 400, "cost"), (0.50, 600, "cost"), (0.15, 800, "cost")],
    )
    nodes.chance(
        name="cost",
        branches=[(0.25, 200, "profit"), (0.50, 400, "profit"), (0.25, 600, "profit")],
    )
    nodes.terminal(name="profit", payoff_fn=payoff_fn)

    return nodes


def stbook():
    """Bid example from "Decision Analysis for the professional."""

    def payoff_fn(**kwargs):
        values = kwargs["values"]
        return (values["bid"] - values["cost"]) * (
            1 if values["bid"] < values["compbid"] else 0
        )

    def nobid_fn(**kwargs):
        return 0

    nodes = Nodes()
    nodes.decision(
        name="bid",
        branches=[
            (300, "compbid"),
            (500, "compbid"),
            (700, "compbid"),
            ("no-bid", 0, "nobid"),
        ],
        maximize=True,
    )
    nodes.chance(
        name="compbid",
        branches=[
            (35.0, 400, "cost"),
            (50.0, 600, "cost"),
            (15.0, 800, "cost"),
        ],
    )
    nodes.chance(
        name="cost",
        branches=[
            (25.0, 200, "profit"),
            (50.0, 400, "profit"),
            (25.0, 600, "profit"),
        ],
    )
    nodes.terminal(name="profit", payoff_fn=payoff_fn)
    nodes.terminal(name="nobid", payoff_fn=nobid_fn)

    return nodes


def oil_tree_example():
    """PrecisionTree Oil Example"""

    def payoff_fn(**kwargs):
        return sum([value for _, value in kwargs["values"].items()])

    nodes = Nodes()
    nodes.decision(
        name="test_decision",
        branches=[
            ("test", -55, "test_results"),
            ("dont-test", 0, "drill_decision"),
        ],
        maximize=True,
    )

    nodes.chance(
        name="test_results",
        branches=[
            ("ind_dry", 0.38, 0, "drill_decision"),
            ("ind_small", 0.39, 0, "drill_decision"),
            ("ind_large", 0.23, 0, "drill_decision"),
        ],
    )

    nodes.decision(
        name="drill_decision",
        branches=[
            ("drill", -600, "oil_found"),
            ("dont-drill", 0, "no_drill"),
        ],
        maximize=True,
    )

    nodes.chance(
        name="oil_found",
        branches=[
            ("dry", 0.38, 0, "profit"),
            ("small", 0.39, 1500, "profit"),
            ("large", 0.23, 3400, "profit"),
        ],
    )

    nodes.terminal(name="no_drill", payoff_fn=payoff_fn)
    nodes.terminal(name="profit", payoff_fn=payoff_fn)

    tree = DecisionTree(variables=nodes, initial_variable="test_decision")

    tree.set_probability(idx=4, probability=0.7895)
    tree.set_probability(idx=5, probability=0.1579)
    tree.set_probability(idx=6, probability=0.0526)

    tree.set_probability(idx=10, probability=0.3846)
    tree.set_probability(idx=11, probability=0.4615)
    tree.set_probability(idx=12, probability=0.1538)

    tree.set_probability(idx=16, probability=0.2174)
    tree.set_probability(idx=17, probability=0.2609)
    tree.set_probability(idx=18, probability=0.5217)

    tree.set_probability(idx=22, probability=0.5000)
    tree.set_probability(idx=23, probability=0.3000)
    tree.set_probability(idx=24, probability=0.2000)

    return tree


# def supertree_bid():
#     """SuperTree basic bid example."""
#

#     #
#     # Bid proposal
#     #
#     nodes.decision(
#         name="bid",
#         branches=[
#             (500, "compbid"),
#             (700, "compbid"),
#         ],
#         max_=True,
#     )

#     #
#     # Competitor proposal
#     #
#     nodes.chance(
#         name="compbid",
#         branches=[
#             (0.35, 400, "cost"),
#             (0.50, 600, "cost"),
#             (0.15, 800, "cost"),
#         ],
#     )

#     #
#     # Production costs
#     #
#     nodes.chance(
#         name="cost",
#         branches=[
#             (0.25, 200, "profit"),
#             (0.50, 400, "profit"),
#             (0.25, 600, "profit"),
#         ],
#     )

#     #
#     # Profit
#     #
#     def profit(bid, cost, compbid):
#         return (bid - cost) * (1 if bid < compbid else 0)

#     nodes.terminal(
#         name="profit",
#         user_fn=profit,
#     )

#     return nodes


# def supertree_bid_2134():
#     """SuperTree basic bid example nodes 2-1-3-4."""
#     nodes = Nodes()

#     #
#     # Competitor proposal
#     #
#     nodes.chance(
#         name="compbid",
#         branches=[(0.35, 400, "bid"), (0.50, 600, "bid"), (0.15, 800, "bid")],
#     )

#     #
#     # Bid proposal
#     #
#     nodes.decision(
#         name="bid",
#         branches=[(500, "cost"), (700, "cost")],
#         max_=True,
#     )

#     #
#     # Production costs
#     #
#     nodes.chance(
#         name="cost",
#         branches=[(0.25, 200, "profit"), (0.50, 400, "profit"), (0.25, 600, "profit")],
#     )

#     #
#     # Profit
#     #
#     def profit(bid, cost, compbid):
#         return (bid - cost) * (1 if bid < compbid else 0)

#     nodes.terminal(name="profit", user_fn=profit)

#     return nodes


# def supertree_bid_2314():
#     """SuperTree basic bid example nodes 2-3-1-4."""
#     nodes = Nodes()

#     #
#     # Competitor proposal
#     #
#     nodes.chance(
#         name="compbid",
#         branches=[(0.35, 400, "cost"), (0.50, 600, "cost"), (0.15, 800, "cost")],
#     )

#     #
#     # Production costs
#     #
#     nodes.chance(
#         name="cost",
#         branches=[(0.25, 200, "bid"), (0.50, 400, "bid"), (0.25, 600, "bid")],
#     )
#     #
#     # Bid proposal
#     #
#     nodes.decision(
#         name="bid",
#         branches=[(500, "profit"), (700, "profit")],
#         max_=True,
#     )

#     #
#     # Profit
#     #
#     def profit(bid, cost, compbid):
#         return (bid - cost) * (1 if bid < compbid else 0)

#     nodes.terminal(name="profit", user_fn=profit)

#     return nodes


# def supertree_prob_sensitivity():
#     """SuperTree basic bid example."""

#     def profit(bid, cost, compbid):
#         return (bid - cost) * (1 if bid < compbid else 0)

#     nodes = Nodes()
#     nodes.decision(
#         name="bid",
#         branches=[(500, "compbid"), (700, "compbid")],
#         max_=True,
#     )
#     nodes.chance(
#         name="compbid",
#         branches=[(0.35, 400, "cost"), (0.50, 600, "cost"), (0.15, 800, "cost")],
#     )
#     nodes.chance(
#         name="cost",
#         branches=[(0.00, 200, "profit"), (0.00, 400, "profit"), (1.0, 600, "profit")],
#     )
#     nodes.terminal(name="profit", user_fn=profit)
#     return nodes


# def supertree_prob_sensitivity_chp3():
#     """SuperTree basic bid example."""

#     def profit(bid, cost, compbid):
#         return (bid - cost) * (1 if bid < compbid else 0)

#     nodes = Nodes()
#     nodes.decision(
#         name="bid",
#         branches=[(300, "compbid"), (500, "compbid"), (700, "compbid")],
#         max_=True,
#     )
#     nodes.chance(
#         name="compbid",
#         branches=[(0.35, 400, "cost"), (0.50, 600, "cost"), (0.15, 800, "cost")],
#     )
#     nodes.chance(
#         name="cost",
#         branches=[(0.25, 200, "profit"), (0.50, 400, "profit"), (0.25, 600, "profit")],
#     )
#     nodes.terminal(name="profit", user_fn=profit)
#     return nodes
