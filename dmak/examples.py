"""
Decision tree examples
===============================================================================

"""

from .nodes import Nodes


def stree_guide():
    """Supertree userguide bid example (2 branches)"""

    def payoff_fn(**values):
        return (values["bid"][0] - values["cost"][0]) * (
            1 if values["bid"][0] < values["compbid"][0] else 0
        )

    nodes = Nodes()
    nodes.decision(name="bid", branches=[(500, "compbid"), (700, "compbid")], max_=True)
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


# def bid():
#     """Bid example from "Decision Analysis for the professional."""

#     def profit(BID, COST, COMPBID):
#         return (BID - COST) * (1 if BID < COMPBID else 0)

#     def nobid(**kwargs):
#         return 0

#     nodes = Nodes()
#     nodes.decision(
#         name="BID",
#         branches=[
#             (200, "COMPBID"),
#             (500, "COMPBID"),
#             (700, "COMPBID"),
#             (0, "NOBID"),
#         ],
#         max_=True,
#     )
#     nodes.chance(
#         name="COMPBID",
#         branches=[
#             (35.0, 400, "COST"),
#             (50.0, 600, "COST"),
#             (15.0, 800, "COST"),
#         ],
#     )
#     nodes.chance(
#         name="COST",
#         branches=[
#             (25.0, 200, "PROFIT"),
#             (50.0, 400, "PROFIT"),
#             (25.0, 600, "PROFIT"),
#         ],
#     )
#     nodes.terminal(
#         name="PROFIT",
#         user_fn=profit,
#     )

#     nodes.terminal(
#         name="NOBID",
#         user_fn=nobid,
#     )

#     return nodes
