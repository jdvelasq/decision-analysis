"""
Node types
-------------------------------------------------------------------------------

This module is used to create and characterize the nodes of the tree. The
package implements three types of nodes:

* Terminal nodes.

* Decision nodes.

* Chance nodes.


"""

import copy
from textwrap import shorten
from typing import Any, List

NAMEMAXLEN = 20


class Nodes:
    """This is a bag used to create and contain the different types of the
    tree nodes. The functions `terminal`, `chance`, and `decision` are used
    to create the nodes.
    """

    def __init__(self, chance_probabilities="must_100%"):
        self.data = {}
        self._chance_probabilities = chance_probabilities

    def __getitem__(self, name: str) -> dict:
        return self.data[name]

    def copy(self):
        """Creates a deep copy of the bag. This function is used internally
        by the package."""
        result = Nodes()
        result.data = copy.deepcopy(self.data)
        return result

    def chance(self, name: str, branches: List[tuple]) -> None:
        """Adds a chance node to the bag.

        :param name:
            Name assigned to the node.

        :param branches:
            A list of tuples, where each tuple contains the following information:

            * Name of the branch.

            * Probability.

            * Associated value to the branch.

            * Name of the successor node.

        :param forced_branch:
            When used, this parameter uses the only the indicated branch in the
            computations. It is equivalent to know with certainty what state of
            ther world will occurrs. It is used to analyze the impact of the
            occurrence of a certain event on the decision.


        """
        #
        # Checks branch information.
        #
        for i_branch, branch in enumerate(branches):
            if len(branch) != 4:
                raise ValueError(
                    "Branch #{} of variable {} has invalid information".format(
                        name, i_branch
                    )
                )

        #
        # Normalize probability
        #
        probabilities = [prob for _, prob, _, _ in branches]

        if self._chance_probabilities == "must_100%":
            if sum(probabilities) != float(1):
                raise ValueError(
                    "Sum of probabilities for variable {} has must be 100%".format(name)
                )

        if self._chance_probabilities == "normalize" and sum(probabilities) != 1.0:
            probabilities = [prob / sum(probabilities) for prob in probabilities]
            for i_branch, (branch, prob) in enumerate(zip(branches, probabilities)):
                branch_name, _, value, next_node = branch
                branches[i_branch] = (branch_name, prob, value, next_node)

        self.data[name] = {
            "type": "CHANCE",
            "branches": branches,
        }

    def decision(
        self,
        name: str,
        branches: List[tuple],
        maximize: bool = False,
    ) -> None:
        """Adds a decision node to the bag.

        :param name:
            Name assigned to the node.

        :param branches:
            A list of tuples, where each tuple contains the following information:

            * Name of the branch.

            * Associated value to the branch.

            * Name of the successor node.

        :param max_:
            When it is `True`, selects the branch with the maximum expected value.

        :param forced_branch:
            When used, this parameter forces the seleccion of the indicated branch
            in the computations. It is equivalent to know with certainty what state of
            ther world will occurrs. It is used to analyze the impact of the
            occurrence of a certain event on the decision.

        **Example**

        The following code a decision node with four branches.




        """
        for i_branch, branch in enumerate(branches):
            if len(branch) != 3:
                raise ValueError(
                    "Branch #{} of variable {} has invalid information".format(
                        name, i_branch
                    )
                )

        self.data[name] = {
            "type": "DECISION",
            "branches": branches,
            "maximize": maximize,
        }

    def terminal(self, name: str, payoff_fn: Any = None) -> None:
        """Adds a decision node to the bag.

        :param name:
            Name assigned to the node.

        :param user_fn:
            It is a valid python function used for computing the value
            of the terminal node in the tree. The names of the created
            nodes must be used as the parameters of the function.

        """
        self.data[name] = {
            "type": "TERMINAL",
            "payoff_fn": payoff_fn,
            "forced_branch": None,
        }

    def __repr__(self):
        def repr_terminal(text: List[str], idx: int, name: str) -> List[str]:
            text = text[:]
            if len(name) > 15:
                varname = name[:12] + "..."
            else:
                varname = name
            text.append("{:<2d} T {:<15s}".format(idx, varname))
            return text

        def repr_chance(text: list, idx: int, name: str) -> list:
            text = text[:]
            for branch in self.data[name]["branches"]:
                name_, prob, outcome, successor = branch
                name_ = shorten(name_, width=NAMEMAXLEN, placeholder="...")
                fmt = "{:<" + str(NAMEMAXLEN) + "s}"
                branch_text = fmt.format(name_) + " "
                branch_text += "{:.3f}".format(prob)[1:] if prob < 1.0 else "1.00"
                branch_text += " {:6.2f} {:<s}".format(outcome, successor)
                if branch == self.data[name]["branches"][0]:
                    if len(name) > 15:
                        varname = name[:12] + "..."
                    else:
                        varname = name
                    branch_text = "{:<2d} C {:<15s} ".format(idx, varname) + branch_text
                else:
                    branch_text = " " * 21 + branch_text
                text.append(branch_text)
            return text

        def repr_decision(text: list, idx: int, name: str) -> list:
            text = text[:]
            for branch in self.data[name]["branches"]:
                name_, outcome, successor = branch
                name_ = shorten(name_, width=NAMEMAXLEN, placeholder="...")
                fmt = "{:<" + str(NAMEMAXLEN) + "s}"
                branch_text = fmt.format(name_) + " "
                branch_text += "     {:6.2f} {:<s}".format(outcome, successor)
                if branch == self.data[name]["branches"][0]:
                    if len(name) > 15:
                        varname = name[:12] + "..."
                    else:
                        varname = name
                    branch_text = "{:<2d} D {:<15s} ".format(idx, varname) + branch_text
                else:
                    branch_text = " " * 21 + branch_text
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

        text = [line.rstrip() for line in text]
        return "\n".join(text)

    def get_top_bottom_branches(self, name):
        """Gets the position of the branches with top and bottom values."""
        branches = self.data[name].get("branches")
        type_ = self.data[name].get("type")
        if type_ == "DECISION":
            values = [branch[1] for branch in branches]
        if type_ == "CHANCE":
            values = [branch[2] for branch in branches]
        top_branch = values.index(max(values))
        bottom_branch = values.index(min(values))
        return top_branch, bottom_branch

    def set_probabitlities_to_zero(self, name):
        """Set to zero the probabilities of the all branchs of variable."""
        for i_branch, branch in enumerate(self.data[name]["branches"]):
            self.data[name]["branches"][i_branch] = (
                branch[0],
                0.0,
                branch[2],
                branch[3],
            )

    # def summary(self):
    #     def repr_decision(name, node):

    #         text = []
    #         text.append("    Type: " + node.get("type"))
    #         text[-1] += (
    #             " - Maximum Payoff" if node.get("max") is True else " - Minimum Payoff"
    #         )
    #         text.append("    Name: " + name)
    #         text.append("    Branches:")
    #         text.append("                         Value  Next Node")
    #         for (outcome, next_node) in node.get("branches"):
    #             text.append(
    #                 "                  {:12.3f}  {:s}".format(outcome, next_node)
    #             )
    #         text.append("")
    #         return text

    #     def repr_chance(name, node):
    #         text = []
    #         text.append("    Type: " + node.get("type"))
    #         text.append("    Name: " + name)
    #         text.append("    Branches:")
    #         text.append("          Chance         Value  Next Node")
    #         for (prob, outcome, next_node) in node.get("branches"):
    #             text.append(
    #                 "           {:6.2f}  {:12.3f}  {:s}".format(
    #                     prob, outcome, next_node
    #                 )
    #             )
    #         text.append("")
    #         return text

    #     def repr_terminal(name, node):
    #         text = []
    #         text.append("    Type: " + node.get("type"))
    #         text.append("    Name: " + name)
    #         if node.get("user_fn") is None:
    #             text.append("    User fn: (cumulative)")
    #         else:
    #             text.append("    User fn: (User fn)")
    #         text.append("")
    #         return text

    #     text = []
    #     for i_node, (name, node) in enumerate(self.data.items()):
    #         text.append("Node {}".format(i_node))
    #         if node.get("type") == "DECISION":
    #             text += repr_decision(name=name, node=node)
    #         if node.get("type") == "CHANCE":
    #             text += repr_chance(name=name, node=node)
    #         if node.get("type") == "TERMINAL":
    #             text += repr_terminal(name=name, node=node)

    #     return print("\n".join(text))


if __name__ == "__main__":

    import doctest

    doctest.testmod()
