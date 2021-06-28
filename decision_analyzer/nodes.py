"""
Variables
-------------------------------------------------------------------------------


"""

from typing import Any, List
import copy


class Nodes:
    """Creates a dictionary with the variables used internally by the decision tree."""

    def __init__(self):
        self.data = {}

    def __getitem__(self, name: str) -> dict:
        return self.data[name]

    def copy(self):
        """Creates a copy of the object."""
        result = Nodes()
        result.data = copy.deepcopy(self.data)
        return result

    def chance(
        self, name: str, branches: List[tuple], forced_branch: int = None
    ) -> None:
        """Adds a chance node.

        :param name:
                     Name of the variable.

        :param branches:
                    A list of tuples, where each tuple contains the corresponding information of
                    each branch in the node. Each tuple has the probability, the value of the
                    branch and the name of the next node.

        >>> nodes = Nodes()
        >>> nodes.chance(
        ...     name="ChanceNode",
        ...     branches=[
        ...         (20.0, 100, "next-node"),
        ...         (30.0, 200, "next-node"),
        ...         (50.0, 300, "next-node"),
        ...     ],
        ... )
        >>> nodes # doctest: +NORMALIZE_WHITESPACE
        Node 0
            Type: CHANCE
            Name: ChanceNode
            Branches:
                  Chance         Value  Next Node
                   20.00       100.000  next-node
                   30.00       200.000  next-node
                   50.00       300.000  next-node
        <BLANKLINE>

        """

        self.data[name] = {
            "type": "CHANCE",
            "branches": branches,
            "forced_branch": forced_branch,
        }

    def decision(
        self,
        name: str,
        branches: List[tuple],
        max_: bool = False,
        forced_branch: int = None,
    ) -> None:
        """Creates a decisions tree's internal decision node.

        :param name:
            A valid name for variables in Python.

        :param branches:
            A list of tuples, where each tuple contains the corresponding
            information of each branch in the node. Each tuple has the value
            of the branch and the name of the next node.

        :param max_:
            When it is `True`, selects the branch with the maximum expected value.


        >>> nodes = Nodes()
        >>> nodes.decision(
        ...     name='DecisionNode',
        ...     branches=[
        ...         (100,  'next-node'),
        ...         (200,  'next-node'),
        ...         (300,  'next-node'),
        ...         (400,  'next-node'),
        ...    ],
        ...    max_=True,
        ... )
        >>> nodes # doctest: +NORMALIZE_WHITESPACE
        Node 0
            Type: DECISION - Maximum Payoff
            Name: DecisionNode
            Branches:
                                 Value  Next Node
                               100.000  next-node
                               200.000  next-node
                               300.000  next-node
                               400.000  next-node
        <BLANKLINE>

        """

        self.data[name] = {
            "type": "DECISION",
            "branches": branches,
            "max": max_,
            "forced_branch": forced_branch,
        }

    def terminal(self, name: str, user_fn: Any = None) -> None:
        """Creates a decision tree's terminal node.

        :param name:
            A valid name for variables in Python.

        :param user_fn:
            It is a valid python function used for computing the value of the
            terminal node in the tree. The names of the nodes must be used as
            the parameters of the function.


        >>> nodes = Nodes()
        >>> def user_fn(x):
        ...     return x
        >>> nodes.terminal(name='terminal_node', user_fn=user_fn)
        >>> nodes # doctest: +NORMALIZE_WHITESPACE
        Node 0
            Type: TERMINAL
            Name: terminal_node
            User fn: (User fn)
        <BLANKLINE>

        """

        self.data[name] = {
            "type": "TERMINAL",
            "user_fn": user_fn,
        }

    def __repr__(self):
        def repr_decision(name, node):

            text = []
            text.append("    Type: " + node.get("type"))
            text[-1] += (
                " - Maximum Payoff" if node.get("max") is True else " - Minimum Payoff"
            )
            text.append("    Name: " + name)
            text.append("    Branches:")
            text.append("                         Value  Next Node")
            for (outcome, next_node) in node.get("branches"):
                text.append(
                    "                  {:12.3f}  {:s}".format(outcome, next_node)
                )
            text.append("")
            return text

        def repr_chance(name, node):
            text = []
            text.append("    Type: " + node.get("type"))
            text.append("    Name: " + name)
            text.append("    Branches:")
            text.append("          Chance         Value  Next Node")
            for (prob, outcome, next_node) in node.get("branches"):
                text.append(
                    "           {:5.2f}  {:12.3f}  {:s}".format(
                        prob, outcome, next_node
                    )
                )
            text.append("")
            return text

        def repr_terminal(name, node):
            text = []
            text.append("    Type: " + node.get("type"))
            text.append("    Name: " + name)
            if node.get("user_fn") is None:
                text.append("    User fn: (cumulative)")
            else:
                text.append("    User fn: (User fn)")
            text.append("")
            return text

        text = []
        for i_node, (name, node) in enumerate(self.data.items()):
            text.append("Node {}".format(i_node))
            if node.get("type") == "DECISION":
                text += repr_decision(name=name, node=node)
            if node.get("type") == "CHANCE":
                text += repr_chance(name=name, node=node)
            if node.get("type") == "TERMINAL":
                text += repr_terminal(name=name, node=node)

        return "\n".join(text)


if __name__ == "__main__":

    import doctest

    doctest.testmod()
