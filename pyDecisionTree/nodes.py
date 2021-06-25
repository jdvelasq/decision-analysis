"""
Variables
-------------------------------------------------------------------------------
"""

from typing import Any, List, Tuple


# class Variable(dict):
#     """dot.notation access to dictionary attributes"""

#     __getattr__ = dict.get
#     __setattr__ = dict.__setitem__
#     __delattr__ = dict.__delitem__


class Nodes:
    def __init__(self):
        self.data = {}

    def __getitem__(self, name: str) -> dict:
        """
        Returns a variable

        """
        return self.data[name]

    def terminal(self, name: str, expr: Any) -> None:
        self.data[name] = {
            "type": "TERMINAL",
            "expr": expr,
        }

    def chance(self, name: str, branches: List[tuple]) -> None:

        self.data[name] = {
            "type": "CHANCE",
            "branches": branches,
        }
