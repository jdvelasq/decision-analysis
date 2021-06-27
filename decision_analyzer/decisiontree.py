"""
Decision Tree Model
===============================================================================

**Node Creation**


"""

from typing import List


class DecisionTree:
    """Decision Tree Model"""

    def __init__(self, variables: List, initial_variable: str) -> None:
        self.tree_nodes = None
        self.variables = variables
        self.initial_variable = initial_variable

    def _build_skeleton(self) -> None:
        #
        def build_tree_node(current_variable: str) -> int:

            # position of the variable in the table of nodes
            current_idx = len(self.tree_nodes)

            # adds the new node
            self.tree_nodes.append(
                {
                    "idx": current_idx,
                    "name": current_variable,
                    "next_idx": None,
                }
            )

            # adds branch nodes
            if "branches" in self.variables[current_variable].keys():

                next_idx = []

                for branch in self.variables[current_variable].get("branches"):

                    # The last position of each branch in a variable contains
                    # the name of the next variable (type)
                    branch_idx: int = build_tree_node(current_variable=branch[-1])
                    next_idx.append(branch_idx)

                self.tree_nodes[current_idx]["next_idx"] = next_idx

            return current_idx

        self.tree_nodes: List = []
        build_tree_node(current_variable=self.initial_variable)

    def _get_node_type(self, name: str = None, idx: int = None) -> str:
        #
        # Gets the node type ("TERMINAL", "CHANCE", "DECISION") from
        # table of variables
        #
        if idx is not None:
            name = self.tree_nodes[idx].get("name")
        return self.variables[name].get("type")

    def _get_next_idx(self, idx: int = None) -> List:
        return self.tree_nodes[idx].get("next_idx")

    def _set_tags(self) -> None:
        #
        # Fills the brancbes with the tags
        #
        for node in self.tree_nodes:
            name = node.get("name")
            next_idx = node.get("next_idx")
            if next_idx is not None:
                for idx in next_idx:
                    self.tree_nodes[idx]["tag"] = name

    def _set_value_tags(self) -> None:
        #
        # Fills the nodes with the values assosiated to the tags
        #
        for node in self.tree_nodes:

            name = node.get("name")
            next_idx = node.get("next_idx")

            if next_idx is not None:

                type_ = self._get_node_type(name=name)
                var_branches = self.variables[name].get("branches")

                if type_ == "DECISION":
                    values = [value for value, _ in var_branches]

                if type_ == "CHANCE":
                    values = [value for _, value, _ in var_branches]

                for idx, value in zip(next_idx, values):
                    self.tree_nodes[idx]["value"] = value

    def _set_prob_tags(self) -> None:
        #
        # Fills the nodes with the probabilities assosiated to the tags
        #
        for node in self.tree_nodes:

            name = node.get("name")

            if self._get_node_type(name=name) == "CHANCE":

                var_branches = self.variables[name].get("branches")
                probs = [prob for prob, _, _ in var_branches]
                next_idx = node.get("next_idx")

                for idx, prob in zip(next_idx, probs):
                    self.tree_nodes[idx]["prob"] = prob

    def build(self):
        """This function is used to build the decision tree using the information in the
        variables.
        """

        self._build_skeleton()
        self._set_tags()
        self._set_value_tags()
        self._set_prob_tags()

    def export_text(self):
        """Exports the tree as text diagram."""

        def print_node(idx: int, is_last_node: bool) -> List:
            #
            def node_number():
                text.append("| #{}".format(idx))

            def tag():
                if "tag" in self.tree_nodes[idx].keys():
                    text.append(
                        "| {}={}".format(
                            self.tree_nodes[idx].get("tag"),
                            self.tree_nodes[idx].get("value"),
                        )
                    )

            def prob():
                if "prob" in self.tree_nodes[idx].keys():
                    text.append(
                        "| Prob={:5.2f}".format(
                            self.tree_nodes[idx].get("prob"),
                        )
                    )

            def node_type():
                type_ = self._get_node_type(idx=idx)
                if type_ == "DECISION":
                    if is_last_node is True:
                        text.append("\\-------[D]")
                    else:
                        text.append("+-------[D]")

                if type_ == "CHANCE":
                    if is_last_node is True:
                        text.append("\\-------[C]")
                    else:
                        text.append("+-------[C]")

                if type_ == "TERMINAL":
                    name = self.tree_nodes[idx].get("name")
                    if is_last_node is True:
                        text.append("\\-------[T] {}".format(name))
                    else:
                        text.append("+-------[T] {}".format(name))

            def node_branches():
                next_nodes = self.tree_nodes[idx].get("next_idx")
                if next_nodes is not None:
                    for i_next_idx, next_idx in enumerate(next_nodes):

                        if i_next_idx + 1 == len(next_nodes):
                            next_is_last_node = True
                        else:
                            next_is_last_node = False

                        result = print_node(next_idx, next_is_last_node)

                        for t_ in result:
                            if is_last_node is True:
                                text.append(" " * 9 + t_)
                            else:
                                if t_[0] == "+":
                                    text.append("|" + " " * 8 + t_)
                                else:
                                    text.append("|" + " " * 8 + "|" + t_[1:])

            text = ["|"]
            node_number()
            tag()
            prob()
            node_type()
            node_branches()

            return text

        text = []

        text.extend(print_node(idx=0, is_last_node=True))

        return "\n".join(text)

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

    def _build_user_fn_args(self) -> None:
        def set_fn_args(idx: int, args: dict) -> None:

            type_ = self._get_node_type(idx=idx)

            if type_ == "TERMINAL":
                self.tree_nodes[idx]["user_args"] = args
                return

            #
            # collecte the values of the branches
            #
            name = self.tree_nodes[idx].get("name")
            var_branches = self.variables[name].get("branches")

            if type_ == "DECISION":
                values = [value for value, _ in var_branches]

            if type_ == "CHANCE":
                values = [value for _, value, _ in var_branches]

            #
            # Fills the next node with value of the current branch
            #
            node_branches = self._get_next_idx(idx=idx)
            if node_branches is not None:
                for next_idx, value in zip(node_branches, values):
                    new_args = args.copy()
                    new_args = {**new_args, **{name: value}}
                    set_fn_args(idx=next_idx, args=new_args)

        set_fn_args(idx=0, args={})

    def _evaluate_terminal_nodes(self) -> None:
        #
        def cumulative(**kwargs):
            return sum(v for _, v in kwargs.items())

        #
        for node in self.tree_nodes:
            name = node.get("name")
            type_ = self._get_node_type(name=name)
            if type_ == "TERMINAL":
                user_fn = self.variables[name].get("user_fn")
                if user_fn is None:
                    user_fn = cumulative
                user_args = node.get("user_args")
                node["ExpVal"] = user_fn(**user_args)

    def evaluate_tree(self):
        """This function is used to build the decision tree using the information in the
        variables.
        """

        self._build_user_fn_args()
        self._evaluate_terminal_nodes()

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
