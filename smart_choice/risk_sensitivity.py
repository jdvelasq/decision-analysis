"""
Risk Sensitivity Analysis
===============================================================================

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


from .decisiontree import DecisionTree


class RiskAttitudeSensitivity:
    """Displays the sensitivity to risk attitude.

    :param decisiontree:
        The decision tree to be analyzed.

    :param utility_fn:
        Utility function to be used.

        * `"exp"`: exponential utility function.

        * `"log"`: logarithmic utility function.

    :param risk_tolerance:
        Risk tolerance of the decision-maker.

    :param idx:
        Identification number of the node to be analyzed.

    """

    def __init__(
        self, decisiontree: DecisionTree, utility_fn: str, risk_tolerance, idx: int = 0
    ):

        self._decisiontree = decisiontree
        self._risk_tolerance = risk_tolerance
        self._utility_fn = utility_fn
        self._idx = idx

        # computation
        self.type_ = decisiontree._tree_nodes[0].get("type")
        if self.type_ == "DECISION":
            self._risk_attitude_decision()
        if self.type_ == "CHANCE":
            self._risk_attitude_chance()

        self._decisiontree.rollback()

    def __repr__(self):
        return self.df_.__repr__()

    def _prepare(self):

        successors = self._decisiontree._tree_nodes[0].get("successors")

        self.branch_names_ = [
            self._decisiontree._tree_nodes[successor].get("tag_branch")
            for successor in successors
        ]

        self.risk_aversions_ = np.linspace(
            start=0, stop=1.0 / self._risk_tolerance, num=11
        ).tolist()

        self.risk_tolerance_ = [
            "Infinity"
            if risk_aversion == np.float(0)
            else int(round(1 / risk_aversion, 0))
            for risk_aversion in self.risk_aversions_
        ]

    def _risk_attitude_decision(self):

        self._prepare()

        self.certainty_equivalents_ = {}
        for tag_branch in self.branch_names_:
            self.certainty_equivalents_[tag_branch] = []

        successors = self._decisiontree._tree_nodes[self._idx].get("successors")
        for risk_aversion in self.risk_aversions_:

            if risk_aversion == np.float64(0):
                self._decisiontree.evaluate()
                self._decisiontree.rollback()
                ceqs = [
                    self._decisiontree._tree_nodes[successor].get("EV")
                    for successor in successors
                ]
            else:
                self._decisiontree.rollback(
                    utility_fn=self._utility_fn, risk_tolerance=1.0 / risk_aversion
                )
                ceqs = [
                    self._decisiontree._tree_nodes[successor].get("CE")
                    for successor in successors
                ]

            for ceq, tag_branch in zip(ceqs, self.branch_names_):
                self.certainty_equivalents_[tag_branch].append(ceq)

        results = self.certainty_equivalents_.copy()
        results["Risk Tolerance"] = self.risk_tolerance_
        self.df_ = pd.DataFrame(results)

    def _risk_attitude_chance(self):

        self.certainty_equivalents_ = []

        for risk_aversion in self.risk_aversions_:

            if risk_aversion == np.float64(0):
                self._decisiontree.evaluate()
                self._decisiontree.rollback()
                ceq = self._decisiontree._tree_nodes[0].get("EV")
            else:
                self._decisiontree.evaluate()
                self._decisiontree.rollback(
                    utility_fn=self._utility_fn, risk_tolerance=1.0 / risk_aversion
                )
                ceq = self._decisiontree._tree_nodes[self._idx].get("CE")
            self.certainty_equivalents_.append(ceq)

        name = self._decisiontree._tree_nodes[self._idx].name
        results = {name: self.certainty_equivalents_}
        results["Risk Tolerance"] = self.risk_tolerance_
        self.df_ = pd.DataFrame(results)

    def _format_plot(self):
        plt.xticks(self.risk_aversions_, self.risk_tolerance_)
        plt.gca().spines["bottom"].set_visible(False)
        plt.gca().spines["left"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        plt.gca().spines["top"].set_visible(False)
        plt.gca().set_ylabel("Expected values")
        plt.gca().set_xlabel("Risk tolerance")
        # plt.gca().invert_xaxis()
        plt.gca().legend()
        plt.grid()

    #
    # Plot
    #

    def plot(self):
        """Plots the sensibility to risk attitude."""

        if self.type_ == "DECISION":
            self._plot_decision()
        if self.type_ == "CHANCE":
            self._plot_chance()
        self._format_plot()

    def _plot_chance(self):

        for tag_branch in self.branch_names_:
            plt.gca().plot(
                self.risk_aversions_,
                self.certainty_equivalents_[tag_branch],
                label=tag_branch,
            )

    def _plot_decision(self):

        linefmts = [
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
        for linefmt, tag_branch in zip(linefmts, self.branch_names_):
            plt.gca().plot(
                self.risk_aversions_,
                self.certainty_equivalents_[tag_branch],
                linefmt,
                label=tag_branch,
            )
