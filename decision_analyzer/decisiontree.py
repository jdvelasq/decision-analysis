"""
Decision Tree Model
===============================================================================

**Node Creation**


"""

# from typing import List


class DecisionTree:
    """Decision Tree Model"""

    def __init__(self, variables: list, initial_variable: str) -> None:
        self.nodes = None
        self.variables = variables
        self.initial_variable = initial_variable

    def _build_skeleton(self) -> None:
        #
        # Builds a structure where nodes are:
        #
        #   [
        #       {name: ..., type: ... successors: [ ... ]}
        #   ]
        #
        def build(name: str) -> int:
            idx: int = len(self.nodes)
            type_: str = self.variables[name]["type"]
            self.nodes.append({"name": name, "type": type_})
            if "max" in self.variables[name].keys():
                self.nodes[idx]["max"] = self.variables[name]["max"]
            if "branches" in self.variables[name].keys():
                successors: list = []
                for branch in self.variables[name].get("branches"):
                    successor: int = build(name=branch[-1])
                    successors.append(successor)
                self.nodes[idx]["successors"] = successors
            return idx

        #
        self.nodes: list = []
        build(name=self.initial_variable)

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
            branches: list = self.variables[name].get("branches")

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

    def build(self):
        """This function is used to build the decision tree using the information in the
        variables.
        """

        self._build_skeleton()
        self._set_tag_attributes()

    def print_nodes(self) -> None:
        """Prints the database of nodes."""
        for i_node, node in enumerate(self.nodes):
            print("#{:<3s} {}".format(str(i_node), node))

    def export_text(self):
        """Exports the tree as text diagram."""

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

        def export_branches(text: list, idx: int, is_last_node: bool) -> list:

            text = text.copy()
            if "successors" not in self.nodes[idx].keys():
                return text

            successors = self.nodes[idx]["successors"]
            for successor in successors:

                next_is_last_node = successor == successors[-1]

                result = export_node(successor, next_is_last_node)

                for txt in result:
                    if is_last_node is True:
                        text.append(" " * 9 + txt)
                    else:
                        text.append("|" + " " * 8 + txt)

            return text

        def export_node(idx: int, is_last_node: bool) -> list:

            type_ = self.nodes[idx]["type"]

            text = ["|"]

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
            text = selected_strategy(text, idx)
            text = node_type(text, idx, is_last_node)
            text = export_branches(text, idx, is_last_node)

            return text

        text = export_node(idx=0, is_last_node=True)

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

            type_ = self._get_node_type(idx=idx)

            if type_ == "TERMINAL":
                self.nodes[idx]["user_args"] = args
            else:
                if "successors" in self.nodes[idx].keys():
                    for successor in self.nodes[idx]["successors"]:
                        set_fn_args(idx=successor, args=args)

        set_fn_args(idx=0, args={})

    def _evaluate_terminal_nodes(self) -> None:
        #
        def cumulative(**kwargs):
            return sum(v for _, v in kwargs.items())

        for node in self.nodes:
            user_args = node.get("user_args")
            if user_args:
                name = node.get("name")
                user_fn = self.variables[name].get("user_fn")
                if user_fn is None:
                    user_fn = cumulative
                node["ExpVal"] = user_fn(**user_args)

    # def _compute_expected_values(self):
    #     #
    #     def terminal_node(idx: int) -> float:
    #         return self.nodes[idx].get("ExpVal")

    #     def decision_node(idx: int) -> float:

    #         name: str = self.nodes[idx]["name"]
    #         max_: bool = self.variables[name]["max_"]
    #         node_branches: List = self._get_next_idx(idx=idx)

    #         optimal_value: float = None
    #         optimal_branch: int = None

    #         for i_branch, next_idx in enumerate(node_branches):

    #             value = compute_expval(idx=next_idx)

    #             if max_ is True:

    #                 if optimal_value is None or value > optimal_value:
    #                     optimal_value = value
    #                     optimal_branch = i_branch

    #             else:
    #                 if optimal_value is None or value < optimal_value:
    #                     optimal_value = value
    #                     optimal_branch = i_branch

    #         self.nodes[idx]["ExpVal"] = optimal_value
    #         self.nodes[idx]["optimal_branch"] = optimal_branch
    #         return optimal_value

    #     def chance_node(idx: int) -> float:

    #         name: str = self.nodes[idx]["name"]

    #         var_branches = self.variables[name]["branches"]
    #         probs = [prob for prob, _, _ in var_branches]

    #         node_branches: List = self._get_next_idx(idx=idx)

    #         node_value: float = 0

    #         for next_idx, prob in zip(node_branches, probs):
    #             value: float = compute_expval(idx=next_idx)
    #             node_value += prob * value / 100.0

    #         self.nodes[idx]["ExpVal"] = node_value
    #         return node_value

    #     #
    #     def compute_expval(idx: int) -> float:

    #         type_: str = self._get_node_type(idx=idx)

    #         if type_ == "TERMINAL":
    #             retval = terminal_node(idx=idx)

    #         if type_ == "DECISION":
    #             retval = decision_node(idx=idx)

    #         if type_ == "CHANCE":
    #             retval = chance_node(idx=idx)

    #         return retval

    #     #
    #     compute_expval(idx=0)

    def evaluate(self):
        """This function is used to build the decision tree using the information in the
        variables.
        """

        self._build_call_kwargs()
        self._evaluate_terminal_nodes()
        # self._compute_expected_values()
        # self._path_probability()
        # self._selected_strategy()

    #
    #
    #  R E F A C T O R I N G
    #
    #

    def _get_node_type(self, name: str = None, idx: int = None) -> str:
        #
        # Gets the node type ("TERMINAL", "CHANCE", "DECISION") from
        # table of variables
        #
        if idx is not None:
            name = self.nodes[idx].get("name")
        return self.variables[name].get("type")

    def _get_next_idx(self, idx: int = None) -> list:
        return self.nodes[idx].get("next_idx")

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

    # def _path_probability(self) -> None:
    #     #
    #     def terminal_node(idx: int, cum_prob: float) -> None:
    #         self.nodes[idx]["PathProb"] = cum_prob * 100.0

    #     def decision_node(idx: int, cum_prob: float) -> None:
    #         optimal_branch = self.nodes[idx].get("optimal_branch")
    #         branches = self.nodes[idx].get("next_idx")
    #         for i_branch, idx_branch in enumerate(branches):
    #             if i_branch == optimal_branch:
    #                 compute_path_prob(idx=idx_branch, cum_prob=1.0)
    #             else:
    #                 compute_path_prob(idx=idx_branch, cum_prob=0.0)

    #     def chance_node(idx: int, cum_prob: float) -> None:

    #         branches = self.nodes[idx].get("next_idx")
    #         name: str = self.nodes[idx]["name"]
    #         var_branches = self.variables[name]["branches"]
    #         probs = [prob for prob, _, _ in var_branches]

    #         for prob, idx_branch in zip(probs, branches):
    #             compute_path_prob(idx=idx_branch, cum_prob=cum_prob * prob / 100)

    #     def compute_path_prob(idx: int, cum_prob: float) -> None:

    #         type_: str = self._get_node_type(idx=idx)

    #         if type_ == "TERMINAL":
    #             terminal_node(idx=idx, cum_prob=cum_prob)

    #         if type_ == "DECISION":
    #             decision_node(idx=idx, cum_prob=cum_prob)

    #         if type_ == "CHANCE":
    #             chance_node(idx=idx, cum_prob=cum_prob)

    #     compute_path_prob(idx=0, cum_prob=1.0)

    # def _selected_strategy(self) -> None:
    #     #
    #     def terminal_node(idx: int, selected_strategy: bool) -> None:
    #         self.nodes[idx]["selected_strategy"] = selected_strategy

    #     def chance_node(idx: int, selected_strategy: bool) -> None:
    #         self.nodes[idx]["selected_strategy"] = selected_strategy
    #         branches = self.nodes[idx].get("next_idx")
    #         for idx_branch in branches:
    #             dispatch(idx=idx_branch, selected_strategy=selected_strategy)

    #     def decision_node(idx: int, selected_strategy: bool) -> None:
    #         self.nodes[idx]["selected_strategy"] = selected_strategy
    #         branches = self.nodes[idx].get("next_idx")
    #         optimal_branch = self.nodes[idx].get("optimal_branch")
    #         for i_branch, idx_branch in enumerate(branches):
    #             if i_branch == optimal_branch:
    #                 dispatch(idx=idx_branch, selected_strategy=selected_strategy)
    #             else:
    #                 dispatch(idx=idx_branch, selected_strategy=False)

    #     #
    #     def dispatch(idx: int, selected_strategy: bool) -> None:

    #         type_: str = self._get_node_type(idx=idx)
    #         if type_ == "TERMINAL":
    #             terminal_node(idx=idx, selected_strategy=selected_strategy)

    #         if type_ == "DECISION":
    #             decision_node(idx=idx, selected_strategy=selected_strategy)

    #         if type_ == "CHANCE":
    #             chance_node(idx=idx, selected_strategy=selected_strategy)

    #     dispatch(idx=0, selected_strategy=True)

    # def _evaluate_user_fn(self):
    #     def cumulative(**kwargs):
    #         return sum(v for _, v in kwargs.items())

    #     for node in self.tree_nodes:
    #         if node.get("type") == "TERMINAL":
    #             kwargs = node.get("user_fn_args")
    #             user_fn = node.get("user_fn")
    #             if user_fn is None:
    #                 user_fn = cumulative
    #             node["user_fn_value"] = user_fn(**kwargs)

    # def compute_expected_values(self):
    #     """Compute expected values"""

    #     def compute_node(idx: int) -> float:

    #         current_node: int = self.tree_nodes[idx]

    #         if current_node.get("type") == "TERMINAL":
    #             current_expected_value = current_node.get("user_fn_value")

    #         if current_node.get("type") == "CHANCE":
    #             #
    #             # Las probabilidades de cada rama están en el nodo siguiente
    #             # independiente del tipo del siguiente nodo
    #             #
    #             current_expected_value = 0
    #             for idx_next in current_node.get("next"):
    #                 branch_exp_value = compute_node(idx_next)
    #                 probability = self.tree_nodes[idx_next].get("prob") / 100.0
    #                 current_expected_value += probability * branch_exp_value

    #         if current_node.get("type") == "DECISION":
    #             #
    #             # El nodo escoge la rama y no hay probabilidades
    #             # asociadas a los nodos siguientes
    #             #
    #             current_expected_value = None
    #             optimal_branch = 0

    #             if current_node.get("max_") is True:
    #                 for i_branch, idx_next in enumerate(current_node.get("next")):
    #                     branch_exp_value = compute_node(idx_next)
    #                     if current_expected_value is None:
    #                         current_expected_value = branch_exp_value
    #                         optimal_branch = i_branch
    #                     if branch_exp_value > current_expected_value:
    #                         current_expected_value = branch_exp_value
    #                         optimal_branch = i_branch

    #             if current_node.get("max_") is False:
    #                 for i_branch, idx_next in enumerate(current_node.get("next")):
    #                     branch_exp_value = compute_node(idx_next)
    #                     if current_expected_value is None:
    #                         current_expected_value = branch_exp_value
    #                         optimal_branch = i_branch
    #                     if branch_exp_value < current_expected_value:
    #                         current_expected_value = branch_exp_value
    #                         optimal_branch = i_branch

    #             current_node["optimal_branch"] = optimal_branch

    #         current_node["ExpVal"] = current_expected_value
    #         return current_expected_value

    #     compute_node(idx=0)

    # def compute_pathprob(self):
    #     """Computes the probability of the terminal nodes."""

    #     def compute_node(idx: int, prob: float = 1.0):

    #         current_node: int = self.tree_nodes[idx]

    #         if "prob" in current_node.keys():
    #             prob = prob * current_node.get("prob") / 100.0

    #         if current_node.get("type") == "TERMINAL":
    #             current_node["PathProb"] = prob

    #         if current_node.get("type") == "CHANCE":
    #             for idx_next in current_node.get("next"):
    #                 compute_node(idx=idx_next, prob=prob)

    #         if current_node.get("type") == "DECISION":
    #             for i_branch, idx_next in enumerate(current_node.get("next")):
    #                 if i_branch == current_node.get("optimal_branch"):
    #                     compute_node(idx=idx_next, prob=1.0)
    #                 else:
    #                     compute_node(idx=idx_next, prob=0.0)

    #     compute_node(idx=0, prob=1.0)

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
