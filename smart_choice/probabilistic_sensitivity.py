"""
Probabilistic Sensitivity Analysis
===============================================================================


"""
from typing import Any
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


from .decisiontree import DecisionTree


LINEFMTS = [
    "-k",
    "--k",
    ".-k",
    ":k",
    "-r",
    "--r",
    ".-r",
    ":r",
    "-g",
    "--g",
    ".-g",
    ":g",
]


class ProbabilisticSensitivity:
    """Display a probabilistic sensitivity plot for a chance node.


    :param tree:
        Decision tree to be analized.

    :param varname:
        Name of the variable.

    :param idx:
        Identification number of the node of the tree used to collect the
        results. The identifier of the root node is `0` .

    """

    def __init__(self, decisiontree: DecisionTree, varname: str, idx: int = 0) -> Any:

        self._decisiontree = decisiontree.copy()
        self._varname = varname
        self._idx = idx

        #
        # Algorithm
        #
        type_ = self._decisiontree._data_nodes[varname]["type"]
        if type_ != "CHANCE":
            raise ValueError('Variable {} is {} != "CHANCE"'.format(varname, type_))

        type_root = self._decisiontree._tree_nodes[self._idx].get("type")
        if type_root == "CHANCE":
            self.probabilistic_sensitivity_chance()
        if type_root == "DECISION":
            self.probabilistic_sensitivity_decision()

    def __repr__(self):
        return self.df_.__repr__()

    def _get_top_bottom_branches(self):

        (
            self._top_branch,
            self._bottom_branch,
        ) = self._decisiontree._data_nodes.get_top_bottom_branches(self._varname)

    def _set_branch_probabilities_to_zero(self):
        for i_node, node in enumerate(self._decisiontree._tree_nodes):
            tag_name = node.get("tag_name")
            if tag_name == self._varname:
                self._decisiontree._tree_nodes[i_node]["tag_prob"] = 0

    def _set_branch_probabilities(self, top_probability):

        for i_node, node in enumerate(self._decisiontree._tree_nodes):
            tag_name = node.get("tag_name")
            if tag_name == self._varname:
                tag_branch = node.get("tag_branch")
                if tag_branch == self._top_branch:
                    self._decisiontree._tree_nodes[i_node]["tag_prob"] = (
                        1 - top_probability
                    )
                if tag_branch == self._bottom_branch:
                    self._decisiontree._tree_nodes[i_node]["tag_prob"] = top_probability

    def probabilistic_sensitivity_chance(self) -> None:

        self._get_top_bottom_branches()
        self._set_branch_probabilities_to_zero()
        self.probabilities_ = np.linspace(start=0, stop=1, num=21).tolist()
        self.expected_values_ = []

        for top_probability in self.probabilities_:
            self._set_branch_probabilities(top_probability)
            self._decisiontree.rollback()
            expval = self._decisiontree._tree_nodes[self._idx].get("EV")
            self.expected_values_.append(expval)

        self.df_ = pd.DataFrame(
            {
                "Probability": self.probabilities_,
                "Expected Value": self.expected_values_,
            }
        )

    def probabilistic_sensitivity_decision(self) -> None:

        self._get_top_bottom_branches()
        self._set_branch_probabilities_to_zero()

        successors = self._decisiontree._tree_nodes[self._idx].get("successors")
        tag_branches = [
            self._decisiontree._tree_nodes[successor].get("tag_branch")
            for successor in successors
        ]

        self.expected_values_ = {}
        for tag_branch in tag_branches:
            self.expected_values_[tag_branch] = []

        self.probabilities_ = np.linspace(start=0, stop=1, num=21).tolist()
        for top_probability in self.probabilities_:

            self._set_branch_probabilities(top_probability)
            self._decisiontree.rollback()

            expvals = [
                self._decisiontree._tree_nodes[successor].get("EV")
                for successor in successors
            ]
            for expval, tag_branch in zip(expvals, tag_branches):
                self.expected_values_[tag_branch].append(expval)

        self.df_ = pd.concat(
            [
                pd.DataFrame(
                    {
                        "Branch": [str(tag_branch)] * len(self.probabilities_),
                        "Probability": self.probabilities_,
                        "Value": self.expected_values_[tag_branch],
                    }
                )
                for tag_branch in self.expected_values_.keys()
            ]
        )

    def plot(self):
        """Plots the sensitivty to probability."""

        if isinstance(self.expected_values_, dict):
            for fmt, tag_branch in zip(LINEFMTS, self.expected_values_.keys()):
                plt.gca().plot(
                    self.probabilities_,
                    self.expected_values_[tag_branch],
                    fmt,
                    label=tag_branch,
                )
        else:
            plt.gca().plot(self.probabilities_, self.expected_values_, "-k")

        plt.gca().spines["bottom"].set_visible(False)
        plt.gca().spines["left"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        plt.gca().spines["top"].set_visible(False)
        plt.gca().set_ylabel("Expected values")
        plt.gca().set_xlabel("Probability")
        plt.legend()
        plt.grid()
