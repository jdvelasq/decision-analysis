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
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from graphviz import Digraph


def _exp_utility_fn(param: float):
    def util_fn(value: float) -> float:
        return 1.0 - np.exp(-value / param)

    def inv_fn(value: float) -> float:
        return -1.0 * param * np.log(1 - value)

    return util_fn, inv_fn


def _log_utility_fn(param: float):
    def util_fn(value: float) -> float:
        return np.log(value + param)

    def inv_fn(value: float):
        return np.exp(value) - param

    return util_fn, inv_fn


def _sqrt_utility_fn(param: float):
    def util_fn(value: float) -> float:
        return np.sqrt(value + param)

    def inv_fn(value: float):
        return np.power(value, 2) - param

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

        * `sqrt`: Squared-root utility function `U(x) = + sqrt(x + param)`.

    :param param:
        Value of the parameter `param` in the utility function.

    """

    def __init__(
        self,
        variables: list,
        initial_variable: str,
        utility: str = None,
        param: float = 0,
    ) -> None:

        self.nodes = None
        self._variables = variables.copy()
        self.initial_variable = initial_variable
        self._use_utility_fn = True

        if utility is None:
            util_fn = _dummy_fn
            inv_fn = _dummy_fn
            self._use_utility_fn = False
        if utility == "exp":
            util_fn, inv_fn = _exp_utility_fn(param)
        if utility == "log":
            util_fn, inv_fn = _log_utility_fn(param)
        if utility == "sqrt":
            util_fn, inv_fn = _sqrt_utility_fn(param)
        self._util_fn = util_fn
        self._inv_fn = inv_fn

        self._build_skeleton()
        self._set_tag_attributes()

    def _build_skeleton(self) -> None:
        #
        # Builds a structure where nodes are:
        #
        #   [
        #       {name: ..., type: ... successors: [ ... ]}
        #   ]
        #
        def dispatch(name: str) -> int:
            idx: int = len(self.nodes)
            type_: str = self._variables[name]["type"]
            forced: int = self._variables[name]["forced_branch"]
            self.nodes.append({"name": name, "type": type_, "forced": forced})
            if "max" in self._variables[name].keys():
                self.nodes[idx]["max"] = self._variables[name]["max"]
            if "branches" in self._variables[name].keys():
                successors: list = []
                for branch in self._variables[name].get("branches"):
                    successor: int = dispatch(name=branch[-1])
                    successors.append(successor)
                self.nodes[idx]["successors"] = successors
            return idx

        #
        self.nodes: list = []
        dispatch(name=self.initial_variable)

    def _set_tag_attributes(self) -> None:
        #
        # tag_value: is the value of the branch of the predecesor node
        # tag_prob: is the probability of the branch of the predecesor (chance) node
        #
        for node in self.nodes:

            if "successors" not in node.keys():
                continue

            name: str = node.get("name")
            successors: list = node.get("successors")
            type_: str = node.get("type")
            branches: list = self._variables[name].get("branches")

            if type_ == "DECISION":
                values = [x for x, _ in branches]
                for successor, value in zip(successors, values):
                    self.nodes[successor]["tag_name"] = name
                    self.nodes[successor]["tag_value"] = value

            if type_ == "CHANCE":
                values = [x for _, x, _ in branches]
                probs = [x for x, _, _ in branches]
                for successor, value, prob in zip(successors, values, probs):
                    self.nodes[successor]["tag_name"] = name
                    self.nodes[successor]["tag_value"] = value
                    self.nodes[successor]["tag_prob"] = prob

    ## TODO: Deprecated
    def build(self):
        """This function is used to build the internal structure of the decision tree
        using the information of the types of variables..
        """
        self._build_skeleton()
        self._set_tag_attributes()

    def __repr__(self):
        def adjust_width(column: list[str]) -> list:

            maxwidth: int = max([len(txtline) for txtline in column]) + 2
            formatstr: str = "{:<" + str(maxwidth) + "s}"
            column: list = [formatstr.format(txtline) for txtline in column]
            return column

        def structure_colum() -> list:

            column: list = ["STRUCTURE", ""]
            for i_node, node in enumerate(self.nodes):
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
            column: list = ["NAMES", ""] + [node["name"] for node in self.nodes]
            return column

        def outcomes_column() -> list:
            column: list = []
            for node in self.nodes:
                type_: str = node["type"]
                outcomes = []
                if type_ == "DECISION":
                    name = node["name"]
                    branches = self.variables[name]["branches"]
                    outcomes = [outcome for outcome, _ in branches]
                if type_ == "CHANCE":
                    name = node["name"]
                    branches = self.variables[name]["branches"]
                    outcomes = [outcome for _, outcome, _ in branches]
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
            for node in self.nodes:
                type_: str = node["type"]
                probabilities = []
                if type_ == "CHANCE":
                    name = node["name"]
                    branches = self.variables[name]["branches"]
                    probabilities = [probability for probability, _, _ in branches]
                column.append(probabilities)

            maxwidth: int = max(
                [len(str(txt)) for txtline in column for txt in txtline]
            )
            formatstr: str = "{:<" + str(maxwidth) + "s}"
            column = [
                [
                    formatstr.format("{:.2f}".format(prob / 100.0))[1:]
                    for prob in txtline
                ]
                for txtline in column
            ]
            column: list = [" ".join(txtline) for txtline in column]
            maxwidth: int = max([len(txtline) for txtline in column])
            formatstr: str = "{:<" + str(maxwidth) + "s}"
            column = [
                formatstr.format("OUTCOMES"),
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

        return "\n".join(lines)

        # text = ["STRUCTURE       NAMES         OUTCOMES        PROBABILITIES"]
        # text.append("")
        # for i_node, node in enumerate(self.nodes):
        #     name = node["name"]
        #     type_ = node["type"]

        #     if type_ == "DECISION":
        #         code = "D"
        #         branches = self.variables[name]["branches"]
        #         outcomes = [outcome for outcome, _ in branches]
        #         successors = node.get("successors")
        #         probabilities = ""

        #         structure = "{:d}{}".format(i_node, code) + " ".join(
        #             [str(successor) for successor in successors]
        #         )
        #         outcomes = " ".join([str(round(outcome, 0)) for outcome in outcomes])

        #     if type_ == "CHANCE":
        #         code = "C"
        #         branches = self.variables[name]["branches"]
        #         probabilities = [probability for probability, _, _ in branches]
        #         successors = node.get("successors")
        #         outcomes = [outcome for _, outcome, _ in branches]
        #         probabilities = " ".join(
        #             [
        #                 "{:.2f}".format(probability / 100)[1:]
        #                 for probability in probabilities
        #             ]
        #         )
        #         outcomes = " ".join([str(round(outcome, 0)) for outcome in outcomes])

        #         structure = "{:d}{}".format(i_node, code) + " ".join(
        #             [str(successor) for successor in successors]
        #         )

        #     if type_ == "TERMINAL":
        #         code = "T"
        #         probabilities = ""
        #         outcomes = ""

        #     text.append(
        #         "{:<14s}  {:<12s}  {:<14s}  {}".format(
        #             structure, name, outcomes, probabilities
        #         )
        #     )

        # return "\n".join(text)

    def print_nodes(self) -> None:
        """Prints the internal structure of the tree as a list of nodes."""
        for i_node, node in enumerate(self.nodes):
            print("#{:<3s} {}".format(str(i_node), node))

    def risk_profile(self, idx: int = 0, cumulative: bool = False) -> tuple:
        """Returns the values and probabilities of a risk profile in the node `idx`."""
        keys = self.nodes[idx]["RiskProfile"].keys()
        values = sorted(keys)
        probabilities = [self.nodes[idx]["RiskProfile"][k] for k in keys]
        if cumulative is True:
            probabilities = np.cumsum(probabilities).tolist()
        return values, probabilities

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
            name = self.nodes[idx].get("name")
            if "ExpVal" in self.nodes[idx].keys():
                value = self.nodes[idx].get("ExpVal")
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
            type_ = self.nodes[idx]["type"]
            if type_ == "TERMINAL":
                text = node_type_terminal(text, idx, is_last_node)
            if type_ == "DECISION":
                text = node_type_decision(text, is_last_node)
            if type_ == "CHANCE":
                text = node_type_chance(text, is_last_node)
            return text

        def newline(text, idx, key, formatstr):
            text = text.copy()
            if key in self.nodes[idx].keys():
                value = self.nodes[idx].get(key)
                text.append(formatstr.format(value))
            return text

        def selected_strategy(text, idx):
            text = text.copy()
            if "selected_strategy" in self.nodes[idx].keys():
                if self.nodes[idx]["selected_strategy"] is True:
                    text.append("| (selected strategy)")
            return text

        def riskprofile(text: list, idx: int) -> list:
            text = text.copy()
            type_ = self.nodes[idx]["type"]
            if type_ != "TERMINAL" and "RiskProfile" in self.nodes[idx].keys():
                text.append("| Risk Profile:")
                text.append("|         Value  Prob")
                values = sorted(self.nodes[idx]["RiskProfile"].keys())
                for value in values:
                    prob = self.nodes[idx]["RiskProfile"][value]
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
            if "successors" not in self.nodes[idx].keys():
                return text

            successors = self.nodes[idx]["successors"]

            type_ = self.nodes[idx]["type"]

            for successor in successors:

                next_is_last_node = successor == successors[-1]

                if "selected_strategy" in self.nodes[successor].keys():
                    selected_strategy = self.nodes[successor]["selected_strategy"]
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
            type_ = self.nodes[idx]["type"]
            text.append("| #{}".format(idx))
            #
            if "tag_name" in self.nodes[idx].keys():
                text.append(
                    "| {}={}".format(
                        self.nodes[idx].get("tag_name"),
                        self.nodes[idx].get("tag_value"),
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

    def _build_call_kwargs(self) -> None:
        #
        # Builts kwargs for user function in terminal nodes
        #
        def set_fn_args(idx: int, args: dict) -> None:

            args = args.copy()

            if "tag_name" in self.nodes[idx].keys():
                name = self.nodes[idx]["tag_name"]
                value = self.nodes[idx]["tag_value"]
                args = {**args, **{name: value}}

            type_ = self.nodes[idx].get("type")

            if type_ == "TERMINAL":
                self.nodes[idx]["user_args"] = args
            else:
                if "successors" in self.nodes[idx].keys():
                    for successor in self.nodes[idx]["successors"]:
                        set_fn_args(idx=successor, args=args)

        set_fn_args(idx=0, args={})

    def _compute_expval_in_terminals_nodes(self) -> None:
        #
        def cumulative(**kwargs):
            return sum(v for _, v in kwargs.items())

        for node in self.nodes:

            user_args = node.get("user_args")

            if user_args:
                #
                name = node.get("name")
                user_fn = self._variables[name].get("user_fn")
                if user_fn is None:
                    user_fn = cumulative
                expval = user_fn(**user_args)
                node["ExpVal"] = expval
                #
                exputil = self._util_fn(expval)
                node["ExpUtl"] = exputil
                node["CE"] = expval

    def _compute_expval_in_intermediate_nodes(self):
        #
        def decision_node(idx: int) -> None:

            max_: bool = self.nodes[idx].get("max")
            successors: list = self.nodes[idx].get("successors")
            forced: int = self.nodes[idx].get("forced")

            expected_val: float = None
            expected_utl: float = None
            expected_ceq: float = None

            optimal_successor: int = None

            for i_succesor, successor in enumerate(successors):

                dispatch(idx=successor)

                expval = self.nodes[successor].get("ExpVal")
                exputl = self.nodes[successor].get("ExpUtl")
                cequiv = self.nodes[successor].get("CE")

                expected_val = expval if expected_val is None else expected_val
                expected_utl = exputl if expected_utl is None else expected_utl
                expected_ceq = cequiv if expected_ceq is None else expected_ceq

                optimal_successor = (
                    successor if optimal_successor is None else optimal_successor
                )

                if forced is None and max_ is True and cequiv > expected_ceq:
                    expected_val = expval
                    expected_utl = exputl
                    expected_ceq = cequiv
                    optimal_successor = successor

                if forced is None and max_ is False and cequiv < expected_ceq:
                    expected_val = expval
                    expected_utl = exputl
                    expected_ceq = cequiv
                    optimal_successor = successor

                if forced is not None and i_succesor == forced:
                    expected_val = expval
                    expected_utl = exputl
                    expected_ceq = cequiv
                    optimal_successor = successor

            self.nodes[idx]["ExpVal"] = expected_val
            self.nodes[idx]["ExpUtl"] = expected_utl
            self.nodes[idx]["CE"] = expected_ceq
            self.nodes[idx]["optimal_successor"] = optimal_successor

        def chance_node(idx: int) -> None:

            successors: list = self.nodes[idx].get("successors")
            forced: int = self.nodes[idx].get("forced")
            expected_val: float = 0
            expected_utl: float = 0

            for i_successor, successor in enumerate(successors):
                dispatch(idx=successor)
                if forced is None:
                    prob: float = self.nodes[successor].get("tag_prob")
                    expval: float = self.nodes[successor].get("ExpVal")
                    exputl: float = self.nodes[successor].get("ExpUtl")
                    expected_val += prob * expval / 100.0
                    expected_utl += prob * exputl / 100.0
                else:
                    if i_successor == forced:
                        prob: float = self.nodes[successor].get("tag_prob")
                        expval: float = self.nodes[successor].get("ExpVal")
                        exputl: float = self.nodes[successor].get("ExpUtl")
                        expected_val = expval
                        expected_utl = exputl

            self.nodes[idx]["ExpVal"] = expected_val
            self.nodes[idx]["ExpUtl"] = expected_utl
            self.nodes[idx]["CE"] = self._inv_fn(expected_utl)

        def dispatch(idx: int) -> None:
            #
            # In this point, expected values in terminal nodes are already
            # computed.
            #
            type_: str = self.nodes[idx].get("type")
            if type_ == "DECISION":
                decision_node(idx=idx)
            if type_ == "CHANCE":
                chance_node(idx=idx)

        dispatch(idx=0)

    def _compute_path_probabilities(self) -> None:
        #
        def terminal_node(idx: int, cum_prob: float) -> None:
            prob = self.nodes[idx].get("tag_prob")
            cum_prob = cum_prob if prob is None else cum_prob * prob / 100.0
            self.nodes[idx]["PathProb"] = cum_prob

        def decision_node(idx: int, cum_prob: float) -> None:
            optimal_successor = self.nodes[idx].get("optimal_successor")
            successors = self.nodes[idx].get("successors")
            for successor in successors:
                if successor == optimal_successor:
                    dispatch(idx=successor, cum_prob=cum_prob)
                else:
                    dispatch(idx=successor, cum_prob=0.0)

        def chance_node(idx: int, cum_prob: float) -> None:

            successors = self.nodes[idx].get("successors")
            prob = self.nodes[idx].get("tag_prob")
            cum_prob = cum_prob if prob is None else cum_prob * prob / 100.0
            for successor in successors:
                dispatch(idx=successor, cum_prob=cum_prob)

        def dispatch(idx: int, cum_prob: float) -> None:

            type_: str = self.nodes[idx].get("type")

            if type_ == "TERMINAL":
                terminal_node(idx=idx, cum_prob=cum_prob)

            if type_ == "DECISION":
                decision_node(idx=idx, cum_prob=cum_prob)

            if type_ == "CHANCE":
                chance_node(idx=idx, cum_prob=cum_prob)

        dispatch(idx=0, cum_prob=100.0)

    def _compute_selected_strategy(self) -> None:
        #
        def terminal_node(idx: int, selected_strategy: bool) -> None:
            self.nodes[idx]["selected_strategy"] = selected_strategy

        def chance_node(idx: int, selected_strategy: bool) -> None:
            self.nodes[idx]["selected_strategy"] = selected_strategy
            successors = self.nodes[idx].get("successors")
            for successor in successors:
                dispatch(idx=successor, selected_strategy=selected_strategy)

        def decision_node(idx: int, selected_strategy: bool) -> None:
            self.nodes[idx]["selected_strategy"] = selected_strategy
            successors = self.nodes[idx].get("successors")
            optimal_successor = self.nodes[idx].get("optimal_successor")
            for successor in successors:
                if successor == optimal_successor:
                    dispatch(idx=successor, selected_strategy=selected_strategy)
                else:
                    dispatch(idx=successor, selected_strategy=False)

        def dispatch(idx: int, selected_strategy: bool) -> None:
            type_: str = self.nodes[idx].get("type")
            if type_ == "TERMINAL":
                terminal_node(idx=idx, selected_strategy=selected_strategy)
            if type_ == "DECISION":
                decision_node(idx=idx, selected_strategy=selected_strategy)
            if type_ == "CHANCE":
                chance_node(idx=idx, selected_strategy=selected_strategy)

        dispatch(idx=0, selected_strategy=True)

    def _compute_risk_profiles(self):
        #
        def terminal(idx: int) -> None:
            value = self.nodes[idx].get("ExpVal")
            prob = self.nodes[idx].get("PathProb")
            self.nodes[idx]["RiskProfile"] = {value: prob}

        def chance(idx: int) -> None:
            successors = self.nodes[idx].get("successors")
            for successor in successors:
                dispatch(idx=successor)
            self.nodes[idx]["RiskProfile"] = {}
            for successor in successors:
                for key, value in self.nodes[successor]["RiskProfile"].items():
                    if key in self.nodes[idx]["RiskProfile"].keys():
                        self.nodes[idx]["RiskProfile"][key] += value
                    else:
                        self.nodes[idx]["RiskProfile"][key] = value

        def decision(idx: int) -> None:
            successors = self.nodes[idx].get("successors")
            for successor in successors:
                dispatch(idx=successor)
            optimal_successor = self.nodes[idx].get("optimal_successor")
            self.nodes[idx]["RiskProfile"] = self.nodes[optimal_successor][
                "RiskProfile"
            ]

        def dispatch(idx: int) -> None:
            #
            # if self.nodes[idx].get("selected_strategy") is False:
            #     return
            #
            type_ = self.nodes[idx].get("type")
            if type_ == "TERMINAL":
                terminal(idx=idx)
            if type_ == "CHANCE":
                chance(idx=idx)
            if type_ == "DECISION":
                decision(idx=idx)

        dispatch(idx=0)

    def evaluate(self):
        """This function is used to evaluate the nodes of the decision tree
        using the information in the variables.
        """

        self._build_call_kwargs()
        self._compute_expval_in_terminals_nodes()
        self._compute_expval_in_intermediate_nodes()
        self._compute_path_probabilities()
        self._compute_selected_strategy()
        self._compute_risk_profiles()

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
            name = self.nodes[idx].get("name")
            if "ExpVal" in self.nodes[idx].keys():
                expval = self.nodes[idx].get("ExpVal")
                pathprob = self.nodes[idx].get("PathProb")
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

                successors = self.nodes[idx].get("successors")
                for successor in successors:
                    dot = dispatch(idx=successor, dot=dot, max_deep=max_deep, deep=deep)
                    tag_name = self.nodes[successor].get("tag_name")
                    tag_value = self.nodes[successor].get("tag_value")
                    tag_prob = self.nodes[successor].get("tag_prob")
                    type_ = self.nodes[successor].get("type")
                    selected_strategy = self.nodes[successor].get("selected_strategy")

                    if "ExpVal" in self.nodes[successor].keys():
                        expval = self.nodes[successor].get("ExpVal")

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

                successors = self.nodes[idx].get("successors")
                for successor in successors:

                    if "selected_strategy" in self.nodes[successor].keys():
                        selected_strategy = self.nodes[successor]["selected_strategy"]
                    else:
                        selected_strategy = False

                    if policy_suggestion is True and selected_strategy is False:
                        continue

                    dot = dispatch(idx=successor, dot=dot, max_deep=max_deep, deep=deep)
                    tag_name = self.nodes[successor].get("tag_name")
                    tag_value = self.nodes[successor].get("tag_value")
                    type_ = self.nodes[successor].get("type")
                    selected_strategy = self.nodes[successor].get("selected_strategy")

                    if "ExpVal" in self.nodes[successor].keys():
                        expval = self.nodes[successor].get("ExpVal")

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

            type_ = self.nodes[idx].get("type")

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
