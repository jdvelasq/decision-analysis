"""
Value Sensitivity Analysis


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
    def __init__(
        self,
        decisiontree: DecisionTree,
        varname: str,
        branch_name: str,
        values: tuple,
        idx: int = 0,
        n_points=11,
    ) -> None:

        self._decisiontree = decisiontree
        self._varname = varname
        self._branch_name = branch_name
        self._values = values
        self._idx = idx
        self._n_points = n_points

        type_ = self._decisiontree._tree_nodes[self._idx]["type"]
        if type_ == "CHANCE":
            self._chance()
        if type_ == "DECISION":
            self._decision()

    def __repr__(self):
        return self.df_.__repr__()

    def _set_branch_value(self, value):

        for i_node, node in enumerate(self._decisiontree._tree_nodes):
            tag_name = node.get("tag_name")
            tag_branch = node.get("tag_branch")
            if tag_name == self._varname and tag_branch == self._branch_name:
                self._decisiontree._tree_nodes[i_node]["tag_value"] = value

    def _chance(self):

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

    def _decision(self):

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

        self.df_ = pd.concat(
            [
                pd.DataFrame(
                    {
                        "Branch": [branch_name] * len(self.branch_values_),
                        "Value": self.branch_values_,
                        "ExpVal": self.expected_values_[branch_name],
                    }
                )
                for branch_name in branch_names
            ]
        )

    def plot(self):

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
