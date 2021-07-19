"""
Risk Profile Analysis
===============================================================================



"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .decisiontree import DecisionTree

LINEFMTS = [
    "-k",
    "-b",
    "-r",
    "-g",
    ".-k",
    ".-b",
    ".-r",
    ".-g",
    "--k",
    ".-k",
    "o-k",
    "--k",
    "--b",
    "--r",
    "--g",
    "-.k",
    "-.b",
    "-.r",
    "-.g",
]

COLORS = ["black", "blue", "red", "green"] * 3


class RiskProfile:
    """Plots a probability distribution of the tree results computed in a designed node.

    :param tree:
        The decision tree to be analyzed.

    :param idx:
        The identification number of the tree node to be analyzed.

    :param cumulative:
        When `True`, displays the cumulative distribution at the analized node.

    :param single:
        When `True`, displays the value for the optimal branch in decision nodes.
        When `False` display the value for all branches of the analyzed node.


    """

    def __init__(
        self,
        decisiontree: DecisionTree,
        idx: int = 0,
        cumulative: bool = False,
        single: bool = True,
    ):
        self._decisiontree = decisiontree.copy()
        self._idx = idx
        self._cumulative = cumulative
        self._single = single

        self.df_ = {}

        self._rollback_risk_profiles()
        self._compute_risk_profiles()

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

    #
    #
    # Computation
    #
    #
    def _rollback_risk_profiles(self) -> None:
        #
        def terminal(idx: int) -> None:
            value: float = self._decisiontree._tree_nodes[idx].get("EV")
            self._decisiontree._tree_nodes[idx]["RiskProfile"] = {value: 1.0}

        def chance(idx: int) -> None:
            successors = self._decisiontree._tree_nodes[idx].get("successors")
            for successor in successors:
                dispatch(idx=successor)
            self._decisiontree._tree_nodes[idx]["RiskProfile"] = {}
            for successor in successors:
                prob = self._decisiontree._tree_nodes[successor].get("tag_prob")

                for value_successor, prob_successor in self._decisiontree._tree_nodes[
                    successor
                ]["RiskProfile"].items():
                    if (
                        value_successor
                        in self._decisiontree._tree_nodes[idx]["RiskProfile"].keys()
                    ):
                        self._decisiontree._tree_nodes[idx]["RiskProfile"][
                            value_successor
                        ] += (prob * prob_successor)
                    else:
                        self._decisiontree._tree_nodes[idx]["RiskProfile"][
                            value_successor
                        ] = (prob * prob_successor)

        def decision(idx: int) -> None:
            successors = self._decisiontree._tree_nodes[idx].get("successors")
            for successor in successors:
                dispatch(idx=successor)
            optimal_successor = self._decisiontree._tree_nodes[idx].get(
                "optimal_successor"
            )
            self._decisiontree._tree_nodes[idx][
                "RiskProfile"
            ] = self._decisiontree._tree_nodes[optimal_successor]["RiskProfile"]

        def dispatch(idx: int) -> None:
            type_ = self._decisiontree._tree_nodes[idx].get("type")
            if type_ == "TERMINAL":
                terminal(idx=idx)
            if type_ == "CHANCE":
                chance(idx=idx)
            if type_ == "DECISION":
                decision(idx=idx)

        dispatch(idx=self._idx)

    def _compute_risk_profiles(self) -> None:
        #
        def compute(idx: int):

            risk_profile = self._decisiontree._tree_nodes[idx].get("RiskProfile").copy()
            values = sorted(risk_profile.keys())
            probs = [risk_profile[value] for value in values]
            cumprobs = np.cumsum(probs).tolist()

            expval = self._decisiontree._tree_nodes[idx].get("EV")
            tag_branch = self._decisiontree._tree_nodes[idx].get("tag_branch")
            if tag_branch is not None:
                label = "{}; EV={:.2f}".format(tag_branch, expval)
            else:
                label = "EV={:.2f}".format(expval)

            df_ = pd.DataFrame(
                {
                    "Value": values,
                    "Probability": probs,
                    "Cumulative Probability": cumprobs,
                }
            )

            return label, df_

        def single(idx: int):
            label, df_ = compute(idx)
            self.df_[label] = df_

        def multiple(idx):
            successors = self._decisiontree._tree_nodes[idx].get("successors")
            for successor in successors:
                label, df_ = compute(idx=successor)
                self.df_[label] = df_

        if self._single is True:
            single(self._idx)
        else:
            multiple(self._idx)

    #
    #
    # Plots
    #
    #
    def plot(self):
        """Risk profile plot."""
        #
        def format_plot():
            plt.gca().spines["bottom"].set_visible(False)
            plt.gca().spines["left"].set_visible(False)
            plt.gca().spines["right"].set_visible(False)
            plt.gca().spines["top"].set_visible(False)

            plt.gca().set_xlabel("Expected values")
            plt.gca().set_ylabel("Probability")
            plt.gca().legend()
            plt.grid()

        def stem_plot():

            for i_key, key in enumerate(self.df_.keys()):
                df_ = self.df_[key]
                x_points = df_["Value"]
                y_points = df_["Probability"]
                markerline, _, _ = plt.gca().stem(
                    x_points,
                    y_points,
                    linefmt=LINEFMTS[i_key],
                    basefmt="gray",
                    label=key,
                )
                markerline.set_markerfacecolor(COLORS[i_key])
                markerline.set_markeredgecolor(COLORS[i_key])

            format_plot()

        def step_plot():

            for i_key, key in enumerate(self.df_.keys()):
                df_ = self.df_[key]
                x_points = df_["Value"].tolist()
                x_points += [x_points[-1]]
                y_points = [0] + df_["Cumulative Probability"].tolist()
                plt.gca().step(
                    x_points, y_points, LINEFMTS[i_key], label=key, alpha=0.8
                )

            format_plot()

        if self._cumulative is False:
            stem_plot()
        else:
            step_plot()
