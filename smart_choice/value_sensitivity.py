"""
Value Sensitivity Analysis
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


class ValueSensitivity:
    """Displays sensitivity results to values in the decision tree.

    :param decisiontree:
        The decision tree to be analyzed.

    :param varname:
        Variable to be analyzed.

    :param branch_name:
        Name of the branch.

    :param values:
        Tuple with the minimal and maximum values to be analyzed.

    :param single:
        When `True`, returns the expected value for chance nodes, and the
        optimal decision for event nodes. When `False` return the values for
        all branches of the node.

    :param idx:
        Identification number of the node to be analyzed.

    :param n_points:
        Number of points used to create the plot.

    """

    def __init__(
        self,
        decisiontree: DecisionTree,
        varname: str,
        branch_name: str,
        values: tuple,
        single: bool = False,
        idx: int = 0,
        n_points=11,
    ) -> None:

        self._decisiontree = decisiontree.copy()
        self._varname = varname
        self._branch_name = branch_name
        self._values = values
        self._single = single
        self._idx = idx
        self._n_points = n_points

        if self._single is True:
            self._compute_sensitivity_single()
        else:
            self._compute_sensitivity_multiple()

    def __repr__(self):
        if isinstance(self.df_, dict):
            text = ""
            for key in self.df_.keys():
                if key != list(self.df_.keys())[0]:
                    text += "\n"
                text += key + "\n"
                text += self.df_[key].__repr__()
                # text += "\n"
            return text
        else:
            return self.df_.__repr__()

    def _get_base_value(self) -> None:

        for i_node, node in enumerate(self._decisiontree._tree_nodes):
            tag_name = node.get("tag_name")
            tag_branch = node.get("tag_branch")
            if tag_name == self._varname and tag_branch == self._branch_name:
                self._base_value = self._decisiontree._tree_nodes[i_node]["tag_value"]

    def _set_branch_value(self, value):

        for i_node, node in enumerate(self._decisiontree._tree_nodes):
            tag_name = node.get("tag_name")
            tag_branch = node.get("tag_branch")
            if tag_name == self._varname and tag_branch == self._branch_name:
                self._decisiontree._tree_nodes[i_node]["tag_value"] = value

    def _compute_sensitivity_single(self):

        self._get_base_value()

        min_value, max_value = self._values
        self.branch_values_ = np.linspace(
            start=min_value, stop=max_value, num=self._n_points
        )

        self.expected_values_ = []
        for branch_value in self.branch_values_:
            self._set_branch_value(branch_value)
            self._decisiontree.evaluate()
            self._decisiontree.rollback()
            expval = self._decisiontree._tree_nodes[self._idx].get("EV")
            self.expected_values_.append(expval)

        self.df_ = pd.DataFrame(
            {
                "Branch Value": self.branch_values_,
                "Expected Value": self.expected_values_,
            }
        )

    def _compute_sensitivity_multiple(self):

        min_value, max_value = self._values
        self.branch_values_ = np.linspace(
            start=min_value, stop=max_value, num=self._n_points
        )

        self.expected_values_ = {}
        successors = self._decisiontree._tree_nodes[self._idx].get("successors")
        branch_names = [
            self._decisiontree._tree_nodes[successor].get("tag_branch")
            for successor in successors
        ]
        for branch_name in branch_names:
            self.expected_values_[branch_name] = []

        for branch_value in self.branch_values_:

            self._set_branch_value(branch_value)
            self._decisiontree.evaluate()
            self._decisiontree.rollback()
            expvals = [
                self._decisiontree._tree_nodes[successor].get("EV")
                for successor in successors
            ]
            for expval, branch_name in zip(expvals, branch_names):
                self.expected_values_[branch_name].append(expval)

        self.df_ = {}
        for branch_name in self.expected_values_:
            self.df_[branch_name] = pd.DataFrame(
                {
                    "Value": self.branch_values_,
                    "ExpVal": self.expected_values_[branch_name],
                }
            )

    def plot(self):
        """Plots the sensitivity to values"""

        if isinstance(self.expected_values_, dict):
            for fmt, branch_name in zip(LINEFMTS, self.expected_values_.keys()):
                plt.gca().plot(
                    self.branch_values_,
                    self.expected_values_[branch_name],
                    fmt,
                    label=branch_name,
                )
                plt.gca().legend()
        else:
            plt.gca().plot(self.branch_values_, self.expected_values_, "-k")

        plt.gca().spines["bottom"].set_visible(False)
        plt.gca().spines["left"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        plt.gca().spines["top"].set_visible(False)
        plt.gca().set_ylabel("Expected values")
        plt.gca().set_xlabel("Branch Values")
        plt.grid()
