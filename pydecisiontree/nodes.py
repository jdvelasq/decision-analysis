"""
Variables
-------------------------------------------------------------------------------
"""

from typing import Any, List


class Nodes:
    """
    Create a list of variables conformint the tree.

    """

    def __init__(self):
        self.data = {}

    def __getitem__(self, name: str) -> dict:
        return self.data[name]

    def chance(self, name: str, branches: List[tuple]) -> None:
        """Adds a chance node."""
        self.data[name] = {
            "type": "CHANCE",
            "branches": branches,
        }

    def decision(self, name: str, branches: List[tuple], max_: bool = False) -> None:
        """Adds a decision node"""
        self.data[name] = {
            "type": "DECISION",
            "branches": branches,
            "max_": max_,
        }

    def terminal(self, name: str, user_fn: Any = None) -> None:
        """Adds a terminal node"""
        self.data[name] = {
            "type": "TERMINAL",
            "user_fn": user_fn,
        }

    def __repr__(self):
        def repr_decision(name, node):

            text = []
            text.append("    Type: " + node.get("type"))
            text[-1] += (
                " - Maximum Payoff" if node.get("max_") is True else " - Minimum Payoff"
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
