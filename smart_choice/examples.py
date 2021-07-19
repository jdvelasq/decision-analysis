"""
Decision tree examples
===============================================================================

The functions in this module returns the data node structures for several 
examples in the literature.

"""

from .datanodes import DataNodes


def stguide():
    """Supertree userguide bid example (2 branches).

    This function returns the data nodes for a bid problem with two possible
    decisiions:

    * Bid $ 500.

    * Bid $ 700.

    This example is used in the documentation available in the web site of
    the software.


    """

    def payoff_fn(**kwargs):
        values = kwargs["values"]
        bid = values["bid"] if "bid" in values.keys() else 0
        competitor_bid = (
            values["competitor_bid"] if "competitor_bid" in values.keys() else 0
        )
        cost = values["cost"] if "cost" in values.keys() else 0
        return (bid - cost) * (1 if bid < competitor_bid else 0)

    nodes = DataNodes()
    nodes.add_decision(
        name="bid",
        branches=[
            ("low", 500, "competitor_bid"),
            ("high", 700, "competitor_bid"),
        ],
        maximize=True,
    )
    nodes.add_chance(
        name="competitor_bid",
        branches=[
            ("low", 0.35, 400, "cost"),
            ("medium", 0.50, 600, "cost"),
            ("high", 0.15, 800, "cost"),
        ],
    )
    nodes.add_chance(
        name="cost",
        branches=[
            ("low", 0.25, 200, "profit"),
            ("medium", 0.50, 400, "profit"),
            ("high", 0.25, 600, "profit"),
        ],
    )
    nodes.add_terminal(name="profit", payoff_fn=payoff_fn)

    return nodes


def stguide_dependent_probabilities():
    """Supertree dependent probabilities example.

    This function returns the data node structure for the bid problem with
    dependent probabilities presented in Fig 7.3 of the documentation
    available in the web site.


    """

    def payoff_fn(**kwargs):
        values = kwargs["values"]
        bid = values["bid"] if "bid" in values.keys() else 0
        competitor_bid = (
            values["competitor_bid"] if "competitor_bid" in values.keys() else 0
        )
        cost = values["cost"] if "cost" in values.keys() else 0
        return (bid - cost) * (1 if bid < competitor_bid else 0)

    nodes = DataNodes()
    nodes.add_decision(
        name="bid",
        branches=[
            ("low", 500, "competitor_bid"),
            ("high", 700, "competitor_bid"),
        ],
        maximize=True,
    )
    nodes.add_chance(
        name="competitor_bid",
        branches=[
            ("low", 0.35, 400, "cost"),
            ("medium", 0.50, 600, "cost"),
            ("high", 0.15, 800, "cost"),
        ],
    )
    nodes.add_chance(
        name="cost",
        branches=[
            ("low", 0.25, 200, "profit"),
            ("medium", 0.50, 400, "profit"),
            ("high", 0.25, 600, "profit"),
        ],
    )
    nodes.add_terminal(name="profit", payoff_fn=payoff_fn)

    nodes.set_probability(0.4000, competitor_bid="low", cost="low")
    nodes.set_probability(0.4000, competitor_bid="low", cost="medium")
    nodes.set_probability(0.2000, competitor_bid="low", cost="high")

    nodes.set_probability(0.2500, competitor_bid="medium", cost="low")
    nodes.set_probability(0.5000, competitor_bid="medium", cost="medium")
    nodes.set_probability(0.2500, competitor_bid="medium", cost="high")

    nodes.set_probability(0.1000, competitor_bid="high", cost="low")
    nodes.set_probability(0.4500, competitor_bid="high", cost="medium")
    nodes.set_probability(0.4500, competitor_bid="high", cost="high")

    return nodes


def stguide_dependent_outcomes():
    """Supertree dependent outcomes example.

    This function returns the data nodes for the example in the Fig. 7.6
    of the documentation available in the web site.


    """

    def payoff_fn(**kwargs):
        values = kwargs["values"]
        bid = values["bid"] if "bid" in values.keys() else 0
        competitor_bid = (
            values["competitor_bid"] if "competitor_bid" in values.keys() else 0
        )
        cost = values["cost"] if "cost" in values.keys() else 0
        return (bid - cost) * (1 if bid < competitor_bid else 0)

    nodes = DataNodes()
    nodes.add_decision(
        name="bid",
        branches=[
            ("low", 500, "competitor_bid"),
            ("high", 700, "competitor_bid"),
        ],
        maximize=True,
    )
    nodes.add_chance(
        name="competitor_bid",
        branches=[
            ("low", 0.35, 400, "cost"),
            ("medium", 0.50, 600, "cost"),
            ("high", 0.15, 800, "cost"),
        ],
    )
    nodes.add_chance(
        name="cost",
        branches=[
            ("low", 0.25, 200, "profit"),
            ("medium", 0.50, 400, "profit"),
            ("high", 0.25, 600, "profit"),
        ],
    )
    nodes.add_terminal(name="profit", payoff_fn=payoff_fn)

    nodes.set_outcome(170, competitor_bid="low", bid="low", cost="low")
    nodes.set_outcome(350, competitor_bid="low", bid="low", cost="medium")
    nodes.set_outcome(350, competitor_bid="low", bid="low", cost="high")

    nodes.set_outcome(190, competitor_bid="low", bid="high", cost="low")
    nodes.set_outcome(380, competitor_bid="low", bid="high", cost="medium")
    nodes.set_outcome(570, competitor_bid="low", bid="high", cost="high")

    nodes.set_outcome(200, competitor_bid="medium", bid="low", cost="low")
    nodes.set_outcome(400, competitor_bid="medium", bid="low", cost="medium")
    nodes.set_outcome(600, competitor_bid="medium", bid="low", cost="high")

    nodes.set_outcome(220, competitor_bid="medium", bid="high", cost="low")
    nodes.set_outcome(420, competitor_bid="medium", bid="high", cost="medium")
    nodes.set_outcome(610, competitor_bid="medium", bid="high", cost="high")

    nodes.set_outcome(280, competitor_bid="high", bid="low", cost="low")
    nodes.set_outcome(450, competitor_bid="high", bid="low", cost="medium")
    nodes.set_outcome(650, competitor_bid="high", bid="low", cost="high")

    nodes.set_outcome(300, competitor_bid="high", bid="high", cost="low")
    nodes.set_outcome(480, competitor_bid="high", bid="high", cost="medium")
    nodes.set_outcome(680, competitor_bid="high", bid="high", cost="high")

    return nodes


def stbook():
    """Bid example from "Decision Analysis for the professional.


    Bidding tree with four possible options:

    * Bid $ 300.

    * Bid $ 500.

    * Bid $ 700.

    * No bid.

    """

    def payoff_fn(**kwargs):
        values = kwargs["values"]
        bid = values["bid"] if "bid" in values.keys() else 0
        competitor_bid = (
            values["competitor_bid"] if "competitor_bid" in values.keys() else 0
        )
        cost = values["cost"] if "cost" in values.keys() else 0
        return (bid - cost) * (1 if bid < competitor_bid else 0)

    nodes = DataNodes()
    nodes.add_decision(
        name="bid",
        branches=[
            ("low", 300, "competitor_bid"),
            ("medium", 500, "competitor_bid"),
            ("high", 700, "competitor_bid"),
            ("no-bid", 0, "profit"),
        ],
        maximize=True,
    )
    nodes.add_chance(
        name="competitor_bid",
        branches=[
            ("low", 0.35, 400, "cost"),
            ("medium", 0.50, 600, "cost"),
            ("high", 0.15, 800, "cost"),
        ],
    )
    nodes.add_chance(
        name="cost",
        branches=[
            ("low", 0.25, 200, "profit"),
            ("medium", 0.50, 400, "profit"),
            ("high", 0.25, 600, "profit"),
        ],
    )
    nodes.add_terminal(name="profit", payoff_fn=payoff_fn)

    return nodes


def stbook_dependent_outcomes():
    """Dependent outcomes example.


    This function returns the data nodes for the tree in the Fig. 4.5 (pag. 81)
    of the book "Decision Analysis for the Professional".

    """

    def payoff_fn(**kwargs):
        values = kwargs["values"]
        bid = values["bid"] if "bid" in values.keys() else 0
        competitor_bid = (
            values["competitor_bid"] if "competitor_bid" in values.keys() else 0
        )
        cost = values["cost"] if "cost" in values.keys() else 0
        return (bid - cost) * (1 if bid < competitor_bid else 0)

    nodes = DataNodes()
    nodes.add_decision(
        name="bid",
        branches=[
            ("low", 300, "cost"),
            ("medium", 500, "cost"),
            ("high", 700, "cost"),
            ("no-bid", 0, "profit"),
        ],
        maximize=True,
    )
    nodes.add_chance(
        name="cost",
        branches=[
            ("low", 0.25, 200, "competitor_bid"),
            ("medium", 0.50, 400, "competitor_bid"),
            ("high", 0.25, 600, "competitor_bid"),
        ],
    )
    nodes.add_chance(
        name="competitor_bid",
        branches=[
            ("low", 0.35, 400, "profit"),
            ("medium", 0.50, 600, "profit"),
            ("high", 0.15, 800, "profit"),
        ],
    )

    nodes.add_terminal(name="profit", payoff_fn=payoff_fn)

    nodes.set_outcome(200, cost="low", competitor_bid="low")
    nodes.set_outcome(400, cost="low", competitor_bid="medium")
    nodes.set_outcome(600, cost="low", competitor_bid="high")

    nodes.set_outcome(400, cost="medium", competitor_bid="low")
    nodes.set_outcome(600, cost="medium", competitor_bid="medium")
    nodes.set_outcome(800, cost="medium", competitor_bid="high")

    nodes.set_outcome(600, cost="high", competitor_bid="low")
    nodes.set_outcome(800, cost="high", competitor_bid="medium")
    nodes.set_outcome(1000, cost="high", competitor_bid="high")

    return nodes


def oil_tree_example():
    """PrecisionTree Oil Example.


    This function returns the data nodes structure for the oil example in
    discuted in the PrecisionTree user guide.

    """

    def payoff_fn(**kwargs):
        values = kwargs["values"]
        test_decision = values["test_decision"]
        drill_decision = values["drill_decision"]
        oil_found = values["oil_found"] if "oil_found" in values.keys() else 0
        return oil_found - drill_decision - test_decision

    nodes = DataNodes()

    nodes.add_decision(
        name="test_decision",
        branches=[
            ("test", 55, "test_results"),
            ("dont-test", 0, "drill_decision"),
        ],
        maximize=True,
    )

    nodes.add_chance(
        name="test_results",
        branches=[
            ("dry", 0.38, 0, "drill_decision"),
            ("small", 0.39, 0, "drill_decision"),
            ("large", 0.23, 0, "drill_decision"),
        ],
    )

    nodes.add_decision(
        name="drill_decision",
        branches=[
            ("drill", 600, "oil_found"),
            ("dont-drill", 0, "profit"),
        ],
        maximize=True,
    )

    nodes.add_chance(
        name="oil_found",
        branches=[
            ("dry-well", 0.7895, 0, "profit"),
            ("small-well", 0.1579, 1500, "profit"),
            ("large-well", 0.0526, 3400, "profit"),
        ],
    )

    nodes.add_terminal(name="profit", payoff_fn=payoff_fn)

    nodes.set_probability(0.5000, test_decision="dont-test", oil_found="dry-well")
    nodes.set_probability(0.3000, test_decision="dont-test", oil_found="small-well")
    nodes.set_probability(0.2000, test_decision="dont-test", oil_found="large-well")

    nodes.set_probability(0.3846, test_results="small", oil_found="dry-well")
    nodes.set_probability(0.4615, test_results="small", oil_found="small-well")
    nodes.set_probability(0.1538, test_results="small", oil_found="large-well")

    nodes.set_probability(0.2174, test_results="large", oil_found="dry-well")
    nodes.set_probability(0.2609, test_results="large", oil_found="small-well")
    nodes.set_probability(0.5217, test_results="large", oil_found="large-well")

    return nodes
