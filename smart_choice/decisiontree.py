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
from typing import Any, Union, List
import copy

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from graphviz import Digraph

from .datanodes import DataNodes

NAMEMAXLEN = 15


def jitter(x):
    stdev = 0.002 * (max(x) - min(x))
    return x + stdev * np.random.randn(len(x))


# -------------------------------------------------------------------------
#
#
#  U T I L I T Y    F U N C T I O N    E V A L U A T I O N
#
#
def _eval_utility_fn(value: float, utility_fn: str, risk_tolerance: float) -> float:
    if utility_fn is None:
        return value
    if utility_fn == "exp":
        return 1.0 - np.exp(-value / risk_tolerance)
    if utility_fn == "log":
        return np.log(value + risk_tolerance)
    raise ValueError(
        'Utility function {} unknown. Valid options {"exp", "log", None}'.format(
            utility_fn
        )
    )


def _eval_inv_utility_fn(value: float, utility_fn: str, risk_tolerance: float) -> float:
    if utility_fn is None:
        return value
    if utility_fn == "exp":
        return -1.0 * risk_tolerance * np.log(1 - np.minimum(0.9999, value))
    if utility_fn == "log":
        return np.exp(value) - risk_tolerance


# -------------------------------------------------------------------------
#
#
#  D E C I S I O N    T R E E
#
#
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
    #  C O N S T R U C T O R
    #
    #
    def __init__(self, nodes: DataNodes) -> None:

        self._tree_nodes = None
        self._data_nodes = nodes.copy()
        self._initial_variable = list(nodes.data.keys())[0]

        ## Prepares the empty structure of the tree
        self.rebuild()

        ## run flags
        self._is_evaluated = False
        self._with_rollback = False

    # -------------------------------------------------------------------------
    #
    #
    #  T R E E    D E E P C O P Y
    #
    #
    def copy(self):
        tree = DecisionTree(nodes=self._data_nodes.copy())
        tree._tree_nodes = copy.deepcopy(self._tree_nodes)
        tree._initial_variable = self._initial_variable
        return tree

    # -------------------------------------------------------------------------
    #
    #
    #  T R E E    C R E A T I O N
    #
    #
    def rebuild(self):
        self._build_skeleton()
        self._set_tag_attributes()
        self._set_payoff_fn()
        self._set_dependent_probability()
        self._set_dependent_outcomes()

    def _build_skeleton(self) -> None:
        #
        # Builds a structure where nodes are:
        #
        #   [
        #       {name: ..., type: ... successors: [ ... ]}
        #   ]
        #
        def dispatch(name: str) -> int:
            idx: int = len(self._tree_nodes)
            type_: str = self._data_nodes[name]["type"]
            self._tree_nodes.append(
                {"name": name, "type": type_, "forced_branch": None}
            )
            if "maximize" in self._data_nodes[name].keys():
                self._tree_nodes[idx]["maximize"] = self._data_nodes[name]["maximize"]
            if "branches" in self._data_nodes[name].keys():
                successors: list = []
                for branch in self._data_nodes[name].get("branches"):
                    successor: int = dispatch(name=branch[-1])
                    successors.append(successor)
                self._tree_nodes[idx]["successors"] = successors
            return idx

        #
        self._tree_nodes: list = []
        dispatch(name=self._initial_variable)

    def _set_tag_attributes(self) -> None:
        #
        # tag_value: is the value of the branch of the predecesor node
        # tag_prob: is the probability of the branch of the predecesor (chance) node
        #
        for node in self._tree_nodes:

            if "successors" not in node.keys():
                continue

            name: str = node.get("name")
            successors: list = node.get("successors")
            type_: str = node.get("type")
            branches: list = self._data_nodes[name].get("branches")

            if type_ == "DECISION":
                bnames = [x for x, _, _ in branches]
                values = [x for _, x, _ in branches]
                for successor, bname, value in zip(successors, bnames, values):
                    self._tree_nodes[successor]["tag_branch"] = bname
                    self._tree_nodes[successor]["tag_name"] = name
                    self._tree_nodes[successor]["tag_value"] = value

            if type_ == "CHANCE":
                bnames = [x for x, _, _, _ in branches]
                values = [x for _, _, x, _ in branches]
                probs = [x for _, x, _, _ in branches]
                for successor, bname, value, prob in zip(
                    successors, bnames, values, probs
                ):
                    self._tree_nodes[successor]["tag_branch"] = bname
                    self._tree_nodes[successor]["tag_name"] = name
                    self._tree_nodes[successor]["tag_prob"] = prob
                    self._tree_nodes[successor]["tag_value"] = value

    def _set_payoff_fn(self):

        for node in self._tree_nodes:
            if node.get("type") == "TERMINAL":
                name = node.get("name")
                payoff_fn = self._data_nodes[name].get("payoff_fn")
                node["payoff_fn"] = payoff_fn

    def _set_dependent_probability(self):
        #
        def dispatch(
            probability: float, conditions: dict, idx: int, args: dict
        ) -> None:

            args = args.copy()

            if "tag_name" in self._tree_nodes[idx].keys():
                tag_name = self._tree_nodes[idx]["tag_name"]
                tag_branch = self._tree_nodes[idx]["tag_branch"]
                args = {**args, **{tag_name: tag_branch}}

            change: bool = True

            for key in conditions.keys():
                if not (key in args.keys() and conditions[key] == args[key]):
                    change: bool = False

            if change is True:
                self._tree_nodes[idx]["tag_prob"] = probability

            if "successors" in self._tree_nodes[idx].keys():
                for successor in self._tree_nodes[idx]["successors"]:
                    dispatch(probability, conditions, idx=successor, args=args)

        if self._data_nodes.dependent_probabilities is not None:
            for probability, conditions in self._data_nodes.dependent_probabilities:
                dispatch(probability, conditions, idx=0, args={})

    def _set_dependent_outcomes(self) -> None:
        """Set outcomes in a node dependent on previous nodes"""

        def dispatch(outcome: float, conditions: dict, idx: int, args: dict) -> None:

            args = args.copy()

            if "tag_name" in self._tree_nodes[idx].keys():
                tag_name = self._tree_nodes[idx]["tag_name"]
                tag_branch = self._tree_nodes[idx]["tag_branch"]
                args = {**args, **{tag_name: tag_branch}}

            change: bool = True

            for key in conditions.keys():
                if not (key in args.keys() and conditions[key] == args[key]):
                    change: bool = False

            if change is True:
                self._tree_nodes[idx]["tag_value"] = outcome

            if "successors" in self._tree_nodes[idx].keys():
                for successor in self._tree_nodes[idx]["successors"]:
                    dispatch(outcome, conditions, idx=successor, args=args)

        if self._data_nodes.dependent_outcomes is not None:
            for outcome, conditions in self._data_nodes.dependent_outcomes:
                dispatch(outcome, conditions, idx=0, args={})

    # -------------------------------------------------------------------------
    #
    #
    #  S E T    P R O P E R T I E S
    #
    #
    # def set_node_values(self, new_values: dict) -> None:
    #     for idx, value in new_values.items():
    #         if "tag_value" not in self._nodes[idx].keys():
    #             raise ValueError(
    #                 'Tree node #{} does not have a value associated"'.format(idx)
    #             )
    #         self._nodes[idx]["tag_value"] = value

    # def set_node_probabilities(self, new_probabilities: dict) -> None:
    #     for idx, probability in new_probabilities.items():
    #         if "tag_prob" not in self._nodes[idx].keys():
    #             raise ValueError(
    #                 'Tree node #{} does not have a probability associated"'.format(idx)
    #             )
    #         self._nodes[idx]["tag_prob"] = probability

    # def set_variable_value(self, name, branch, value):
    #     for node in self._nodes:
    #         tag_name = node.get("tag_name")
    #         tag_branch = node.get("tag_branch")
    #         if (
    #             tag_name == name
    #             and tag_branch == branch
    #             and node.get("tag_value") is not None
    #         ):
    #             node["tag_value"] = value

    # def set_variable_probability(self, name, branch, probability):
    #     for node in self._nodes:
    #         tag_name = node.get("tag_name")
    #         tag_branch = node.get("tag_branch")
    #         if (
    #             tag_name == name
    #             and tag_branch == branch
    #             and node.get("tab_prob") is not None
    #         ):
    #             node["tag_prob"] = probability

    # def set_values(
    #     self, nodes: Union[int, List[int]], values: Union[float, List[float]]
    # ) -> None:
    #     if isinstance(nodes, int):
    #         nodes = [nodes]
    #     if isinstance(values, float):
    #         values = [values]
    #     for idx in nodes:
    #         if "tag_value" not in self._nodes[idx].keys():
    #             raise ValueError(
    #                 'Tree node #{} does not have a value associated"'.format(idx)
    #             )
    #     for idx, value in zip(nodes, values):
    #         self._nodes[idx]["tag_value"] = value

    # def set_probabilities(
    #     self, nodes: Union[int, List[int]], probabilities: Union[float, List[float]]
    # ) -> None:
    #     if isinstance(nodes, int):
    #         nodes = [nodes]
    #     if isinstance(probabilities, float):
    #         probabilities = [probabilities]
    #     for idx in nodes:
    #         if "tag_prob" not in self._nodes[idx].keys():
    #             raise ValueError(
    #                 'Tree node #{} does not have a probability associated"'.format(idx)
    #             )
    #     for idx, probability in zip(nodes, probabilities):
    #         self._nodes[idx]["tag_prob"] = probability

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
        def adjust_width(column: List[str]) -> list:
            maxwidth: int = max([len(txtline) for txtline in column]) + 2
            formatstr: str = "{:<" + str(maxwidth) + "s}"
            column: list = [formatstr.format(txtline) for txtline in column]
            return column

        def structure_colum() -> list:

            column: list = ["STRUCTURE", ""]
            for i_node, node in enumerate(self._tree_nodes):
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
            column: list = ["NAMES", ""] + [node["name"] for node in self._tree_nodes]
            return column

        def outcomes_column() -> list:
            column: list = []
            for node in self._tree_nodes:
                successors = node.get("successors")
                if successors is not None:
                    outcomes = [
                        self._tree_nodes[successor].get("tag_value")
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
            for node in self._tree_nodes:
                type_: str = node["type"]
                if type_ == "CHANCE":
                    successors = node.get("successors")
                    probabilities = [
                        self._tree_nodes[successor].get("tag_prob")
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
                    formatstr.format("{:.4f}".format(prob))[1:]
                    if prob < 1.0
                    else "1.000"
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
        lines = [line.strip() for line in lines]
        return "\n".join(lines)

    # -------------------------------------------------------------------------
    #
    #
    #  V I E W    N O D E S
    #
    #
    def nodes(self) -> None:
        """Prints the internal structure of the tree as a list of nodes."""
        text = {}
        for i_node, node in enumerate(self._tree_nodes):
            text[i_node] = node
        print(json.dumps(text, indent=4))

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
        view: str = "ev",
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

        def display_node(
            idx, is_first_node, is_last_node, is_optimal_choice, deep, max_deep
        ):
            #
            def prepare_text():

                type_ = self._tree_nodes[idx].get("type")
                tag_branch = self._tree_nodes[idx].get("tag_branch")
                tag_prob = self._tree_nodes[idx].get("tag_prob")
                tag_value = self._tree_nodes[idx].get("tag_value")
                pathprob = self._tree_nodes[idx].get("PathProb")
                expval = self._tree_nodes[idx].get("EV")
                exputl = self._tree_nodes[idx].get("EU")
                cequiv = self._tree_nodes[idx].get("CE")

                text = ""

                if tag_branch is not None:
                    if len(tag_branch) > NAMEMAXLEN:
                        tag_branch = tag_branch[: NAMEMAXLEN - 3] + "..."
                    fmt = " {:<" + str(NAMEMAXLEN) + "s}"
                    text += fmt.format(tag_branch)
                if tag_prob is not None:
                    text += " " + "{:.4f}".format(tag_prob)[1:]
                if tag_value is not None:
                    text += " {:8.2f}".format(tag_value)

                if type_ == "TERMINAL" and (
                    exputl is not None or cequiv is not None or expval is not None
                ):
                    text += " :"
                if view == "eu" and exputl is not None:
                    text += " {:8.2f}".format(exputl)
                if view == "ce" and cequiv is not None:
                    text += " {:8.2f}".format(cequiv)
                if view == "ev" and expval is not None:
                    text += " {:8.2f}".format(expval)
                if pathprob is not None:
                    if pathprob == np.float64(1.0):
                        text += " " + "1.000"
                    else:
                        text += " " + "{:.4f}".format(pathprob)[1:]

                return text

            # ---------------------------------------------------------------------------
            type_ = self._tree_nodes[idx]["type"]
            tag_name = self._tree_nodes[idx].get("tag_name")

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
            # max deep
            deep += 1

            # ---------------------------------------------------------------------------
            # line between --------[?] and childrens
            if type_ == "TERMINAL":
                text = []
            else:
                if tag_name is not None:
                    if is_first_node is True:
                        text = ["| {}".format(tag_name)]
                    elif max_deep is None or (
                        max_deep is not None and deep <= max_deep
                    ):
                        text = ["| {}".format(tag_name)]
                    else:
                        text = []
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
                    branch = (
                        "\\"
                        + "-" * (len_branch_text - 4)
                        + "[{}] #{}".format(letter, idx)
                    )
                else:
                    branch = (
                        "+"
                        + "-" * (len_branch_text - 4)
                        + "[{}] #{}".format(letter, idx)
                    )

                #
                # Policy suggestion
                #
                if max_deep is None or (max_deep is not None and deep <= max_deep):
                    text.append(branch)

            # ---------------------------------------------------------------------------
            # successors
            successors = self._tree_nodes[idx].get("successors")

            if successors is not None and (
                max_deep is None or (max_deep is not None and deep <= max_deep)
            ):
                for successor in successors:

                    # -------------------------------------------------------------------
                    # Mark optimal strategy
                    optimal_strategy = self._tree_nodes[successor].get(
                        "optimal_strategy"
                    )
                    is_optimal_choice = type_ == "DECISION" and optimal_strategy is True

                    # -------------------------------------------------------------------
                    # policy suggestion
                    if optimal_strategy is False and policy_suggestion is True:
                        continue

                    # -------------------------------------------------------------------
                    # vbar following the line of preious node
                    if policy_suggestion is False:
                        is_first_child_node = successor == successors[0]
                        is_last_child_node = successor == successors[-1]

                    else:
                        if type_ == "DECISION":
                            is_first_child_node = True
                            is_last_child_node = True
                        else:
                            is_first_child_node = successor == successors[0]
                            is_last_child_node = successor == successors[-1]

                    text_ = display_node(
                        successor,
                        is_first_child_node,
                        is_last_child_node,
                        is_optimal_choice,
                        deep,
                        max_deep,
                    )

                    vbar = " " if is_last_node else "|"

                    # ---------------------------------------------------------------------------
                    # indents the childrens
                    text_ = [
                        vbar + " " * (len_branch_text - 3) + line for line in text_
                    ]

                    # ---------------------------------------------------------------------------
                    # Adds a vertical bar as first element of a terminal node sequence
                    successor_type = self._tree_nodes[successor]["type"]
                    if successor_type == "TERMINAL" and successor == successors[0]:
                        successor_tag_name = self._tree_nodes[successor].get("tag_name")
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
            is_first_node=True,
            is_last_node=True,
            is_optimal_choice=False,
            deep=0,
            max_deep=max_deep,
        )

        text = [line.rstrip() for line in text]

        print("\n".join(text))

    # -------------------------------------------------------------------------
    #
    #
    #  E V A L U A T I O N
    #
    #
    def _generate_paths(self) -> None:
        #
        # Builts kwargs for user function in terminal nodes
        #
        def dispatch(idx: int, args: dict, probs: dict, branches: dict) -> None:

            args = args.copy()

            if "tag_name" in self._tree_nodes[idx].keys():
                name = self._tree_nodes[idx]["tag_name"]

            if "tag_value" in self._tree_nodes[idx].keys():
                value = self._tree_nodes[idx]["tag_value"]
                args = {**args, **{name: value}}

            if "tag_prob" in self._tree_nodes[idx].keys():
                prob = self._tree_nodes[idx]["tag_prob"]
                probs = {**probs, **{name: prob}}

            if "tag_branch" in self._tree_nodes[idx].keys():
                branch = self._tree_nodes[idx]["tag_branch"]
                branches = {**branches, **{name: branch}}

            type_ = self._tree_nodes[idx].get("type")

            if type_ == "TERMINAL":
                self._tree_nodes[idx]["payoff_fn_args"] = args
                self._tree_nodes[idx]["payoff_fn_probs"] = probs
                self._tree_nodes[idx]["payoff_fn_branches"] = branches
                return

            if "successors" in self._tree_nodes[idx].keys():
                for successor in self._tree_nodes[idx]["successors"]:
                    dispatch(idx=successor, args=args, probs=probs, branches=branches)

        dispatch(idx=0, args={}, probs={}, branches={})

    def _compute_payoff_fn(self):
        #
        # Compute payoff_fn in terminal nodes
        #

        for node in self._tree_nodes:

            if node.get("type") == "TERMINAL":
                payoff_fn_args = node.get("payoff_fn_args")
                payoff_fn_probs = node.get("payoff_fn_probs")
                payoff_fn_branches = node.get("payoff_fn_branches")
                payoff_fn = node.get("payoff_fn")
                node["EV"] = payoff_fn(
                    values=payoff_fn_args,
                    probabilities=payoff_fn_probs,
                    branches=payoff_fn_branches,
                )

    def evaluate(self) -> None:
        """Calculates the values at the end of the tree (terminal nodes)."""

        self._generate_paths()
        self._compute_payoff_fn()
        self._is_evaluated = True

    # -------------------------------------------------------------------------
    #
    #
    #  R O L L B A C K
    #
    #
    def rollback(
        self, view: str = "ev", utility_fn: str = None, risk_tolerance: float = 0
    ) -> float:
        """Computes the preferred decision by calculating the expected
        values at each internal node, and returns the expected value of the
        preferred decision.


        Computation begins at the terminal nodes towards the root node. In each
        chance node, the expected values are calculated as the sum of
        probabilities in each branch  multiplied by the expected value in
        the corresponding node. For decision nodes, the expected value is
        the maximum (or minimum) value of its branches.

        :param utilitiy_fn:

        :param risk_attitude:


        """
        if utility_fn is not None:
            self._payoff_to_utility(
                utility_fn=utility_fn, risk_tolerance=risk_tolerance
            )
        else:
            self._delete_utility_values()

        self._rollback_tree(use_exputl_criterion=utility_fn is not None)

        self._compute_optimal_strategy()
        self._compute_path_probabilities()

        if utility_fn is not None:
            self._compute_certainty_equivalents(
                utility_fn=utility_fn, risk_tolerance=risk_tolerance
            )

        self._with_rollback = True

        result = self._tree_nodes[0].get("EV")
        if utility_fn is not None:
            if view == "ce":
                result = self._tree_nodes[0].get("CE")
            if view == "eu":
                result = self._tree_nodes[0].get("EU")

        return result

    #
    # Auxiliary functions
    #
    def _payoff_to_utility(self, utility_fn: str, risk_tolerance: float) -> None:
        for node in self._tree_nodes:
            if node.get("type") == "TERMINAL":
                expected_val = node.get("EV")
                node["EU"] = _eval_utility_fn(
                    value=expected_val,
                    utility_fn=utility_fn,
                    risk_tolerance=risk_tolerance,
                )

    def _delete_utility_values(self) -> None:
        for node in self._tree_nodes:
            node.pop("EU", None)
            node.pop("CE", None)

    def _rollback_tree(self, use_exputl_criterion: bool) -> None:
        #
        # Computes the expected values at internal tree nodes.
        # At this point, expected values in terminal nodes are already
        # computed
        #
        def decision_node(idx: int) -> None:

            ## evaluate successors
            successors: list = self._tree_nodes[idx].get("successors")
            for i_successor, successor in enumerate(successors):
                dispatch(idx=successor)

            ## forced branch as index
            forced_branch: int = self._tree_nodes[idx].get("forced_branch")

            optimal_expval: float = None
            optimal_exputl: float = None
            optimal_criterion: float = None
            optimal_successor: int = None

            if forced_branch is None:

                maximize: bool = self._tree_nodes[idx].get("maximize")
                optimal_criterion: float = 0

                for i_successor, successor in enumerate(successors):

                    expval = self._tree_nodes[successor].get("EV")
                    exputl = self._tree_nodes[successor].get("EU")

                    if use_exputl_criterion is True:
                        criterion = exputl
                    else:
                        criterion = expval

                    update = False
                    if i_successor == 0:
                        update = True
                    if maximize is True and criterion > optimal_criterion:
                        update = True
                    if maximize is False and criterion < optimal_criterion:
                        update = True
                    if update is True:
                        optimal_expval = expval
                        optimal_exputl = exputl
                        optimal_successor = successor
                        optimal_criterion = criterion
            else:
                optimal_successor = successors[forced_branch]
                optimal_expval = self._tree_nodes[optimal_successor].get("EV")
                optimal_exputl = self._tree_nodes[optimal_successor].get("EU")

            self._tree_nodes[idx]["EV"] = optimal_expval
            if use_exputl_criterion is True:
                self._tree_nodes[idx]["EU"] = optimal_exputl
            self._tree_nodes[idx]["optimal_successor"] = optimal_successor

        def chance_node(idx: int) -> None:

            ## evaluate successors
            successors: list = self._tree_nodes[idx].get("successors")
            for successor in successors:
                dispatch(idx=successor)

            forced_branch: int = self._tree_nodes[idx].get("forced_branch")
            node_expval: float = 0
            node_exputl: float = 0

            if forced_branch is None:
                for successor in successors:
                    prob: float = self._tree_nodes[successor].get("tag_prob")
                    expval: float = self._tree_nodes[successor].get("EV")
                    node_expval += prob * expval
                    if use_exputl_criterion:
                        exputl: float = self._tree_nodes[successor].get("EU")
                        node_exputl += prob * exputl
            else:
                optimal_successor = successors[forced_branch]
                node_expval = self._tree_nodes[optimal_successor].get("EV")
                node_exputl = self._tree_nodes[optimal_successor].get("EU")

            self._tree_nodes[idx]["EV"] = node_expval
            if use_exputl_criterion is True:
                self._tree_nodes[idx]["EU"] = node_exputl

        def dispatch(idx: int) -> None:
            type_: str = self._tree_nodes[idx].get("type")
            if type_ == "DECISION":
                decision_node(idx=idx)
            if type_ == "CHANCE":
                chance_node(idx=idx)

        dispatch(idx=0)

    def _compute_optimal_strategy(self) -> None:
        #
        def terminal_node(idx: int, optimal_strategy: bool) -> None:
            self._tree_nodes[idx]["optimal_strategy"] = optimal_strategy

        def chance_node(idx: int, optimal_strategy: bool) -> None:
            self._tree_nodes[idx]["optimal_strategy"] = optimal_strategy
            forced_branch: int = self._tree_nodes[idx].get("forced_branch")
            successors = self._tree_nodes[idx].get("successors")
            if forced_branch is None:
                for successor in successors:
                    dispatch(idx=successor, optimal_strategy=optimal_strategy)
            else:
                for i_successor, successor in enumerate(successors):
                    if i_successor == forced_branch:
                        dispatch(idx=successor, optimal_strategy=optimal_strategy)
                    else:
                        dispatch(idx=successor, optimal_strategy=False)

        def decision_node(idx: int, optimal_strategy: bool) -> None:
            self._tree_nodes[idx]["optimal_strategy"] = optimal_strategy
            successors = self._tree_nodes[idx].get("successors")
            optimal_successor = self._tree_nodes[idx].get("optimal_successor")
            for successor in successors:
                if successor == optimal_successor:
                    dispatch(idx=successor, optimal_strategy=optimal_strategy)
                else:
                    dispatch(idx=successor, optimal_strategy=False)

        def dispatch(idx: int, optimal_strategy: bool) -> None:
            type_: str = self._tree_nodes[idx].get("type")
            if type_ == "TERMINAL":
                terminal_node(idx=idx, optimal_strategy=optimal_strategy)
            if type_ == "DECISION":
                decision_node(idx=idx, optimal_strategy=optimal_strategy)
            if type_ == "CHANCE":
                chance_node(idx=idx, optimal_strategy=optimal_strategy)

        dispatch(idx=0, optimal_strategy=True)

    def _compute_certainty_equivalents(
        self, utility_fn: str, risk_tolerance: float
    ) -> None:
        for node in self._tree_nodes:
            exputl = node.get("EU")
            node["CE"] = _eval_inv_utility_fn(exputl, utility_fn, risk_tolerance)

    def _compute_path_probabilities(self) -> None:
        #
        def terminal_node(idx: int, cum_prob: float) -> None:
            prob = self._tree_nodes[idx].get("tag_prob")
            cum_prob = cum_prob if prob is None else cum_prob * prob
            self._tree_nodes[idx]["PathProb"] = cum_prob

        def decision_node(idx: int, cum_prob: float) -> None:
            successors = self._tree_nodes[idx].get("successors")
            optimal_successor = self._tree_nodes[idx].get("optimal_successor")
            prob = self._tree_nodes[idx].get("tag_prob")
            prob = 1.0 if prob is None else prob
            for successor in successors:
                if successor == optimal_successor:
                    dispatch(idx=successor, cum_prob=cum_prob * prob)
                else:
                    dispatch(idx=successor, cum_prob=0.0)

        def chance_node(idx: int, cum_prob: float) -> None:
            successors = self._tree_nodes[idx].get("successors")
            forced_branch: int = self._tree_nodes[idx].get("forced_branch")
            if forced_branch is None:
                prob = self._tree_nodes[idx].get("tag_prob")
                cum_prob = cum_prob if prob is None else cum_prob * prob
                for successor in successors:
                    dispatch(idx=successor, cum_prob=cum_prob)
            else:
                ## same behaviour of a selection node
                for i_successor, successor in enumerate(successors):
                    if i_successor == forced_branch:
                        dispatch(idx=successor, cum_prob=cum_prob)
                    else:
                        dispatch(idx=successor, cum_prob=0.0)

        def dispatch(idx: int, cum_prob: float) -> None:
            type_: str = self._tree_nodes[idx].get("type")
            if type_ == "TERMINAL":
                terminal_node(idx=idx, cum_prob=cum_prob)
            if type_ == "DECISION":
                decision_node(idx=idx, cum_prob=cum_prob)
            if type_ == "CHANCE":
                chance_node(idx=idx, cum_prob=cum_prob)

        dispatch(idx=0, cum_prob=1.0)

    # -------------------------------------------------------------------------
    #
    #
    #  P L O T
    #
    #
    def plot(self, max_deep: int = None, policy_suggestion: bool = False):
        """Plots the tree.

        :param max_deep: maximum deep of the tree nodes to be plotted.

        :param policy_suggestion:
            When `True`, it plots only the subtree showing the nodes and branches
            relevants to the optimal decision (optimal strategy).

        """

        width = "0.25"
        height = "0.1"
        arrowsize = "0.3"
        fontsize = "8.0"

        def terminal(idx: int, main_dot, max_deep: int, deep: int):

            name = self._tree_nodes[idx].get("name")
            label = ""
            if "EV" in self._tree_nodes[idx].keys():
                expval = self._tree_nodes[idx].get("EV")
                label += "{:.2f}".format(expval)
            if "PathProb" in self._tree_nodes[idx].keys():
                pathprob = self._tree_nodes[idx].get("PathProb")
                if pathprob == np.float64(1.0):
                    label += " 1.000%"
                else:
                    label += " " + "{:.4f}%".format(pathprob)[1:]
            if label == "":
                label = name

            dot = Digraph(name="cluster_" + str(idx))
            dot.attr(rankdir="LR", color="white")
            dot.node(
                str(idx),
                label,
                shape="box",
                height=height,
                width=width,
                style="filled",
                color="powderblue",
                fontsize=fontsize,
                fontname="Courier New",
            )

            main_dot.subgraph(dot)

            ## return main_dot

        def chance(idx: int, main_dot, max_deep: int, deep: int):

            #
            # It's the maximum deep
            #
            deep += 1
            if max_deep is not None and deep >= max_deep:

                label = self._tree_nodes[idx].get("name")
                if "EV" in self._tree_nodes[idx].keys():
                    expval = self._tree_nodes[idx].get("EV")
                    label += r"\n{:0.2f}".format(expval)

                main_dot.node(
                    str(idx),
                    label=label,
                    shape="ellipse",
                    width=width,
                    height="0.05",
                    color="darkseagreen",
                    fontsize=fontsize,
                    fontname="Courier New",
                )
                return

            #
            # Draws the node and branches
            #
            label = self._tree_nodes[idx].get("name")
            dot = Digraph(name="cluster_" + str(idx))
            dot.attr(rankdir="LR", style="rounded", color="darkseagreen")

            if "EV" in self._tree_nodes[idx].keys():
                expval = self._tree_nodes[idx].get("EV")
                label += r"\n{:0.2f}".format(expval)

            dot.node(
                str(idx),
                label=label,
                shape="ellipse",
                width=width,
                height="0.05",
                color="darkseagreen",
                fontsize=fontsize,
                fontname="Courier New",
            )

            successors = self._tree_nodes[idx].get("successors")
            for successor in successors:
                tag_branch = self._tree_nodes[successor].get("tag_branch")
                dot.node(
                    str(idx) + tag_branch,
                    label=tag_branch,
                    shape="box",
                    height="0.1",
                    style="rounded",
                    color="darkseagreen",
                    fontsize=fontsize,
                    fontname="Courier New",
                )

                optimal_strategy = self._tree_nodes[successor].get("optimal_strategy")

                penwidth = "2" if optimal_strategy is True else "1"

                dot.edge(
                    str(idx),
                    str(idx) + tag_branch,
                    arrowsize=arrowsize,
                    penwidth=penwidth,
                )

            main_dot.subgraph(dot)

            #
            # Draw successors
            #
            if max_deep is None or (max_deep is not None and deep < max_deep):

                for successor in successors:
                    dispatch(
                        idx=successor, main_dot=main_dot, max_deep=max_deep, deep=deep
                    )

                    tag_branch = self._tree_nodes[successor].get("tag_branch")

                    optimal_strategy = self._tree_nodes[successor].get(
                        "optimal_strategy"
                    )

                    penwidth = "2" if optimal_strategy is True else "1"

                    main_dot.edge(
                        str(idx) + tag_branch,
                        str(successor),
                        arrowsize=arrowsize,
                        penwidth=penwidth,
                    )

            ## return main_dot

        def decision(idx: int, main_dot, max_deep: int, deep: int):

            name = self._tree_nodes[idx].get("name")

            label = name
            if "EV" in self._tree_nodes[idx].keys():
                expval = self._tree_nodes[idx].get("EV")
                label += r"\n{:0.2f}".format(expval)

            dot = Digraph(name="cluster_" + str(idx))
            dot.attr(rankdir="LR", style="rounded", color="peru")
            dot.node(
                str(idx),
                label=label,
                shape="box",
                width=width,
                height="0.05",
                style="rounded",
                color="chocolate",
                fontsize=fontsize,
                fontname="Courier New",
            )

            if max_deep is None or (max_deep is not None and deep < max_deep):

                successors = self._tree_nodes[idx].get("successors")

                #
                # Draws the branch
                #
                for successor in successors:

                    tag_branch = self._tree_nodes[successor].get("tag_branch")

                    dot.node(
                        str(idx) + tag_branch,
                        label=tag_branch,
                        shape="box",
                        style="rounded",
                        height="0.05",
                        color="chocolate",
                        fontsize=fontsize,
                        fontname="Courier New",
                    )

                    optimal_strategy = self._tree_nodes[successor].get(
                        "optimal_strategy"
                    )

                    penwidth = "2" if optimal_strategy is True else "1"

                    dot.edge(
                        str(idx),
                        str(idx) + tag_branch,
                        arrowsize=arrowsize,
                        penwidth=penwidth,
                    )

                main_dot.subgraph(dot)

                #
                # Draws successors
                #
                for successor in successors:

                    if "optimal_strategy" in self._tree_nodes[successor].keys():
                        optimal_strategy = self._tree_nodes[successor][
                            "optimal_strategy"
                        ]
                    else:
                        optimal_strategy = False

                    if policy_suggestion is True and optimal_strategy is False:
                        continue

                    dispatch(
                        idx=successor, main_dot=main_dot, max_deep=max_deep, deep=deep
                    )

                    #
                    # Connection
                    #
                    tag_branch = self._tree_nodes[successor].get("tag_branch")

                    optimal_strategy = self._tree_nodes[successor].get(
                        "optimal_strategy"
                    )

                    penwidth = "2" if optimal_strategy is True else "1"

                    main_dot.edge(
                        str(idx) + tag_branch,
                        str(successor),
                        arrowsize=arrowsize,
                        penwidth=penwidth,
                    )

        def dispatch(idx: int, main_dot, max_deep: int, deep: int):

            type_ = self._tree_nodes[idx].get("type")

            if type_ == "TERMINAL":
                ## main_dot = terminal(idx, main_dot, max_deep, deep)
                terminal(idx, main_dot, max_deep, deep)

            if type_ == "DECISION":
                ## main_dot = decision(idx, main_dot, max_deep, deep)
                decision(idx, main_dot, max_deep, deep)

            if type_ == "CHANCE":
                ## main_dot = chance(idx, main_dot, max_deep, deep)
                chance(idx, main_dot, max_deep, deep)

            ## return main_dot

        dot = Digraph()
        dot.attr(rankdir="LR")  # splines="compound"
        dispatch(idx=0, main_dot=dot, max_deep=max_deep, deep=0)
        ## dot = dispatch(idx=0, main_dot=dot, max_deep=max_deep, deep=0)
        return dot


if __name__ == "__main__":

    import doctest

    doctest.testmod()
