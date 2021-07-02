"""
Decision Tree Model
===============================================================================

The **DecisionTree** is the object used to represent the decision tree model.
This module is responsible for all functionality of the package. A typical 
sequence of use is the following:

* Create the nodes used to feed the tree (Module `nodes`).

* Create the tree.

* Build the internal structure of the tree.

* Evaluate the tree.

* Analyze plots and other results.

* Modify the structure of the tree and repeat the analysis.


"""
import json
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from graphviz import Digraph

from .nodes import Nodes


def _exp_utility_fn(risk_tolerance: float):
    def util_fn(value: float) -> float:
        return 1.0 - np.exp(-value / risk_tolerance)

    def inv_fn(value: float) -> float:
        return -1.0 * risk_tolerance * np.log(1 - np.minimum(0.9999, value))

    return util_fn, inv_fn


def _log_utility_fn(risk_tolerance: float):
    def util_fn(value: float) -> float:
        return np.log(value + risk_tolerance)

    def inv_fn(value: float):
        return np.exp(value) - risk_tolerance

    return util_fn, inv_fn


def _dummy_fn(value: float) -> float:
    return value


class DecisionTree:
    """Decision tree representation.


    :param variables:
        Types of nodes used in the tree. This parameter is created using the
        module `Nodes`.

    :param initial_variable:
        Name of the initial variable of the tree. Usually, the first variable
        in variables.

    :param utility:
        Utility function to be used. When is `None` the computed values of
        terminal nodes are used as the expected utility in the internal
        nodes of the tree. The module implements the following utility
        functions:

        * `exp`: Exponential utility function `U(x): 1 - exp(-x / param)`.

        * `log`: Logarithmic utility function `U(x) = log(x + param)`.


    :param param:
        Value of the parameter `param` in the utility function.

    """

    # -------------------------------------------------------------------------
    #
    #
    #  C R E A T I O N
    #
    #
    def __init__(
        self,
        variables: Nodes,
        initial_variable: str,
    ) -> None:

        self._nodes = None
        self._variables = variables.copy()
        self._initial_variable = initial_variable

        ## Prepares the empty structure of the tree
        self._build_skeleton()
        self._set_tag_attributes()

        ## run flags
        self._is_evaluated = False
        self._with_rollback = False

    # -------------------------------------------------------------------------
    #
    #
    #  T R E E    C R E A T I O N
    #
    #
    def _build_skeleton(self) -> None:
        #
        # Builds a structure where nodes are:
        #
        #   [
        #       {name: ..., type: ... successors: [ ... ]}
        #   ]
        #
        def dispatch(name: str) -> int:
            idx: int = len(self._nodes)
            type_: str = self._variables[name]["type"]
            forced: int = self._variables[name]["forced_branch"]
            self._nodes.append({"name": name, "type": type_, "forced": forced})
            if "maximize" in self._variables[name].keys():
                self._nodes[idx]["maximize"] = self._variables[name]["maximize"]
            if "branches" in self._variables[name].keys():
                successors: list = []
                for branch in self._variables[name].get("branches"):
                    successor: int = dispatch(name=branch[-1])
                    successors.append(successor)
                self._nodes[idx]["successors"] = successors
            return idx

        #
        self._nodes: list = []
        dispatch(name=self._initial_variable)

    def _set_tag_attributes(self) -> None:
        #
        # tag_value: is the value of the branch of the predecesor node
        # tag_prob: is the probability of the branch of the predecesor (chance) node
        #
        for node in self._nodes:

            if "successors" not in node.keys():
                continue

            name: str = node.get("name")
            successors: list = node.get("successors")
            type_: str = node.get("type")
            branches: list = self._variables[name].get("branches")

            if type_ == "DECISION":
                bnames = [x for x, _, _ in branches]
                values = [x for _, x, _ in branches]
                for successor, bname, value in zip(successors, bnames, values):
                    self._nodes[successor]["tag_branch"] = bname
                    self._nodes[successor]["tag_name"] = name
                    self._nodes[successor]["tag_value"] = value

            if type_ == "CHANCE":
                bnames = [x for x, _, _, _ in branches]
                values = [x for _, _, x, _ in branches]
                probs = [x for _, x, _, _ in branches]
                for successor, bname, value, prob in zip(
                    successors, bnames, values, probs
                ):
                    self._nodes[successor]["tag_branch"] = bname
                    self._nodes[successor]["tag_name"] = name
                    self._nodes[successor]["tag_prob"] = prob
                    self._nodes[successor]["tag_value"] = value

    # -------------------------------------------------------------------------
    #
    #
    #  T R E E    S T R U C T U R E    D I S P L A Y
    #
    #
    def __repr__(self):
        #
        # Shows the tree structure
        #
        def adjust_width(column: list[str]) -> list:
            maxwidth: int = max([len(txtline) for txtline in column]) + 2
            formatstr: str = "{:<" + str(maxwidth) + "s}"
            column: list = [formatstr.format(txtline) for txtline in column]
            return column

        def structure_colum() -> list:

            column: list = ["STRUCTURE", ""]
            for i_node, node in enumerate(self._nodes):
                type_: str = node["type"]
                code: str = (
                    "D" if type_ == "DECISION" else "C" if type_ == "CHANCE" else "T"
                )
                successors: list = node.get("successors")
                txtline: str = "{}{}".format(i_node, code)
                if successors is not None:
                    successors = [str(successor) for successor in successors]
                    txtline += " ".join(successors)
                column.append(txtline)
            return column

        def names_column() -> list:
            column: list = ["NAMES", ""] + [node["name"] for node in self._nodes]
            return column

        def outcomes_column() -> list:
            column: list = []
            for node in self._nodes:
                successors = node.get("successors")
                if successors is not None:
                    outcomes = [
                        self._nodes[successor].get("tag_value")
                        for successor in successors
                    ]
                else:
                    outcomes = []
                column.append(outcomes)

            maxwidth: int = max(
                [len(str(txt)) for txtline in column for txt in txtline]
            )
            formatstr: str = "{:<" + str(maxwidth) + "s}"
            column = [
                [formatstr.format(str(txt)) for txt in txtline] for txtline in column
            ]
            column: list = [" ".join(txtline) for txtline in column]
            maxwidth: int = max([len(txtline) for txtline in column])
            formatstr: str = "{:<" + str(maxwidth) + "s}"
            column = [
                formatstr.format("OUTCOMES"),
                formatstr.format(""),
            ] + column
            return column

        def probabilities_column() -> list:
            column: list = []
            for node in self._nodes:
                type_: str = node["type"]
                if type_ == "CHANCE":
                    successors = node.get("successors")
                    probabilities = [
                        self._nodes[successor].get("tag_prob")
                        for successor in successors
                    ]
                else:
                    probabilities = []
                column.append(probabilities)

            maxwidth: int = max(
                [len(str(txt)) for txtline in column for txt in txtline]
            )
            formatstr: str = "{:<" + str(maxwidth) + "s}"
            column = [
                [
                    formatstr.format("{:.3f}".format(prob))[1:]
                    if prob < 1.0
                    else "1.00"
                    for prob in txtline
                ]
                for txtline in column
            ]
            column: list = [" ".join(txtline) for txtline in column]
            maxwidth: int = max([len(txtline) for txtline in column])
            formatstr: str = "{:<" + str(maxwidth) + "s}"
            column = [
                formatstr.format("PROBABILIES"),
                formatstr.format(""),
            ] + column
            return column

        structure: list = adjust_width(structure_colum())
        names: list = adjust_width(names_column())
        outcomes: list = adjust_width(outcomes_column())
        probabilities: list = adjust_width(probabilities_column())

        lines = [
            struct + name + outcom + prob
            for struct, name, outcom, prob in zip(
                structure, names, outcomes, probabilities
            )
        ]

        maxlen = max([len(txt) for txt in lines])
        lines[1] = "-" * maxlen

        return "\n".join(lines)

    # -------------------------------------------------------------------------
    #
    #
    #  D E P E N D E N T    P R O B A B I L I T I E S
    #
    #
    def set_dependent_probabilities(
        self, variable: str, depends_on: Any, probabilities: dict
    ) -> None:
        """Set probability values in a chance node dependent on previous nodes.

        :param variable:

        :param depends_on:

        :param probabilities:


        """

        def dispatch(idx: int, args: dict) -> None:

            args = args.copy()

            if "tag_name" in self._nodes[idx].keys():
                tag_name = self._nodes[idx]["tag_name"]
                tag_value = self._nodes[idx]["tag_value"]
                args = {**args, **{tag_name: tag_value}}

            name = self._nodes[idx].get("name")
            if name == variable:

                if isinstance(depends_on, list):
                    key = tuple(args[term] for term in depends_on)
                else:
                    key = args[depends_on]

                probs = probabilities[key]

                for i_successor, successor in enumerate(self._nodes[idx]["successors"]):

                    self._nodes[successor]["tag_prob"] = probs[i_successor]

            if "successors" in self._nodes[idx].keys():
                for successor in self._nodes[idx]["successors"]:
                    dispatch(idx=successor, args=args)

        dispatch(idx=0, args={})

    # -------------------------------------------------------------------------
    #
    #
    #  D E P E N D E N T    O U T C O M E S
    #
    #
    def set_dependent_outcomes(
        self, variable: str, depends_on: Any, outcomes: dict
    ) -> None:
        """Set outcomes in a node dependent on previous nodes"""

        def dispatch(idx: int, args: dict) -> None:

            args = args.copy()

            if "tag_name" in self._nodes[idx].keys():
                tag_name = self._nodes[idx]["tag_name"]
                tag_value = self._nodes[idx]["tag_value"]
                args = {**args, **{tag_name: tag_value}}

            name = self._nodes[idx].get("name")
            if name == variable:

                if isinstance(depends_on, (list, tuple)):
                    key = tuple(args[term] for term in depends_on)
                else:
                    key = args[depends_on]

                outcome = outcomes[key]

                for i_successor, successor in enumerate(self._nodes[idx]["successors"]):
                    self._nodes[successor]["tag_value"] = outcome[i_successor]

            if "successors" in self._nodes[idx].keys():
                for successor in self._nodes[idx]["successors"]:
                    dispatch(idx=successor, args=args)

        dispatch(idx=0, args={})

    # -------------------------------------------------------------------------
    #
    #  V I E W    N O D E S
    #
    #
    def nodes(self) -> None:
        """Prints the internal structure of the tree as a list of nodes."""
        text = {}
        for i_node, node in enumerate(self._nodes):
            text[i_node] = node
        print(json.dumps(text, indent=4))

    ##
    ##
    ##
    ##   R E F A C T O R I N G !
    ##
    ##
    ##

    #
    # Auxiliary functions
    #
    def set_display(self, option: str) -> None:
        if option not in ["ev", "eu", "ce"]:
            raise ValueError(
                'Value {} not is a valid option ("ev", "eu", "ce")'.format(option)
            )
        self._display = option

    def _set_utitity_fn(self, utility, risk_tolerance) -> None:

        if utility is not None:
            self._use_utility_fn = True
            self._util_fn, self._inv_fn = {
                "exp": _exp_utility_fn(risk_tolerance),
                "log": _log_utility_fn(risk_tolerance),
            }[utility]
        else:
            self._util_fn = _dummy_fn
            self._inv_fn = _dummy_fn
            self._use_utility_fn = False

    def _build_call_kwargs(self) -> None:
        #
        # Builts kwargs for user function in terminal nodes
        #
        def set_fn_args(idx: int, args: dict) -> None:

            args = args.copy()

            if "tag_name" in self._nodes[idx].keys():
                name = self._nodes[idx]["tag_name"]
                value = self._nodes[idx]["tag_value"]
                args = {**args, **{name: value}}

            type_ = self._nodes[idx].get("type")

            if type_ == "TERMINAL":
                self._nodes[idx]["user_args"] = args
            else:
                if "successors" in self._nodes[idx].keys():
                    for successor in self._nodes[idx]["successors"]:
                        set_fn_args(idx=successor, args=args)

        set_fn_args(idx=0, args={})

    # -------------------------------------------------------------------------
    #
    #  E V A L U A T I O N
    #
    #
    def evaluate(self) -> None:
        """Calculates the values at the end of the tree (terminal nodes)."""

        def cumulative(**kwargs):
            return sum(v for _, v in kwargs.items())

        for node in self._nodes:

            user_args = node.get("user_args")

            if user_args:
                #
                name = node.get("name")
                user_fn = self._variables[name].get("user_fn")
                if user_fn is None:
                    user_fn = cumulative
                expval = user_fn(**user_args)
                #
                node["ExpVal"] = expval
                node["ExpUtl"] = self._util_fn(expval)
                node["CE"] = expval

        self._is_evaluated = True

    # -------------------------------------------------------------------------
    #
    #  R O L L B A C K
    #
    #
    def rollback(self) -> float:
        """Computes the preferred decision by calculating the expected
        values at each internal node, and returns the expected value of the
        preferred decision.


        Computation begins at the terminal nodes towards the root node. In each
        chance node, the expected values are calculated as the sum of
        probabilities in each branch  multiplied by the expected value in
        the corresponding node. For decision nodes, the expected value is
        the maximum (or minimum) value of its branches.

        """

        self._compute_expval()
        self._compute_optimal_strategy()
        self._with_rollback = True
        return self._nodes[0]["ExpVal"]

    #
    # Auxiliary functions
    #
    def _compute_expval(self) -> None:
        #
        # Computes the expected values at intemediate nodes.
        #
        def decision_node(idx: int) -> None:

            max_: bool = self._nodes[idx].get("max")
            successors: list = self._nodes[idx].get("successors")
            forced: int = self._nodes[idx].get("forced")

            expected_val: float = None
            expected_utl: float = None
            expected_ceq: float = None

            optimal_successor: int = None

            for i_succesor, successor in enumerate(successors):

                dispatch(idx=successor)

                expval = self._nodes[successor].get("ExpVal")
                exputl = self._nodes[successor].get("ExpUtl")
                cequiv = self._nodes[successor].get("CE")

                expected_val = expval if expected_val is None else expected_val
                expected_utl = exputl if expected_utl is None else expected_utl
                expected_ceq = cequiv if expected_ceq is None else expected_ceq

                optimal_successor = (
                    successor if optimal_successor is None else optimal_successor
                )

                if forced is None and max_ is True and exputl > expected_utl:
                    expected_val = expval
                    expected_utl = exputl
                    expected_ceq = cequiv
                    optimal_successor = successor

                if forced is None and max_ is False and exputl < expected_utl:
                    expected_val = expval
                    expected_utl = exputl
                    expected_ceq = cequiv
                    optimal_successor = successor

                if forced is not None and i_succesor == forced:
                    expected_val = expval
                    expected_utl = exputl
                    expected_ceq = cequiv
                    optimal_successor = successor

            self._nodes[idx]["ExpVal"] = expected_val
            self._nodes[idx]["ExpUtl"] = expected_utl
            self._nodes[idx]["CE"] = expected_ceq
            self._nodes[idx]["optimal_successor"] = optimal_successor

        def chance_node(idx: int) -> None:

            successors: list = self._nodes[idx].get("successors")
            forced: int = self._nodes[idx].get("forced")
            expected_val: float = 0
            expected_utl: float = 0

            for i_successor, successor in enumerate(successors):
                dispatch(idx=successor)
                if forced is None:
                    prob: float = self._nodes[successor].get("tag_prob")
                    expval: float = self._nodes[successor].get("ExpVal")
                    exputl: float = self._nodes[successor].get("ExpUtl")
                    expected_val += prob * expval
                    expected_utl += prob * exputl
                else:
                    if i_successor == forced:
                        prob: float = self._nodes[successor].get("tag_prob")
                        expval: float = self._nodes[successor].get("ExpVal")
                        exputl: float = self._nodes[successor].get("ExpUtl")
                        expected_val = expval
                        expected_utl = exputl

            self._nodes[idx]["ExpVal"] = expected_val
            self._nodes[idx]["ExpUtl"] = expected_utl
            self._nodes[idx]["CE"] = self._inv_fn(expected_utl)

        def dispatch(idx: int) -> None:
            #
            # In this point, expected values in terminal nodes are already
            # computed.
            #
            type_: str = self._nodes[idx].get("type")
            if type_ == "DECISION":
                decision_node(idx=idx)
            if type_ == "CHANCE":
                chance_node(idx=idx)

        dispatch(idx=0)

    def _compute_optimal_strategy(self) -> None:
        #
        def terminal_node(idx: int, optimal_strategy: bool) -> None:
            self._nodes[idx]["optimal_strategy"] = optimal_strategy

        def chance_node(idx: int, optimal_strategy: bool) -> None:
            self._nodes[idx]["optimal_strategy"] = optimal_strategy
            successors = self._nodes[idx].get("successors")
            for successor in successors:
                dispatch(idx=successor, optimal_strategy=optimal_strategy)

        def decision_node(idx: int, optimal_strategy: bool) -> None:
            self._nodes[idx]["optimal_strategy"] = optimal_strategy
            successors = self._nodes[idx].get("successors")
            optimal_successor = self._nodes[idx].get("optimal_successor")
            for successor in successors:
                if successor == optimal_successor:
                    dispatch(idx=successor, optimal_strategy=optimal_strategy)
                else:
                    dispatch(idx=successor, optimal_strategy=False)

        def dispatch(idx: int, optimal_strategy: bool) -> None:
            type_: str = self._nodes[idx].get("type")
            if type_ == "TERMINAL":
                terminal_node(idx=idx, optimal_strategy=optimal_strategy)
            if type_ == "DECISION":
                decision_node(idx=idx, optimal_strategy=optimal_strategy)
            if type_ == "CHANCE":
                chance_node(idx=idx, optimal_strategy=optimal_strategy)

        dispatch(idx=0, optimal_strategy=True)

    # -------------------------------------------------------------------------
    #
    #
    #  D I S P L A Y
    #
    #
    def display(
        self,
        idx: int = 0,
        max_deep: int = None,
        policy_suggestion: bool = False,
    ) -> None:
        """Exports the tree as text diagram.

        :param idx:
            Id number of the root of the tree to be exported. When it is zero, the
            entire tree is exported.

        :param max_deep:
            Controls the maximum deep of the nodes in the tree exported as text.

        :param policy_suggestion:
            When `True` exports only the subtree showing the nodes and branches
            relevants to the optimal decision (optimal strategy).


        """

        def display_node(idx, is_last_node, is_optimal_choice, deep, max_deep):
            #
            def prepare_text():

                tag_prob = self._nodes[idx].get("tag_prob")
                tag_value = self._nodes[idx].get("tag_value")
                expval = self._nodes[idx].get("ExpVal")
                exputl = self._nodes[idx].get("ExpUtl")
                cequiv = self._nodes[idx].get("CE")

                text = " "
                if tag_prob is not None:
                    text += "{:.3f} ".format(tag_prob)[1:]
                if tag_value is not None:
                    text += "{:8.2f} ".format(tag_value)
                if self._use_utility_fn is False or self._display == "ev":
                    if expval is not None:
                        text += "{:8.2f} ".format(expval)
                else:
                    if exputl is not None and self._display == "eu":
                        text += "{:8.2f} ".format(exputl)
                    if cequiv is not None and self._display == "ce":
                        text += "{:8.2f} ".format(cequiv)

                return text

            # ---------------------------------------------------------------------------
            type_ = self._nodes[idx]["type"]
            tag_name = self._nodes[idx].get("tag_name")

            # ---------------------------------------------------------------------------
            # vertical bar in the last node of terminals
            if type_ == "TERMINAL":
                vbar = "\\" if is_last_node is True else "|"
            else:
                vbar = "|"
            branch_text = vbar + prepare_text()

            # ---------------------------------------------------------------------------
            # mark optimal choice
            if is_optimal_choice is True:
                branch_text = ">" + branch_text[1:]

            # ---------------------------------------------------------------------------
            # line between --------[?] and childrens
            if type_ == "TERMINAL":
                text = []
            else:
                if tag_name is not None:
                    text = ["| {}".format(tag_name)]
                else:
                    text = ["|"]

            # ---------------------------------------------------------------------------
            # values on the branch
            text.append(branch_text)

            # ---------------------------------------------------------------------------
            # Node -----------[?]
            letter = "D" if type_ == "DECISION" else "C" if type_ == "CHANCE" else "T"
            len_branch_text = max(7, len(branch_text))
            if type_ != "TERMINAL":
                if is_last_node is True:
                    branch = "\\" + "-" * (len_branch_text - 4) + "[{}]".format(letter)
                else:
                    branch = "+" + "-" * (len_branch_text - 4) + "[{}]".format(letter)
                text.append(branch)

            # ---------------------------------------------------------------------------
            # successors
            successors = self._nodes[idx].get("successors")

            # ---------------------------------------------------------------------------
            # max deep
            deep += 1

            if successors is not None and (
                max_deep is None or (max_deep is not None and deep <= max_deep)
            ):
                for successor in successors:

                    # -------------------------------------------------------------------
                    # Mark optimal strategy
                    optimal_strategy = self._nodes[successor].get("optimal_strategy")
                    is_optimal_choice = type_ == "DECISION" and optimal_strategy is True

                    # -------------------------------------------------------------------
                    # policy suggestion
                    if optimal_strategy is False and policy_suggestion is True:
                        continue

                    # -------------------------------------------------------------------
                    # vbar following the line of preious node
                    if policy_suggestion is False:
                        is_last_child_node = successor == successors[-1]
                    else:
                        if type_ == "DECISION":
                            is_last_child_node = True
                        else:
                            is_last_child_node = successor == successors[-1]

                    text_ = display_node(
                        successor, is_last_child_node, is_optimal_choice, deep, max_deep
                    )

                    vbar = " " if is_last_node else "|"

                    # ---------------------------------------------------------------------------
                    # indents the childrens
                    text_ = [
                        vbar + " " * (len_branch_text - 3) + line for line in text_
                    ]

                    # ---------------------------------------------------------------------------
                    # Adds a vertical bar as first element of a terminal node sequence
                    successor_type = self._nodes[successor]["type"]
                    if successor_type == "TERMINAL" and successor == successors[0]:
                        successor_tag_name = self._nodes[successor].get("tag_name")
                        if successor_tag_name is not None:
                            text.extend(
                                [
                                    vbar
                                    + " " * (len_branch_text - 3)
                                    + "| {}".format(successor_tag_name)
                                ]
                            )
                        else:
                            text.extend([vbar + " " * (len_branch_text - 3) + "|"])

                    text.extend(text_)

            return text

        if self._with_rollback is False:
            policy_suggestion = False

        text = display_node(
            idx=idx,
            is_last_node=True,
            is_optimal_choice=False,
            deep=0,
            max_deep=max_deep,
        )

        print("\n".join(text))

    # -------------------------------------------------------------------------
    #
    #  R I S K    P R O F I L E
    #
    #
    def risk_profile(self, idx: int, cumulative: bool, single: bool) -> None:
        """Plots a probability distribution of the tree results computed in a designed node.

        :param idx:

        :param cumulative:

        :param single:


        """
        self._compute_risk_profiles(idx=idx)
        self._plot_risk_profile(idx=idx, cumulative=cumulative, single=single)

    #
    # Auxiliary functions
    #
    def _compute_risk_profiles(self, idx: int) -> None:
        #
        def terminal(idx: int) -> None:
            value: float = self._nodes[idx].get("ExpVal")
            self._nodes[idx]["RiskProfile"] = {value: 1.0}

        def chance(idx: int) -> None:
            successors = self._nodes[idx].get("successors")
            for successor in successors:
                dispatch(idx=successor)
            self._nodes[idx]["RiskProfile"] = {}
            for successor in successors:
                prob = self._nodes[successor].get("tag_prob")

                for value_successor, prob_successor in self._nodes[successor][
                    "RiskProfile"
                ].items():
                    if value_successor in self._nodes[idx]["RiskProfile"].keys():
                        self._nodes[idx]["RiskProfile"][value_successor] += (
                            prob * prob_successor
                        )
                    else:
                        self._nodes[idx]["RiskProfile"][value_successor] = (
                            prob * prob_successor
                        )

        def decision(idx: int) -> None:
            successors = self._nodes[idx].get("successors")
            for successor in successors:
                dispatch(idx=successor)
            optimal_successor = self._nodes[idx].get("optimal_successor")
            self._nodes[idx]["RiskProfile"] = self._nodes[optimal_successor][
                "RiskProfile"
            ]

        def dispatch(idx: int) -> None:
            type_ = self._nodes[idx].get("type")
            if type_ == "TERMINAL":
                terminal(idx=idx)
            if type_ == "CHANCE":
                chance(idx=idx)
            if type_ == "DECISION":
                decision(idx=idx)

        dispatch(idx=idx)

    #
    # Plots
    #
    def _plot_risk_profile(self, idx: int, cumulative: bool, single: bool) -> None:
        #
        def plot_stem_single(idx: int, linefmt: str = "-k", color: str = "black"):

            risk_profile = self._nodes[idx].get("RiskProfile").copy()
            values = sorted(risk_profile.keys())
            probs = [risk_profile[value] for value in values]

            expval = self._nodes[idx].get("ExpVal")
            tag_value = self._nodes[idx].get("tag_value")
            if tag_value is not None:
                label = "{};EV={}".format(tag_value, expval)
            else:
                label = "EV={}".format(expval)

            markerline, _, _ = plt.gca().stem(
                values, probs, linefmt=linefmt, basefmt="gray", label=label
            )

            markerline.set_markerfacecolor(color)
            markerline.set_markeredgecolor(color)

            plt.gca().spines["bottom"].set_visible(False)
            plt.gca().spines["left"].set_visible(False)
            plt.gca().spines["right"].set_visible(False)
            plt.gca().spines["top"].set_visible(False)

            plt.gca().set_xlabel("Expected values")
            plt.gca().set_ylabel("Probability")
            plt.gca().legend()

        def plot_step_single(idx: int, linefmt: str = "-k") -> None:

            risk_profile = self._nodes[idx].get("RiskProfile").copy()
            values = sorted(risk_profile.keys())
            probs = [risk_profile[value] for value in values]

            cumprobs = [0] + np.cumsum(probs).tolist()
            values = values + [values[-1]]

            expval = self._nodes[idx].get("ExpVal")
            tag_value = self._nodes[idx].get("tag_value")
            if tag_value is not None:
                label = "{};EV={}".format(tag_value, expval)
            else:
                label = "EV={}".format(expval)

            plt.gca().step(values, cumprobs, linefmt, label=label)

            plt.gca().spines["bottom"].set_visible(False)
            plt.gca().spines["left"].set_visible(False)
            plt.gca().spines["right"].set_visible(False)
            plt.gca().spines["top"].set_visible(False)

            plt.gca().set_xlabel("Expected values")
            plt.gca().set_ylabel("Cumulative probability")
            plt.gca().legend()

        def plot_stem_multiple(idx: int) -> None:

            successors = self._nodes[idx].get("successors")
            for i_successor, successor in enumerate(successors):
                plot_stem_single(successor, linefmts[i_successor], colors[i_successor])

        def plot_step_multiple(idx: int) -> None:

            successors = self._nodes[idx].get("successors")
            for i_successor, successor in enumerate(successors):
                plot_step_single(successor, linefmts[i_successor])

        linefmts = [
            "-k",
            "-b",
            "-r",
            "-g",
            "--k",
            "--b",
            "--r",
            "--g",
            "-.k",
            "-.b",
            "-.r",
            "-.g",
        ]
        colors = ["black", "blue", "red", "green"] * 3

        if cumulative is False and single is True:
            plot_stem_single(idx)
        if cumulative is True and single is True:
            plot_step_single(idx)
        if cumulative is False and single is False:
            plot_stem_multiple(idx)
        if cumulative is True and single is False:
            plot_step_multiple(idx)

    # -------------------------------------------------------------------------
    #
    #  P R O B A B I L I S T I  C     S E N S I T I V I T Y
    #
    #
    def probabilistic_sensitivity(self, varname: str) -> None:
        """Display a probabilistic sensitivity plot for a chance node.

        :param varname:
            Name of the probabilistic variable.

        """

        def probabilistic_sensitivity_chance() -> None:

            top_branch, bottom_branch = self._variables.get_top_bottom_branches(varname)
            self._variables.set_probabitlities_to_zero(varname)

            results = []
            probabilities = np.linspace(start=0, stop=1, num=21).tolist()
            for top_probability in probabilities:

                branch = self._variables[varname]["branches"][top_branch]
                self._variables[varname]["branches"][top_branch] = (
                    1 - top_probability,
                    branch[1],
                    branch[2],
                )

                branch = self._variables[varname]["branches"][bottom_branch]
                self._variables[varname]["branches"][bottom_branch] = (
                    top_probability,
                    branch[1],
                    branch[2],
                )

                self._build_skeleton()
                self._set_tag_attributes()
                self._build_call_kwargs()
                self.evaluate()
                self.rollback()
                results.append(self._nodes[0].get("ExpVal"))

            plt.gca().plot(probabilities, results, "-k")
            plt.gca().spines["bottom"].set_visible(False)
            plt.gca().spines["left"].set_visible(False)
            plt.gca().spines["right"].set_visible(False)
            plt.gca().spines["top"].set_visible(False)
            plt.gca().set_ylabel("Expected values")
            plt.gca().set_xlabel("Probability")
            plt.grid()

        def probabilistic_sensitivity_decision() -> None:

            top_branch, bottom_branch = self._variables.get_top_bottom_branches(varname)
            self._variables.set_probabitlities_to_zero(varname)

            results = {}
            successors = self._nodes[0].get("successors")
            tag_values = [
                self._nodes[successor].get("tag_value") for successor in successors
            ]
            for tag_value in tag_values:
                results[tag_value] = []

            probabilities = np.linspace(start=0, stop=1, num=21).tolist()
            for probability in probabilities:

                branch = self._variables[varname]["branches"][bottom_branch]
                self._variables[varname]["branches"][bottom_branch] = (
                    probability,
                    branch[1],
                    branch[2],
                )

                branch = self._variables[varname]["branches"][top_branch]
                self._variables[varname]["branches"][top_branch] = (
                    1.0 - probability,
                    branch[1],
                    branch[2],
                )

                self._build_skeleton()
                self._set_tag_attributes()
                self._build_call_kwargs()
                self.evaluate()
                self.rollback()
                expvals = [
                    self._nodes[successor].get("ExpVal") for successor in successors
                ]
                for expval, tag_value in zip(expvals, tag_values):
                    results[tag_value].append(expval)

            for tag_value in tag_values:
                plt.gca().plot(probabilities, results[tag_value], label=str(tag_value))

            plt.gca().spines["bottom"].set_visible(False)
            plt.gca().spines["left"].set_visible(False)
            plt.gca().spines["right"].set_visible(False)
            plt.gca().spines["top"].set_visible(False)
            plt.gca().set_ylabel("Expected values")
            plt.gca().set_xlabel("Probability")
            plt.gca().legend()
            plt.grid()

        #
        #
        #
        type_ = self._variables[varname]["type"]
        if type_ != "CHANCE":
            raise ValueError('Variable {} is {} != "CHANCE"'.format(varname, type_))

        orig_variables = self._variables.copy()
        type_root = self._nodes[0].get("type")
        if type_root == "CHANCE":
            probabilistic_sensitivity_chance()
        if type_root == "DECISION":
            probabilistic_sensitivity_decision()

        self._variables = orig_variables
        self._build_skeleton()
        self._set_tag_attributes()
        self._build_call_kwargs()
        self.evaluate()
        self.rollback()

    # -------------------------------------------------------------------------
    #
    #  R I S K    A T T I T U D E
    #
    #
    def risk_attitude_sensitivity(
        self, utilitiy_fn: str, risk_tolerance: float
    ) -> None:
        """Plots a risk tolrecance plot."""

        def _risk_attitude_decision():

            results = {}
            successors = self._nodes[0].get("successors")
            tag_values = [
                self._nodes[successor].get("tag_value") for successor in successors
            ]
            for tag_value in tag_values:
                results[tag_value] = []

            risk_aversions = np.linspace(
                start=0, stop=1.0 / risk_tolerance, num=11
            ).tolist()

            for risk_aversion in risk_aversions:

                if risk_aversion == np.float64(0):
                    self._set_utitity_fn(None, 0)
                else:
                    self._set_utitity_fn(utilitiy_fn, 1.0 / risk_aversion)

                self.evaluate()
                self.rollback()

                ceqs = [self._nodes[successor].get("CE") for successor in successors]
                for ceq, tag_value in zip(ceqs, tag_values):
                    results[tag_value].append(ceq)

            # for tag_value in tag_values:
            #    print("branch = ", tag_value, results[tag_value])
            linefmts = ["-k", "--k", ".-k", "-g", "--g", ".-g", "-r", "--r", ".-r"]
            for linefmt, tag_value in zip(linefmts, tag_values):
                plt.gca().plot(
                    risk_aversions,
                    results[tag_value],
                    linefmt,
                    label=str(tag_value),
                )

            labels = [
                "Infinity"
                if risk_aversion == np.float(0)
                else str(int(round(1 / risk_aversion, 0)))
                for risk_aversion in risk_aversions
            ]
            # plt.xticks(risk_aversions, labels, rotation="vertical")
            plt.xticks(risk_aversions, labels)

            plt.gca().spines["bottom"].set_visible(False)
            plt.gca().spines["left"].set_visible(False)
            plt.gca().spines["right"].set_visible(False)
            plt.gca().spines["top"].set_visible(False)
            plt.gca().set_ylabel("Certainty equivalent")
            plt.gca().set_xlabel("Risk tolerance")
            plt.gca().legend()
            plt.grid()

        def _risk_attitude_chance():

            results = {}
            successors = self._nodes[0].get("successors")
            tag_values = [
                self._nodes[successor].get("tag_value") for successor in successors
            ]
            for tag_value in tag_values:
                results[tag_value] = []

            risk_tolerances = np.linspace(
                start=risk_tolerance, stop=1000, num=50
            ).tolist()

            for rtol in risk_tolerances:

                self._set_utitity_fn(utilitiy_fn, rtol)
                self.evaluate()
                self.rollback()
                expvals = [
                    self._nodes[successor].get("ExpVal") for successor in successors
                ]
                for expval, tag_value in zip(expvals, tag_values):
                    results[tag_value].append(expval)

            for tag_value in tag_values:
                plt.gca().plot(
                    risk_tolerances, results[tag_value], label=str(tag_value)
                )

            plt.gca().spines["bottom"].set_visible(False)
            plt.gca().spines["left"].set_visible(False)
            plt.gca().spines["right"].set_visible(False)
            plt.gca().spines["top"].set_visible(False)
            plt.gca().set_ylabel("Expected values")
            plt.gca().set_xlabel("Risk tolerance")
            plt.gca().invert_xaxis()
            plt.gca().legend()
            plt.grid()

        orig_util_fn = self._util_fn
        orig_inv_fn = self._inv_fn
        orig_use_utitlity_fn = self._use_utility_fn

        type_ = self._nodes[0].get("type")
        if type_ == "DECISION":
            _risk_attitude_decision()
        if type_ == "CHANCE":
            _risk_attitude_chance()

        self._util_fn = orig_util_fn
        self._inv_fn = orig_inv_fn
        self._use_utility_fn = orig_use_utitlity_fn
        self.rollback()

    #
    #
    #

    #
    # Pendiente
    #
    def pendiente(self):

        self._compute_path_probabilities()

    #
    #
    #  I N T E R N A L   F U N C T I O N S
    #
    #

    # =========================================================================
    #
    # __init__()
    #
    # =========================================================================

    def export_text(
        self,
        idx: int = 0,
        risk_profile: bool = False,
        max_deep: int = None,
        policy_suggestion: bool = False,
    ) -> str:
        """Exports the tree as text diagram.

        :param idx:
            Id number of the root of the tree to be exported. When it is zero, the entire tree is exported.

        :param risk_profile:
            Includes the risk profile information on each node. The risk profile
            is the possibles results (payoffs or losses) and the associated
            probabilities for any decision strategy.

        :param max_deep:
            Controls the maximum deep of the nodes in the tree exported as text.

        :param policy_suggestion:
            When `True` exports only the subtree showing the nodes and branches
            relevants to the optimal decision (optimal strategy).



        """

        def node_type_chance(text: list, is_last_node: bool) -> list:
            text: list = text.copy()
            if is_last_node is True:
                text.append("\\-------[C]")
            else:
                text.append("+-------[C]")
            return text

        def node_type_decision(text: list, is_last_node: bool) -> list:
            text: list = text.copy()
            if is_last_node is True:
                text.append("\\-------[D]")
            else:
                text.append("+-------[D]")
            return text

        def node_type_terminal(text: list, idx: int, is_last_node: bool) -> list:
            text = text.copy()
            name = self._nodes[idx].get("name")
            if "ExpVal" in self._nodes[idx].keys():
                value = self._nodes[idx].get("ExpVal")
                if is_last_node is True:
                    text.append("\\-------[T] {}={:.2f}".format(name, value))
                else:
                    text.append("+-------[T] {}={:.2f}".format(name, value))
            else:
                if is_last_node is True:
                    text.append("\\-------[T] {}".format(name))
                else:
                    text.append("+-------[T] {}".format(name))
            return text

        def node_type(text, idx, is_last_node):
            type_ = self._nodes[idx]["type"]
            if type_ == "TERMINAL":
                text = node_type_terminal(text, idx, is_last_node)
            if type_ == "DECISION":
                text = node_type_decision(text, is_last_node)
            if type_ == "CHANCE":
                text = node_type_chance(text, is_last_node)
            return text

        def newline(text, idx, key, formatstr):
            text = text.copy()
            if key in self._nodes[idx].keys():
                value = self._nodes[idx].get(key)
                text.append(formatstr.format(value))
            return text

        def selected_strategy(text, idx):
            text = text.copy()
            if "selected_strategy" in self._nodes[idx].keys():
                if self._nodes[idx]["selected_strategy"] is True:
                    text.append("| (selected strategy)")
            return text

        def riskprofile(text: list, idx: int) -> list:
            text = text.copy()
            type_ = self._nodes[idx]["type"]
            if type_ != "TERMINAL" and "RiskProfile" in self._nodes[idx].keys():
                text.append("| Risk Profile:")
                text.append("|         Value  Prob")
                values = sorted(self._nodes[idx]["RiskProfile"].keys())
                for value in values:
                    prob = self._nodes[idx]["RiskProfile"][value]
                    text.append("| {:-13.2f} {:5.2f}".format(value, prob))
            return text

        def export_branches(
            text: list,
            idx: int,
            is_last_node: bool,
            max_deep: int,
            deep: int,
            strategy: bool,
        ) -> list:

            text = text.copy()
            if "successors" not in self._nodes[idx].keys():
                return text

            successors = self._nodes[idx]["successors"]

            type_ = self._nodes[idx]["type"]

            for successor in successors:

                next_is_last_node = successor == successors[-1]

                if "selected_strategy" in self._nodes[successor].keys():
                    selected_strategy = self._nodes[successor]["selected_strategy"]
                else:
                    selected_strategy = False

                if strategy is True and selected_strategy is False:
                    continue

                if strategy is True and type_ == "DECISION":
                    next_is_last_node = True

                result = export_node(
                    successor, next_is_last_node, max_deep, deep, strategy
                )

                for txt in result:
                    if is_last_node is True:
                        text.append(" " * 9 + txt)
                    else:
                        text.append("|" + " " * 8 + txt)

            return text

        def export_node(
            idx: int,
            is_last_node: bool,
            max_deep: int,
            deep: int,
            strategy: bool,
        ) -> list:

            if deep is None:
                deep: int = 0

            text = ["|"]
            type_ = self._nodes[idx]["type"]
            text.append("| #{}".format(idx))
            #
            if "tag_name" in self._nodes[idx].keys():
                text.append(
                    "| {}={}".format(
                        self._nodes[idx].get("tag_name"),
                        self._nodes[idx].get("tag_value"),
                    )
                )

            text = newline(text, idx, "tag_prob", "| Prob={:.2f}")
            if type_ != "TERMINAL":
                text = newline(text, idx, "ExpVal", "| ExpVal={:.2f}")
            text = newline(text, idx, "PathProb", "| PathProb={:.2f}")
            if self._use_utility_fn is True:
                text = newline(text, idx, "ExpUtl", "| ExpUtl={:.2f}")
                text = newline(text, idx, "CE", "| CE={:.2f}")

            if risk_profile is True:
                text = riskprofile(text, idx)
            text = selected_strategy(text, idx)
            text = node_type(text, idx, is_last_node)

            if max_deep is None or (max_deep is not None and deep < max_deep):
                deep += 1
                text = export_branches(
                    text, idx, is_last_node, max_deep, deep, strategy
                )
                deep -= 1

            return text

        text = export_node(
            idx=idx,
            is_last_node=True,
            max_deep=max_deep,
            deep=None,
            strategy=policy_suggestion,
        )

        return "\n".join(text)

    def _compute_path_probabilities(self) -> None:
        #
        def terminal_node(idx: int, cum_prob: float) -> None:
            prob = self._nodes[idx].get("tag_prob")
            cum_prob = cum_prob if prob is None else cum_prob * prob / 100.0
            self._nodes[idx]["PathProb"] = cum_prob

        def decision_node(idx: int, cum_prob: float) -> None:
            optimal_successor = self._nodes[idx].get("optimal_successor")
            successors = self._nodes[idx].get("successors")
            for successor in successors:
                if successor == optimal_successor:
                    dispatch(idx=successor, cum_prob=cum_prob)
                else:
                    dispatch(idx=successor, cum_prob=0.0)

        def chance_node(idx: int, cum_prob: float) -> None:

            successors = self._nodes[idx].get("successors")
            prob = self._nodes[idx].get("tag_prob")
            cum_prob = cum_prob if prob is None else cum_prob * prob / 100.0
            for successor in successors:
                dispatch(idx=successor, cum_prob=cum_prob)

        def dispatch(idx: int, cum_prob: float) -> None:

            type_: str = self._nodes[idx].get("type")

            if type_ == "TERMINAL":
                terminal_node(idx=idx, cum_prob=cum_prob)

            if type_ == "DECISION":
                decision_node(idx=idx, cum_prob=cum_prob)

            if type_ == "CHANCE":
                chance_node(idx=idx, cum_prob=cum_prob)

        dispatch(idx=0, cum_prob=100.0)

    def plot(self, max_deep: int = None, policy_suggestion: bool = False):
        """Plots the tree.

        :param max_deep: maximum deep of the tree nodes to be plotted.

        :param policy_suggestion:
            When `True`, it plots only the subtree showing the nodes and branches
            relevants to the optimal decision (optimal strategy).

        """

        width = "0.25"
        height = "0.15"
        arrowsize = "0.3"
        fontsize = "8.0"

        def terminal(idx: int, dot, max_deep: int, deep: int):
            name = self._nodes[idx].get("name")
            if "ExpVal" in self._nodes[idx].keys():
                expval = self._nodes[idx].get("ExpVal")
                pathprob = self._nodes[idx].get("PathProb")
                label = "{}={}, {}%".format(name, round(expval, 2), round(pathprob, 2))
            else:
                label = name

            dot.node(
                str(idx),
                label,
                shape="record",
                orientation="90",
                height=height,
                style="filled",
                color="powderblue",
                fontsize=fontsize,
                fontname="Courier New",
            )

            return dot

        def chance(idx: int, dot, max_deep: int, deep: int):

            dot.node(
                str(idx),
                label="#{}".format(idx),
                shape="circle",
                width=width,
                style="filled",
                color="yellowgreen",
                fontsize=fontsize,
                fontname="Courier New",
                fizedsize="shape",
            )

            if max_deep is None or (max_deep is not None and deep < max_deep):

                deep += 1

                successors = self._nodes[idx].get("successors")
                for successor in successors:
                    dot = dispatch(idx=successor, dot=dot, max_deep=max_deep, deep=deep)
                    tag_name = self._nodes[successor].get("tag_name")
                    tag_value = self._nodes[successor].get("tag_value")
                    tag_prob = self._nodes[successor].get("tag_prob")
                    type_ = self._nodes[successor].get("type")
                    selected_strategy = self._nodes[successor].get("selected_strategy")

                    if "ExpVal" in self._nodes[successor].keys():
                        expval = self._nodes[successor].get("ExpVal")

                        if type_ != "TERMINAL":
                            label = "{}={}, {}%\nExpVal={}".format(
                                tag_name,
                                tag_value,
                                round(tag_prob, 2),
                                round(expval, 2),
                            )
                        else:
                            label = "{}={}, {}%".format(
                                tag_name, tag_value, round(tag_prob, 2)
                            )

                    else:
                        label = "{}={}, {}%".format(
                            tag_name, tag_value, round(tag_prob, 2)
                        )

                    if selected_strategy is True:
                        penwidth = "2"
                    else:
                        penwidth = "1"

                    dot.edge(
                        str(idx),
                        str(successor),
                        arrowsize=arrowsize,
                        label=label,
                        fontsize=fontsize,
                        penwidth=penwidth,
                        fontname="Courier New",
                    )

                deep -= 1

            return dot

        def decision(idx: int, dot, max_deep: int, deep: int):

            dot.node(
                str(idx),
                label="#{}".format(idx),
                shape="square",
                width=width,
                style="filled",
                color="brown",
                fontsize=fontsize,
                fontname="Courier New",
                fizedsize="shape",
            )

            if max_deep is None or (max_deep is not None and deep < max_deep):

                deep += 1

                successors = self._nodes[idx].get("successors")
                for successor in successors:

                    if "selected_strategy" in self._nodes[successor].keys():
                        selected_strategy = self._nodes[successor]["selected_strategy"]
                    else:
                        selected_strategy = False

                    if policy_suggestion is True and selected_strategy is False:
                        continue

                    dot = dispatch(idx=successor, dot=dot, max_deep=max_deep, deep=deep)
                    tag_name = self._nodes[successor].get("tag_name")
                    tag_value = self._nodes[successor].get("tag_value")
                    type_ = self._nodes[successor].get("type")
                    selected_strategy = self._nodes[successor].get("selected_strategy")

                    if "ExpVal" in self._nodes[successor].keys():
                        expval = self._nodes[successor].get("ExpVal")

                        if type_ != "TERMINAL":
                            label = "{}={}, ExpVal={}".format(
                                tag_name, tag_value, round(expval, 2)
                            )
                        else:
                            label = "{}={}".format(tag_name, tag_value)
                    else:
                        label = "{}={}".format(tag_name, tag_value)

                    if selected_strategy is True:
                        penwidth = "2"
                    else:
                        penwidth = "1"

                    dot.edge(
                        str(idx),
                        str(successor),
                        arrowsize=arrowsize,
                        label=label,
                        fontsize=fontsize,
                        penwidth=penwidth,
                        fontname="Courier New",
                    )

                deep -= 1

            return dot

        def dispatch(idx: int, dot, max_deep: int, deep: int):

            type_ = self._nodes[idx].get("type")

            if type_ == "TERMINAL":
                dot = terminal(idx, dot, max_deep, deep)

            if type_ == "DECISION":
                dot = decision(idx, dot, max_deep, deep)

            if type_ == "CHANCE":
                dot = chance(idx, dot, max_deep, deep)

            return dot

        dot = Digraph()
        dot.attr(rankdir="LR")  # splines="compound"
        dot = dispatch(idx=0, dot=dot, max_deep=max_deep, deep=0)
        return dot

    @property
    def variables(self):
        """Returns the variables used to build the decision tree."""
        return self._variables

    #
    #
    #  R E F A C T O R I N G
    #
    #

    #     def print_branch(prefix, this_branch, is_node_last_branch):

    #         print(prefix + "|")

    #         type = this_branch.get("type")
    #         if "id" in this_branch.keys():
    #             print(prefix + "| #" + str(this_branch.get("id")))

    #         ## prints the name and value of the variable
    #         if "tag" in this_branch.keys():
    #             var = this_branch["tag"]
    #             if "value" in this_branch.keys():
    #                 txt = "| " + var + "=" + str(this_branch["value"])
    #             else:
    #                 txt = "| " + var
    #             print(prefix + txt)

    #         ## prints the probability
    #         if "prob" in this_branch.keys():
    #             txt = "| Prob={:1.2f}".format(this_branch["prob"])
    #             print(prefix + txt)

    #         ## prints the cumulative probability
    #         if type == "TERMINAL" and "PathProb" in this_branch.keys():
    #             txt = "| PathProb={:1.2f}".format(this_branch["PathProb"])
    #             print(prefix + txt)

    #         if "ExpVal" in this_branch.keys() and this_branch["ExpVal"] is not None:
    #             txt = "| ExpVal={:1.2f}".format(this_branch["ExpVal"])
    #             print(prefix + txt)

    #         if "ExpUtl" in this_branch.keys() and this_branch["ExpUtl"] is not None:
    #             txt = "| ExpUtl={:1.2f}".format(this_branch["ExpUtl"])
    #             print(prefix + txt)

    #         if "CE" in this_branch.keys() and this_branch["CE"] is not None:
    #             txt = "| CE={:1.2f}".format(this_branch["CE"])
    #             print(prefix + txt)

    #         if "RiskProfile" in this_branch.keys() and type != "TERMINAL":
    #             print(prefix + "| Risk Profile:")
    #             print(prefix + "|      Value  Prob")
    #             for key in sorted(this_branch["RiskProfile"]):
    #                 txt = "|   {:8.2f} {:5.2f}".format(
    #                     key, this_branch["RiskProfile"][key]
    #                 )
    #                 print(prefix + txt)

    #         if (
    #             "sel_strategy" in this_branch.keys()
    #             and this_branch["sel_strategy"] is True
    #         ):
    #             txt = "| (selected strategy)"
    #             print(prefix + txt)

    #         if (
    #             "forced_branch_idx" in this_branch.keys()
    #             and this_branch["forced_branch_idx"] is not None
    #         ):
    #             txt = "| (forced branch = {:1d})".format(
    #                 this_branch["forced_branch_idx"]
    #             )
    #             print(prefix + txt)

    #         next_branches = (
    #             this_branch["next_branches"]
    #             if "next_branches" in this_branch.keys()
    #             else None
    #         )

    #         if is_node_last_branch is True:
    #             if type == "DECISION":
    #                 txt = r"\-------[D]"
    #             if type == "CHANCE":
    #                 txt = r"\-------[C]"
    #             if type == "TERMINAL":
    #                 txt = r"\-------[T] {:s}".format(this_branch["expr"])
    #         else:
    #             if type == "DECISION":
    #                 txt = "+-------[D]"
    #             if type == "CHANCE":
    #                 txt = "+-------[C]"
    #             if type == "TERMINAL":
    #                 txt = "+-------[T] {:s}".format(this_branch["expr"])
    #         print(prefix + txt)

    #         if maxdeep is not None and self.current_deep == maxdeep:
    #             return

    #         self.current_deep += 1

    #         if next_branches is not None:

    #             if selected_strategy is True and type == "DECISION":
    #                 optbranch = this_branch["opt_branch_idx"]
    #                 if is_node_last_branch is True:
    #                     print_branch(
    #                         prefix + " " * 9,
    #                         self.tree[next_branches[optbranch]],
    #                         is_node_last_branch=True,
    #                     )
    #                 else:
    #                     print_branch(
    #                         prefix + "|" + " " * 8,
    #                         self.tree[next_branches[optbranch]],
    #                         is_node_last_branch=True,
    #                     )
    #             else:
    #                 for next_branch_idx, next_branch_id in enumerate(next_branches):
    #                     is_last_tree_branch = (
    #                         True if next_branch_idx == len(next_branches) - 1 else False
    #                     )
    #                     if is_node_last_branch is True:
    #                         print_branch(
    #                             prefix + " " * 9,
    #                             self.tree[next_branch_id],
    #                             is_node_last_branch=is_last_tree_branch,
    #                         )
    #                     else:
    #                         print_branch(
    #                             prefix + "|" + " " * 8,
    #                             self.tree[next_branch_id],
    #                             is_node_last_branch=is_last_tree_branch,
    #                         )

    #         self.current_deep -= 1

    #     self.current_deep = 0
    #     print_branch(prefix="", this_branch=self.tree[0], is_node_last_branch=True)

    # def display_tree_as_text(self, maxdeep=None, selected_strategy=False):
    #     r"""Prints the tree as a text diagram.

    #     Args:
    #         maxdeep (int, None): maximum deep of tree to print.
    #         selected_strategy (bool): When it is `True`, only the
    #             optimal (or forced branches) in the tree are displayed.

    #     Returns:
    #         None.

    #     The following example creates a decision tree with a unique decision
    #     node at the root of the tree. When the tree has not been evaluated,
    #     this function shows only the number of the branch and the name and
    #     value of the variable representing the type of node.

    #     >>> tree = DecisionTree()
    #     >>> tree.decision_node(name='DecisionNode',
    #     ...                    branches=[(100,  1),
    #     ...                              (200,  1),
    #     ...                              (300,  1),
    #     ...                              (400,  1)],
    #     ...                    max=True)
    #     >>> tree.terminal_node()
    #     >>> tree.build_tree()
    #     >>> tree.display_tree()  # doctest: +NORMALIZE_WHITESPACE
    #     |
    #     | #0
    #     \-------[D]
    #              |
    #              | #1
    #              | DecisionNode=100
    #              +-------[T] DecisionNode
    #              |
    #              | #2
    #              | DecisionNode=200
    #              +-------[T] DecisionNode
    #              |
    #              | #3
    #              | DecisionNode=300
    #              +-------[T] DecisionNode
    #              |
    #              | #4
    #              | DecisionNode=400
    #              \-------[T] DecisionNode

    #     When the tree is evaluated, additional information is displayed for
    #     each branch. `PathProb` is the path probability for the corresponding
    #     branch of the tree. `ExpVal` is the expected value of the node.
    #     `(selected strategy)` indicates the branches corresponding to the
    #     optimal (or forced) decision strategy.

    #     >>> tree.evaluate()
    #     >>> tree.display_tree()  # doctest: +NORMALIZE_WHITESPACE
    #     |
    #     | #0
    #     | ExpVal=400.00
    #     | (selected strategy)
    #     \-------[D]
    #              |
    #              | #1
    #              | DecisionNode=100
    #              | PathProb=0.00
    #              | ExpVal=100.00
    #              +-------[T] DecisionNode
    #              |
    #              | #2
    #              | DecisionNode=200
    #              | PathProb=0.00
    #              | ExpVal=200.00
    #              +-------[T] DecisionNode
    #              |
    #              | #3
    #              | DecisionNode=300
    #              | PathProb=0.00
    #              | ExpVal=300.00
    #              +-------[T] DecisionNode
    #              |
    #              | #4
    #              | DecisionNode=400
    #              | PathProb=100.00
    #              | ExpVal=400.00
    #              | (selected strategy)
    #              \-------[T] DecisionNode

    #     The parameter `selected_strategy` are used to print the branches of
    #     tree in the optimal decision strategy. This option allows the user
    #     to analyze the sequence of optimal decisions.

    #     >>> tree.display_tree(selected_strategy=True)  # doctest: +NORMALIZE_WHITESPACE
    #     |
    #     | #0
    #     | ExpVal=400.00
    #     | (selected strategy)
    #     \-------[D]
    #              |
    #              | #4
    #              | DecisionNode=400
    #              | PathProb=100.00
    #              | ExpVal=400.00
    #              | (selected strategy)
    #              \-------[T] DecisionNode
    #     """

    #     def print_branch(prefix, this_branch, is_node_last_branch):

    #         print(prefix + "|")

    #         type = this_branch.get("type")
    #         if "id" in this_branch.keys():
    #             print(prefix + "| #" + str(this_branch.get("id")))

    #         ## prints the name and value of the variable
    #         if "tag" in this_branch.keys():
    #             var = this_branch["tag"]
    #             if "value" in this_branch.keys():
    #                 txt = "| " + var + "=" + str(this_branch["value"])
    #             else:
    #                 txt = "| " + var
    #             print(prefix + txt)

    #         ## prints the probability
    #         if "prob" in this_branch.keys():
    #             txt = "| Prob={:1.2f}".format(this_branch["prob"])
    #             print(prefix + txt)

    #         ## prints the cumulative probability
    #         if type == "TERMINAL" and "PathProb" in this_branch.keys():
    #             txt = "| PathProb={:1.2f}".format(this_branch["PathProb"])
    #             print(prefix + txt)

    #         if "ExpVal" in this_branch.keys() and this_branch["ExpVal"] is not None:
    #             txt = "| ExpVal={:1.2f}".format(this_branch["ExpVal"])
    #             print(prefix + txt)

    #         if "ExpUtl" in this_branch.keys() and this_branch["ExpUtl"] is not None:
    #             txt = "| ExpUtl={:1.2f}".format(this_branch["ExpUtl"])
    #             print(prefix + txt)

    #         if "CE" in this_branch.keys() and this_branch["CE"] is not None:
    #             txt = "| CE={:1.2f}".format(this_branch["CE"])
    #             print(prefix + txt)

    #         if "RiskProfile" in this_branch.keys() and type != "TERMINAL":
    #             print(prefix + "| Risk Profile:")
    #             print(prefix + "|      Value  Prob")
    #             for key in sorted(this_branch["RiskProfile"]):
    #                 txt = "|   {:8.2f} {:5.2f}".format(
    #                     key, this_branch["RiskProfile"][key]
    #                 )
    #                 print(prefix + txt)

    #         if (
    #             "sel_strategy" in this_branch.keys()
    #             and this_branch["sel_strategy"] is True
    #         ):
    #             txt = "| (selected strategy)"
    #             print(prefix + txt)

    #         if (
    #             "forced_branch_idx" in this_branch.keys()
    #             and this_branch["forced_branch_idx"] is not None
    #         ):
    #             txt = "| (forced branch = {:1d})".format(
    #                 this_branch["forced_branch_idx"]
    #             )
    #             print(prefix + txt)

    #         next_branches = (
    #             this_branch["next_branches"]
    #             if "next_branches" in this_branch.keys()
    #             else None
    #         )

    #         if is_node_last_branch is True:
    #             if type == "DECISION":
    #                 txt = r"\-------[D]"
    #             if type == "CHANCE":
    #                 txt = r"\-------[C]"
    #             if type == "TERMINAL":
    #                 txt = r"\-------[T] {:s}".format(this_branch["expr"])
    #         else:
    #             if type == "DECISION":
    #                 txt = "+-------[D]"
    #             if type == "CHANCE":
    #                 txt = "+-------[C]"
    #             if type == "TERMINAL":
    #                 txt = "+-------[T] {:s}".format(this_branch["expr"])
    #         print(prefix + txt)

    #         if maxdeep is not None and self.current_deep == maxdeep:
    #             return

    #         self.current_deep += 1

    #         if next_branches is not None:

    #             if selected_strategy is True and type == "DECISION":
    #                 optbranch = this_branch["opt_branch_idx"]
    #                 if is_node_last_branch is True:
    #                     print_branch(
    #                         prefix + " " * 9,
    #                         self.tree[next_branches[optbranch]],
    #                         is_node_last_branch=True,
    #                     )
    #                 else:
    #                     print_branch(
    #                         prefix + "|" + " " * 8,
    #                         self.tree[next_branches[optbranch]],
    #                         is_node_last_branch=True,
    #                     )
    #             else:
    #                 for next_branch_idx, next_branch_id in enumerate(next_branches):
    #                     is_last_tree_branch = (
    #                         True if next_branch_idx == len(next_branches) - 1 else False
    #                     )
    #                     if is_node_last_branch is True:
    #                         print_branch(
    #                             prefix + " " * 9,
    #                             self.tree[next_branch_id],
    #                             is_node_last_branch=is_last_tree_branch,
    #                         )
    #                     else:
    #                         print_branch(
    #                             prefix + "|" + " " * 8,
    #                             self.tree[next_branch_id],
    #                             is_node_last_branch=is_last_tree_branch,
    #                         )

    #         self.current_deep -= 1

    #     self.current_deep = 0
    #     print_branch(prefix="", this_branch=self.tree[0], is_node_last_branch=True)


if __name__ == "__main__":

    import doctest

    doctest.testmod()
