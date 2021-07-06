""""
Test suite for variables
=========================================================================================


"""
from textwrap import dedent

from _pytest.pytester import LineMatcher
from smart_choice.nodes import Nodes


def test_terminal_node_output(capsys):
    """Console output test"""

    expected_text = dedent(
        """
        0  T terminal_node
        """
    )

    def payoff_fn(fnc):
        return fnc

    nodes = Nodes()
    nodes.terminal(name="terminal_node", payoff_fn=payoff_fn)
    print(nodes)

    #
    # Test
    #
    captured_text = capsys.readouterr().out.splitlines()
    captured_text = captured_text[1:]
    captured_text = [text.rstrip() for text in captured_text]
    matcher = LineMatcher(expected_text)
    matcher.fnmatch_lines(captured_text, consecutive=True)


def test_chance_node_output(capsys):
    """Console output test"""

    expected_text = dedent(
        """
        0  C ChanceNode      branch-1   .300 100.00 next-node
                             branch-2   .300 200.00 next-node
                             branch-3   .400 300.00 next-node
        """
    )

    nodes = Nodes()
    nodes.chance(
        name="ChanceNode",
        branches=[
            ("branch-1", 0.30, 100, "next-node"),
            ("branch-2", 0.30, 200, "next-node"),
            ("branch-3", 0.40, 300, "next-node"),
        ],
    )
    print(nodes)

    #
    # Test
    #
    captured_text = capsys.readouterr().out.splitlines()
    captured_text = captured_text[1:]
    captured_text = [text.rstrip() for text in captured_text]
    matcher = LineMatcher(expected_text.splitlines())
    matcher.fnmatch_lines(captured_text, consecutive=True)


def test_decision_node_output(capsys):
    """Console output test"""

    expected_text = dedent(
        """
        0  D DecisionNode    branch-1        100.00 next-node
                             branch-2        200.00 next-node
                             branch-3        300.00 next-node
        """
    )

    nodes = Nodes()
    nodes.decision(
        name="DecisionNode",
        branches=[
            ("branch-1", 100, "next-node"),
            ("branch-2", 200, "next-node"),
            ("branch-3", 300, "next-node"),
        ],
        maximize=True,
    )
    print(nodes)

    #
    # Test
    #
    captured_text = capsys.readouterr().out.splitlines()
    captured_text = captured_text[1:]
    captured_text = [text.rstrip() for text in captured_text]
    matcher = LineMatcher(expected_text.splitlines()[1:])
    matcher.fnmatch_lines(captured_text, consecutive=True)
