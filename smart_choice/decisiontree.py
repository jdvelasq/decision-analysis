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

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from graphviz import Digraph

from .datanodes import DataNodes

NAMEMAXLEN = 15

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
        def adjust_width(column: list[str]) -> list:
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

        def display_node(idx, is_last_node, is_optimal_choice, deep, max_deep):
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

                # if tag_branch is not None and tag_branch != str(tag_value):
                #     if len(tag_branch) > 10:
                #         tag_branch = tag_branch[:7] + "..."
                #     text += " {:<10s}".format(tag_branch)
                if tag_branch is not None:
                    if len(tag_branch) > NAMEMAXLEN:
                        tag_branch = tag_branch[: NAMEMAXLEN - 3] + "..."
                    fmt = " {:<" + str(NAMEMAXLEN) + "s}"
                    text += fmt.format(tag_branch)
                # text += " {:<10s}".format(tag_branch)
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
                text.append(branch)

            # ---------------------------------------------------------------------------
            # successors
            successors = self._tree_nodes[idx].get("successors")

            # ---------------------------------------------------------------------------
            # max deep
            deep += 1

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
        def dispatch(idx: int, args: dict, probs: dict) -> None:

            args = args.copy()

            if "tag_name" in self._tree_nodes[idx].keys():
                name = self._tree_nodes[idx]["tag_name"]

            if "tag_value" in self._tree_nodes[idx].keys():
                value = self._tree_nodes[idx]["tag_value"]
                args = {**args, **{name: value}}

            if "tag_prob" in self._tree_nodes[idx].keys():
                prob = self._tree_nodes[idx]["tag_prob"]
                probs = {**probs, **{name: prob}}

            type_ = self._tree_nodes[idx].get("type")

            if type_ == "TERMINAL":
                self._tree_nodes[idx]["payoff_fn_args"] = args
                self._tree_nodes[idx]["payoff_fn_probs"] = probs
                return

            if "successors" in self._tree_nodes[idx].keys():
                for successor in self._tree_nodes[idx]["successors"]:
                    dispatch(idx=successor, args=args, probs=probs)

        dispatch(idx=0, args={}, probs={})

    def _compute_payoff_fn(self):
        #
        # Compute payoff_fn in terminal nodes
        #

        for node in self._tree_nodes:

            if node.get("type") == "TERMINAL":
                payoff_fn_args = node.get("payoff_fn_args")
                payoff_fn_probs = node.get("payoff_fn_probs")
                payoff_fn = node.get("payoff_fn")
                node["EV"] = payoff_fn(values=payoff_fn_args, probs=payoff_fn_probs)

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
    #  R I S K    P R O F I L E
    #
    #
    def risk_profile(
        self, idx: int, cumulative: bool, single: bool, plot: bool = False
    ) -> None:
        """Plots a probability distribution of the tree results computed in a designed node.

        :param idx:

        :param cumulative:

        :param single:


        """

        def stem_single(idx: int, linefmt: str = "-k", color: str = "black"):

            risk_profile = self._tree_nodes[idx].get("RiskProfile").copy()
            values = sorted(risk_profile.keys())
            probs = [round(risk_profile[value], 2) for value in values]

            expval = self._tree_nodes[idx].get("EV")
            tag_value = self._tree_nodes[idx].get("tag_value")
            if tag_value is not None:
                label = "{};EV={:.2f}".format(tag_value, expval)
            else:
                label = "EV={:.2f}".format(expval)

            if plot is False:
                labels = [label] * len(probs)
                return pd.DataFrame(
                    {"Label": labels, "Value": values, "Probability": probs}
                )
            else:
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

            return None

        def step_single(idx: int, linefmt: str = "-k"):

            risk_profile = self._tree_nodes[idx].get("RiskProfile").copy()
            values = sorted(risk_profile.keys())
            probs = [round(risk_profile[value], 4) for value in values]
            cumprobs = np.cumsum(probs).tolist()

            expval = self._tree_nodes[idx].get("EV")
            tag_value = self._tree_nodes[idx].get("tag_value")
            if tag_value is not None:
                label = "{};EV={:.2f}".format(tag_value, expval)
            else:
                label = "EV={:.2f}".format(expval)

            if plot is False:
                labels = [label] * len(probs)
                return pd.DataFrame(
                    {
                        "Label": labels,
                        "Value": values,
                        "Cumulative Probability": cumprobs,
                    }
                )
            else:
                cumprobs = [0] + cumprobs
                values = values + [values[-1]]

                plt.gca().step(values, cumprobs, linefmt, label=label)

                plt.gca().spines["bottom"].set_visible(False)
                plt.gca().spines["left"].set_visible(False)
                plt.gca().spines["right"].set_visible(False)
                plt.gca().spines["top"].set_visible(False)

                plt.gca().set_xlabel("Expected values")
                plt.gca().set_ylabel("Cumulative probability")
                plt.gca().legend()

            return None

        def stem_multiple(idx: int):
            successors = self._tree_nodes[idx].get("successors")
            if plot is True:
                for i_successor, successor in enumerate(successors):
                    stem_single(successor, linefmts[i_successor], colors[i_successor])
            else:
                return pd.concat([stem_single(successor) for successor in successors])
            return None

        def step_multiple(idx: int):
            successors = self._tree_nodes[idx].get("successors")
            if plot is True:
                for i_successor, successor in enumerate(successors):
                    step_single(successor, linefmts[i_successor])
            else:
                return pd.concat([step_single(successor) for successor in successors])
            return None

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

        self._compute_risk_profiles(idx)

        if cumulative is False and single is True:
            result = stem_single(idx)
        if cumulative is True and single is True:
            result = step_single(idx)
        if cumulative is False and single is False:
            result = stem_multiple(idx)
        if cumulative is True and single is False:
            result = step_multiple(idx)
        if plot is False:
            return result

    def _compute_risk_profiles(self, idx: int) -> None:
        #
        def terminal(idx: int) -> None:
            value: float = self._tree_nodes[idx].get("EV")
            self._tree_nodes[idx]["RiskProfile"] = {value: 1.0}

        def chance(idx: int) -> None:
            successors = self._tree_nodes[idx].get("successors")
            for successor in successors:
                dispatch(idx=successor)
            self._tree_nodes[idx]["RiskProfile"] = {}
            for successor in successors:
                prob = self._tree_nodes[successor].get("tag_prob")

                for value_successor, prob_successor in self._tree_nodes[successor][
                    "RiskProfile"
                ].items():
                    if value_successor in self._tree_nodes[idx]["RiskProfile"].keys():
                        self._tree_nodes[idx]["RiskProfile"][value_successor] += (
                            prob * prob_successor
                        )
                    else:
                        self._tree_nodes[idx]["RiskProfile"][value_successor] = (
                            prob * prob_successor
                        )

        def decision(idx: int) -> None:
            successors = self._tree_nodes[idx].get("successors")
            for successor in successors:
                dispatch(idx=successor)
            optimal_successor = self._tree_nodes[idx].get("optimal_successor")
            self._tree_nodes[idx]["RiskProfile"] = self._tree_nodes[optimal_successor][
                "RiskProfile"
            ]

        def dispatch(idx: int) -> None:
            type_ = self._tree_nodes[idx].get("type")
            if type_ == "TERMINAL":
                terminal(idx=idx)
            if type_ == "CHANCE":
                chance(idx=idx)
            if type_ == "DECISION":
                decision(idx=idx)

        dispatch(idx=idx)

    # -------------------------------------------------------------------------
    #
    #  P R O B A B I L I S T I C     S E N S I T I V I T Y
    #
    #
    def probabilistic_sensitivity(self, varname: str, plot: bool = False) -> Any:
        """Display a probabilistic sensitivity plot for a chance node.

        :param varname:
            Name of the probabilistic variable.

        """

        def probabilistic_sensitivity_chance() -> Any:

            top_branch, bottom_branch = self._data_nodes.get_top_bottom_branches(
                varname
            )
            self._data_nodes.set_probabitlities_to_zero(varname)

            results = []
            probabilities = np.linspace(start=0, stop=1, num=21).tolist()
            for top_probability in probabilities:

                branch = self._data_nodes[varname]["branches"][top_branch]
                self._data_nodes[varname]["branches"][top_branch] = (
                    branch[0],
                    1 - top_probability,
                    branch[2],
                    branch[3],
                )

                branch = self._data_nodes[varname]["branches"][bottom_branch]
                self._data_nodes[varname]["branches"][bottom_branch] = (
                    branch[0],
                    top_probability,
                    branch[2],
                    branch[3],
                )

                self._build_skeleton()
                self._set_tag_attributes()
                self._set_payoff_fn()
                self.evaluate()
                self.rollback()
                results.append(self._tree_nodes[0].get("EV"))

            if plot is True:
                plt.gca().plot(probabilities, results, "-k")
                plt.gca().spines["bottom"].set_visible(False)
                plt.gca().spines["left"].set_visible(False)
                plt.gca().spines["right"].set_visible(False)
                plt.gca().spines["top"].set_visible(False)
                plt.gca().set_ylabel("Expected values")
                plt.gca().set_xlabel("Probability")
                plt.grid()
                return None

            return pd.DataFrame({"Probability": probabilities, "Values": results})

        def probabilistic_sensitivity_decision() -> None:

            top_branch, bottom_branch = self._data_nodes.get_top_bottom_branches(
                varname
            )
            self._data_nodes.set_probabitlities_to_zero(varname)

            results = {}
            successors = self._tree_nodes[0].get("successors")
            tag_values = [
                self._tree_nodes[successor].get("tag_value") for successor in successors
            ]
            for tag_value in tag_values:
                results[tag_value] = []

            probabilities = np.linspace(start=0, stop=1, num=21).tolist()
            for probability in probabilities:

                branch = self._data_nodes[varname]["branches"][bottom_branch]
                self._data_nodes[varname]["branches"][bottom_branch] = (
                    branch[0],
                    probability,
                    branch[2],
                    branch[3],
                )

                branch = self._data_nodes[varname]["branches"][top_branch]
                self._data_nodes[varname]["branches"][top_branch] = (
                    branch[0],
                    1.0 - probability,
                    branch[2],
                    branch[3],
                )

                self._build_skeleton()
                self._set_tag_attributes()
                self._set_payoff_fn()
                self.evaluate()
                self.rollback()
                expvals = [
                    self._tree_nodes[successor].get("EV") for successor in successors
                ]
                for expval, tag_value in zip(expvals, tag_values):
                    results[tag_value].append(expval)

            if plot is True:
                for tag_value in tag_values:
                    plt.gca().plot(
                        probabilities, results[tag_value], label=str(tag_value)
                    )
                plt.gca().spines["bottom"].set_visible(False)
                plt.gca().spines["left"].set_visible(False)
                plt.gca().spines["right"].set_visible(False)
                plt.gca().spines["top"].set_visible(False)
                plt.gca().set_ylabel("Expected values")
                plt.gca().set_xlabel("Probability")
                plt.gca().legend()
                plt.grid()
                return None

            return pd.concat(
                [
                    pd.DataFrame(
                        {
                            "Branch": [str(tag_value)] * len(probabilities),
                            "Probability": probabilities,
                            "Value": results[tag_value],
                        }
                    )
                    for tag_value in tag_values
                ]
            )

        #
        #
        #
        type_ = self._data_nodes[varname]["type"]
        if type_ != "CHANCE":
            raise ValueError('Variable {} is {} != "CHANCE"'.format(varname, type_))

        orig_variables = self._data_nodes.copy()
        type_root = self._tree_nodes[0].get("type")
        if type_root == "CHANCE":
            result = probabilistic_sensitivity_chance()
        if type_root == "DECISION":
            result = probabilistic_sensitivity_decision()

        self._data_nodes = orig_variables
        self._build_skeleton()
        self._set_tag_attributes()
        self._set_payoff_fn()
        self.evaluate()
        self.rollback()

        if plot is False:
            return result

    # -------------------------------------------------------------------------
    #
    #  V A L U E     S E N S I T I V I T Y
    #
    #

    def value_sensitivity(
        self, name: str, branch: str, values: tuple, n_points=11, plot: bool = False
    ):
        def get_original_value():
            for node in self._tree_nodes:
                tag_name = node.get("tag_name")
                tag_branch = node.get("tag_branch")
                if tag_name == name and tag_branch == branch:
                    return node.get("tag_value")

        def restore_original_value(original_value):
            for i_node, node in enumerate(self._tree_nodes):
                tag_name = node.get("tag_name")
                tag_branch = node.get("tag_branch")
                if tag_name == name and tag_branch == branch:
                    self._tree_nodes[i_node]["tag_value"] = original_value

        def value_sensitivity_chance(
            name: str, branch: str, values: tuple, n_points=11, plot: bool = False
        ):

            min_value, max_value = values
            values = np.linspace(start=min_value, stop=max_value, num=n_points)

            expvals = []
            for value in values:
                for i_node, node in enumerate(self._tree_nodes):
                    tag_name = node.get("tag_name")
                    tag_branch = node.get("tag_branch")
                    if tag_name == name and tag_branch == branch:
                        self._tree_nodes[i_node]["tag_value"] = value
                self.evaluate()
                expvals.append(round(self.rollback(), 2))

            if plot is False:
                return pd.DataFrame(
                    {
                        "value": values,
                        "ExpVal": expvals,
                    }
                )

            plt.gca().plot(values, expvals)
            plt.gca().spines["bottom"].set_visible(False)
            plt.gca().spines["left"].set_visible(False)
            plt.gca().spines["right"].set_visible(False)
            plt.gca().spines["top"].set_visible(False)
            plt.gca().set_ylabel("Expected values")
            plt.gca().set_xlabel("Values")
            # plt.gca().legend()
            plt.grid()

            return None

        def value_sensitivity_decision(
            name: str, branch: str, values: tuple, n_points=11, plot: bool = False
        ):

            results = {}
            successors = self._tree_nodes[0].get("successors")
            tag_branches_root = [
                self._tree_nodes[successor].get("tag_branch")
                for successor in successors
            ]
            for tag_branch_root in tag_branches_root:
                results[tag_branch_root] = []

            min_value, max_value = values
            values = np.linspace(start=min_value, stop=max_value, num=n_points)

            for value in values:
                for i_node, node in enumerate(self._tree_nodes):
                    tag_name = node.get("tag_name")
                    tag_branch = node.get("tag_branch")
                    if tag_name == name and tag_branch == branch:
                        self._tree_nodes[i_node]["tag_value"] = value
                self.evaluate()
                self.rollback()
                expvals = [
                    self._tree_nodes[successor].get("EV") for successor in successors
                ]
                for expval, tag_branch_root in zip(expvals, tag_branches_root):
                    results[tag_branch_root].append(expval)

            if plot is False:
                return pd.concat(
                    [
                        pd.DataFrame(
                            {
                                "Branch": [tag_branch_root] * len(values),
                                "Value": values,
                                "ExpVal": results[tag_branch_root],
                            }
                        )
                        for tag_branch_root in tag_branches_root
                    ]
                )

            plt.gca().plot(values, expvals)
            plt.gca().spines["bottom"].set_visible(False)
            plt.gca().spines["left"].set_visible(False)
            plt.gca().spines["right"].set_visible(False)
            plt.gca().spines["top"].set_visible(False)
            plt.gca().set_ylabel("Expected values")
            plt.gca().set_xlabel("Values")
            # plt.gca().legend()
            plt.grid()

            return None

        original_value = get_original_value()
        type_ = self._tree_nodes[0]["type"]
        if type_ == "CHANCE":
            result = value_sensitivity_chance(
                name=name, branch=branch, values=values, n_points=n_points
            )
        if type_ == "DECISION":
            result = value_sensitivity_decision(
                name=name, branch=branch, values=values, n_points=n_points
            )

        restore_original_value(original_value)
        return result

    # -------------------------------------------------------------------------
    #
    #  R I S K    S E N S I T I V I T Y
    #
    #
    def risk_sensitivity(
        self, utility_fn: str, risk_tolerance: float, plot: bool = False
    ) -> None:
        """Plots a risk tolrecance plot."""

        def _risk_attitude_decision():

            results = {}
            successors = self._tree_nodes[0].get("successors")
            tag_values = [
                self._tree_nodes[successor].get("tag_value") for successor in successors
            ]
            for tag_value in tag_values:
                results[tag_value] = []

            risk_aversions = np.linspace(
                start=0, stop=1.0 / risk_tolerance, num=11
            ).tolist()

            for risk_aversion in risk_aversions:

                if risk_aversion == np.float64(0):
                    self.evaluate()
                    self.rollback()
                    ceqs = [
                        self._tree_nodes[successor].get("EV")
                        for successor in successors
                    ]
                else:
                    self.evaluate()
                    self.rollback(
                        utility_fn=utility_fn, risk_tolerance=1.0 / risk_aversion
                    )
                    ceqs = [
                        self._tree_nodes[successor].get("CE")
                        for successor in successors
                    ]

                for ceq, tag_value in zip(ceqs, tag_values):
                    results[tag_value].append(ceq)

            if plot is True:

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
                plt.xticks(risk_aversions, labels)
                plt.gca().spines["bottom"].set_visible(False)
                plt.gca().spines["left"].set_visible(False)
                plt.gca().spines["right"].set_visible(False)
                plt.gca().spines["top"].set_visible(False)
                plt.gca().set_ylabel("Certainty equivalent")
                plt.gca().set_xlabel("Risk tolerance")
                plt.gca().legend()
                plt.grid()

                return None

            results["Risk Tolerance"] = [
                "Infinity"
                if risk_aversion == np.float(0)
                else int(round(1 / risk_aversion, 0))
                for risk_aversion in risk_aversions
            ]
            return pd.DataFrame(results)

        def _risk_attitude_chance():

            results = {}
            successors = self._tree_nodes[0].get("successors")
            tag_values = [
                self._tree_nodes[successor].get("tag_value") for successor in successors
            ]
            for tag_value in tag_values:
                results[tag_value] = []

            risk_aversions = np.linspace(
                start=0, stop=1.0 / risk_tolerance, num=11
            ).tolist()

            for risk_aversion in risk_aversions:

                if risk_aversion == np.float64(0):
                    self.evaluate()
                    self.rollback()
                    ceqs = [
                        self._tree_nodes[successor].get("EV")
                        for successor in successors
                    ]
                else:
                    self.evaluate()
                    self.rollback(
                        utility_fn=utility_fn, risk_tolerance=1.0 / risk_aversion
                    )
                    ceqs = [
                        self._tree_nodes[successor].get("CE")
                        for successor in successors
                    ]

                for ceq, tag_value in zip(ceqs, tag_values):
                    results[tag_value].append(ceq)

            if plot is True:
                for tag_value in tag_values:
                    plt.gca().plot(
                        risk_aversions, results[tag_value], label=str(tag_value)
                    )

                labels = [
                    "Infinity"
                    if risk_aversion == np.float(0)
                    else str(int(round(1 / risk_aversion, 0)))
                    for risk_aversion in risk_aversions
                ]
                plt.xticks(risk_aversions, labels)
                plt.gca().spines["bottom"].set_visible(False)
                plt.gca().spines["left"].set_visible(False)
                plt.gca().spines["right"].set_visible(False)
                plt.gca().spines["top"].set_visible(False)
                plt.gca().set_ylabel("Expected values")
                plt.gca().set_xlabel("Risk tolerance")
                plt.gca().invert_xaxis()
                plt.gca().legend()
                plt.grid()
                return None

            results["Risk Tolerance"] = [
                "Infinity"
                if risk_aversion == np.float(0)
                else int(round(1 / risk_aversion, 0))
                for risk_aversion in risk_aversions
            ]
            return pd.DataFrame(results)

        type_ = self._tree_nodes[0].get("type")
        if type_ == "DECISION":
            result = _risk_attitude_decision()
        if type_ == "CHANCE":
            result = _risk_attitude_chance()

        self.rollback()
        if plot is False:
            return result

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
            name = self._tree_nodes[idx].get("name")
            if "ExpVal" in self._tree_nodes[idx].keys():
                value = self._tree_nodes[idx].get("ExpVal")
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
            type_ = self._tree_nodes[idx]["type"]
            if type_ == "TERMINAL":
                text = node_type_terminal(text, idx, is_last_node)
            if type_ == "DECISION":
                text = node_type_decision(text, is_last_node)
            if type_ == "CHANCE":
                text = node_type_chance(text, is_last_node)
            return text

        def newline(text, idx, key, formatstr):
            text = text.copy()
            if key in self._tree_nodes[idx].keys():
                value = self._tree_nodes[idx].get(key)
                text.append(formatstr.format(value))
            return text

        def selected_strategy(text, idx):
            text = text.copy()
            if "selected_strategy" in self._tree_nodes[idx].keys():
                if self._tree_nodes[idx]["selected_strategy"] is True:
                    text.append("| (selected strategy)")
            return text

        def riskprofile(text: list, idx: int) -> list:
            text = text.copy()
            type_ = self._tree_nodes[idx]["type"]
            if type_ != "TERMINAL" and "RiskProfile" in self._tree_nodes[idx].keys():
                text.append("| Risk Profile:")
                text.append("|         Value  Prob")
                values = sorted(self._tree_nodes[idx]["RiskProfile"].keys())
                for value in values:
                    prob = self._tree_nodes[idx]["RiskProfile"][value]
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
            if "successors" not in self._tree_nodes[idx].keys():
                return text

            successors = self._tree_nodes[idx]["successors"]

            type_ = self._tree_nodes[idx]["type"]

            for successor in successors:

                next_is_last_node = successor == successors[-1]

                if "selected_strategy" in self._tree_nodes[successor].keys():
                    selected_strategy = self._tree_nodes[successor]["selected_strategy"]
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
            type_ = self._tree_nodes[idx]["type"]
            text.append("| #{}".format(idx))
            #
            if "tag_name" in self._tree_nodes[idx].keys():
                text.append(
                    "| {}={}".format(
                        self._tree_nodes[idx].get("tag_name"),
                        self._tree_nodes[idx].get("tag_value"),
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
            name = self._tree_nodes[idx].get("name")
            if "ExpVal" in self._tree_nodes[idx].keys():
                expval = self._tree_nodes[idx].get("ExpVal")
                pathprob = self._tree_nodes[idx].get("PathProb")
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

                successors = self._tree_nodes[idx].get("successors")
                for successor in successors:
                    dot = dispatch(idx=successor, dot=dot, max_deep=max_deep, deep=deep)
                    tag_name = self._tree_nodes[successor].get("tag_name")
                    tag_value = self._tree_nodes[successor].get("tag_value")
                    tag_prob = self._tree_nodes[successor].get("tag_prob")
                    type_ = self._tree_nodes[successor].get("type")
                    selected_strategy = self._tree_nodes[successor].get(
                        "selected_strategy"
                    )

                    if "ExpVal" in self._tree_nodes[successor].keys():
                        expval = self._tree_nodes[successor].get("ExpVal")

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

                successors = self._tree_nodes[idx].get("successors")
                for successor in successors:

                    if "selected_strategy" in self._tree_nodes[successor].keys():
                        selected_strategy = self._tree_nodes[successor][
                            "selected_strategy"
                        ]
                    else:
                        selected_strategy = False

                    if policy_suggestion is True and selected_strategy is False:
                        continue

                    dot = dispatch(idx=successor, dot=dot, max_deep=max_deep, deep=deep)
                    tag_name = self._tree_nodes[successor].get("tag_name")
                    tag_value = self._tree_nodes[successor].get("tag_value")
                    type_ = self._tree_nodes[successor].get("type")
                    selected_strategy = self._tree_nodes[successor].get(
                        "selected_strategy"
                    )

                    if "ExpVal" in self._tree_nodes[successor].keys():
                        expval = self._tree_nodes[successor].get("ExpVal")

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

            type_ = self._tree_nodes[idx].get("type")

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
        return self._data_nodes

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
