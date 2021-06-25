"""

DecisionTree

"""
from typing import List

# from pydecisiontree.nodes import Nodes


class DecisionTree:
    """Decision Tree Model"""

    def __init__(self):
        self.tree_nodes = None

    def build_skeleton(self, initial_variable: str, variables: dict) -> None:
        """Skeleton"""

        def build_tree_node(current_variable: str) -> int:
            current_id = len(self.tree_nodes)
            self.tree_nodes.append(
                {
                    "id": current_id,
                    "name": current_variable,
                    "next": None,
                }
            )
            if "branches" in variables[current_variable].keys():
                next_tree_nodes = []
                for branch in variables[current_variable].get("branches"):
                    branch_id: int = build_tree_node(current_variable=branch[-1])
                    next_tree_nodes.append(branch_id)
                self.tree_nodes[current_id]["next"] = next_tree_nodes

            return current_id

        #
        #
        self.tree_nodes: List = []
        build_tree_node(current_variable=initial_variable)

    def fill_node_properties(self, variables: dict) -> None:
        """FIll the tree with run properties"""

        for node in self.tree_nodes:

            var = variables[node["name"]]
            if var.get("type") == "DECISION":
                for idx, branch in zip(node.get("next"), var.get("branches")):
                    self.tree_nodes[idx]["arg"] = {node["name"]: branch[0]}

            if var.get("type") == "CHANCE":
                for idx, branch in zip(node.get("next"), var.get("branches")):
                    self.tree_nodes[idx]["prob"] = branch[0]
                    self.tree_nodes[idx]["arg"] = {node["name"]: branch[1]}

            if var.get("type") == "TERMNAL":
                node["user_fn"] = var.get("expr")

    def prepare_user_fn_args(self):
        """.

        Fist part of evaluation algorithm.


        """
        for node in self.tree_nodes:

            if node.get("next") is None:
                continue

            arg = {} if "arg" not in node.keys() else node.get("arg")

            for idx in node.get("next"):
                self.tree_nodes[idx]["user_fn_args"] = {
                    **arg,
                    **self.tree_nodes[idx].get("arg"),
                }


    def compute_user_fn(self):

        

    #
    # Debug
    #
    # def _build_tree(self, root_node: str) -> None:

    #     self.tree = []

    #     _, this_branch = new_branch()
    #     set_branch_data(
    #         this_branch=this_branch, this_node=self.data[0], path=path.copy()
    #     )

    # def new_branch():
    #     self.branches.append(
    #         {
    #             "ExpVal": None,
    #             "sel_strategy": None,
    #             "id": len(self.branches),
    #         }
    #     )
    #     return (len(self.branches) - 1, self.branches[-1])

    # #
    # #
    # # OLD CODE
    # #
    # #

    # def build_tree_(self) -> None:
    #     """Builds the decision tree using the information in the variables."""

    #     def get_current_branch(id):
    #         for var_id, var_branch in self.stack:
    #             if var_id == id:
    #                 return var_branch
    #         return None

    #     def find_value(data):
    #         if isinstance(data, tuple):
    #             id, values = data
    #             return find_value(values[get_current_branch(id)])
    #         return data

    #     # def new_branch():
    #     #     self.tree.append(
    #     #         {
    #     #             "ExpVal": None,
    #     #             "sel_strategy": None,
    #     #             "id": len(self.tree),
    #     #         }
    #     #     )
    #     #     return (len(self.tree) - 1, self.tree[-1])

    #     def set_branch_data(this_branch, this_node, path):
    #         def set_terminal():
    #             this_branch["type"] = this_node.get("type")
    #             if this_branch.get("ignore", True) is False:
    #                 path.append(this_branch.get("tag"))
    #             this_branch["expr"] = (
    #                 "+".join(path)
    #                 if this_node.get("expr") is None
    #                 else this_node.get("expr")
    #             )

    #         def set_decision():
    #             #
    #             this_branch["type"] = this_node.get("type")
    #             this_branch["forced_branch_idx"] = None
    #             this_branch["next_branches"] = []
    #             this_branch["max"] = this_node.get("max")
    #             if this_branch.get("ignore", True) is False:
    #                 path.append(this_branch.get("tag"))
    #             #
    #             for idx, (value, next_node) in enumerate(this_node.get("branches")):
    #                 #
    #                 self.stack.append((this_node["id"], idx))
    #                 #
    #                 next_branch_id, next_branch = new_branch()
    #                 this_branch["next_branches"].append(next_branch_id)
    #                 next_branch["ignore"] = this_node.get("ignore")
    #                 next_branch["tag"] = this_node.get("tag")
    #                 next_branch["value"] = find_value(value)
    #                 #
    #                 set_branch_data(
    #                     this_branch=next_branch,
    #                     this_node=self.data[next_node],
    #                     path=path.copy(),
    #                 )
    #                 #
    #                 self.stack.pop()

    #         def set_chance():

    #             this_branch["type"] = this_node.get("type")
    #             this_branch["forced_branch_idx"] = None
    #             this_branch["next_branches"] = []
    #             if this_branch.get("ignore", True) is False:
    #                 path.append(this_branch.get("tag"))

    #             for idx, (prob, value, next_node) in enumerate(
    #                 this_node.get("branches")
    #             ):

    #                 self.stack.append((this_node["id"], idx))

    #                 next_branch_id, next_branch = new_branch()
    #                 this_branch["next_branches"].append(next_branch_id)
    #                 next_branch["ignore"] = this_node.get("ignore")
    #                 next_branch["tag"] = this_node.get("tag")
    #                 next_branch["value"] = find_value(value)
    #                 next_branch["prob"] = find_value(prob)

    #                 set_branch_data(
    #                     this_branch=next_branch,
    #                     this_node=self.data[next_node],
    #                     path=path.copy(),
    #                 )

    #                 self.stack.pop()

    #         ####
    #         # if this_node.get("type") == "DECISION":
    #             set_decision()
    #         elif this_node.get("type") == "CHANCE":
    #             set_chance()
    #         elif this_node.get("type") == "TERMINAL":
    #             set_terminal()
    #         else:
    #             pass

    #     ###
    #     self.stack = []
    #     self.tree = []
    #     path = []
    #     _, this_branch = new_branch()
    #     set_branch_data(
    #         this_branch=this_branch, this_node=self.data[0], path=path.copy()
    #     )
    #     del self.stack
