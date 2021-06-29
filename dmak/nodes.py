"""
Node types
-------------------------------------------------------------------------------

This module is used to create and characterize the nodes of the tree. The 
package implements three types of nodes:

* Terminal nodes.

* Decision nodes.

* Chance nodes.


"""

from typing import Any, List
import copy


class Nodes:
    """This is a bag used to create and contain the different types of the
    tree nodes. The functions `terminal`, `chance`, and `decision` are used
    to create the nodes.
    """

    def __init__(self):
        self.data = {}

    def __getitem__(self, name: str) -> dict:
        return self.data[name]

    def copy(self):
        """Creates a deep copy of the bag. This function is used internally
        by the package."""
        result = Nodes()
        result.data = copy.deepcopy(self.data)
        return result

    def chance(
        self, name: str, branches: List[tuple], forced_branch: int = None
    ) -> None:
        """Adds a chance node to the bag.

        :param name:
            Name assigned to the node.

        :param branches:
            A list of tuples, where each tuple contains the following information:

            * Probability.

            * Associated value to the branch.

            * Name of the successor node.

        :param forced_branch:
            When used, this parameter uses the only the indicated branch in the
            computations. It is equivalent to know with certainty what state of
            ther world will occurrs. It is used to analyze the impact of the
            occurrence of a certain event on the decision.

        **Example**

        The following code a chance node with three branches; the first value
        of each branch is the probability.

        >>> nodes = Nodes()
        >>> nodes.chance(
        ...     name="ChanceNode",
        ...     branches=[
        ...         (.20, 100, "next-node"),
        ...         (.30, 200, "next-node"),
        ...         (.50, 300, "next-node"),
        ...     ],
        ... )
        >>> nodes.summary() # doctest: +NORMALIZE_WHITESPACE


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
        """Adds a decision node to the bag.

        :param name:
            Name assigned to the node.


        :param branches:
            A list of tuples, where each tuple contains the following information:

            * Associated value to the branch.

            * Name of the successor node.

        :param max_:
            When it is `True`, selects the branch with the maximum expected value.


        :param forced_branch:
            When used, this parameter uses the only the indicated branch in the
            computations. It is equivalent to know with certainty what state of
            ther world will occurrs. It is used to analyze the impact of the
            occurrence of a certain event on the decision.

        **Example**

        The following code a decision node with four branches.

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
        >>> nodes.summary() # doctest: +NORMALIZE_WHITESPACE
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
        """Adds a decision node to the bag.


        :param name:
            Name assigned to the node.

        :param user_fn:
            It is a valid python function used for computing the value
            of the terminal node in the tree. The names of the created
            nodes must be used as the parameters of the function.

        **Example**

        The following code creates a terminal node that uses a
        user-defined function to compute its expected value.

        >>> nodes = Nodes()
        >>> def user_fn(x):
        ...     return x
        >>> nodes.terminal(name='terminal_node', user_fn=user_fn)
        >>> nodes.summary() # doctest: +NORMALIZE_WHITESPACE
        Node 0
            Type: TERMINAL
            Name: terminal_node
            User fn: (User fn)
        <BLANKLINE>

        """

        self.data[name] = {
            "type": "TERMINAL",
            "user_fn": user_fn,
            "forced_branch": None,
        }

    def __repr__(self):
        def repr_terminal(text: list[str], idx: int, name: str) -> list[str]:
            text = text[:]
            text.append("{:<2d} T {:<10s}".format(idx, name))
            return text

        def repr_chance(text: list, idx: int, name: str) -> list:
            text = text[:]
            for branch in self.data[name]["branches"]:
                prob, outcome, successor = branch
                branch_text = "{:.3f}".format(prob)[1:] + "  {:6.2f} {:<10s}".format(
                    outcome, successor
                )
                if branch == self.data[name]["branches"][0]:
                    branch_text = "{:<2d} C {:<10s}".format(idx, name) + branch_text
                else:
                    branch_text = " " * 15 + branch_text
                text.append(branch_text)
            return text

        def repr_decision(text: list, idx: int, name: str) -> list:
            text = text[:]
            for branch in self.data[name]["branches"]:
                outcome, successor = branch
                branch_text = "      {:6.2f} {:<10s}".format(outcome, successor)
                if branch == self.data[name]["branches"][0]:
                    branch_text = "{:<2d} D {:<10s}".format(idx, name) + branch_text
                else:
                    branch_text = " " * 15 + branch_text
                text.append(branch_text)
            return text

        text = []
        for idx, name in enumerate(self.data.keys()):
            type_ = self.data[name]["type"]
            if type_ == "TERMINAL":
                text = repr_terminal(text, idx, name)
            if type_ == "CHANCE":
                text = repr_chance(text, idx, name)
            if type_ == "DECISION":
                text = repr_decision(text, idx, name)
        return "\n".join(text)

    def summary(self):
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
                    "           {:6.2f}  {:12.3f}  {:s}".format(
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

        return print("\n".join(text))


if __name__ == "__main__":

    import doctest

    doctest.testmod()
