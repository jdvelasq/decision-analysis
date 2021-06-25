"""
Variables
-------------------------------------------------------------------------------
"""

from typing import Any, List


class Nodes:
    """
    Create a list of variables conformint the tree.

    """

    def __init__(self):
        self.data = {}

    def __getitem__(self, name: str) -> dict:
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

    def decision(self, name: str, branches: List[tuple], max_: bool = False) -> None:
        self.data[name] = {
            "type": "DECISION",
            "branches": branches,
            "max_": max_,
        }
