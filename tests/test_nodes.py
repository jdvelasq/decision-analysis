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
        0  C ChanceNode      .3000 100             next-node
                             .3000 200             next-node
                             .4000 last-branch     next-node
        """
    )

    nodes = Nodes()
    nodes.chance(
        name="ChanceNode",
        branches=[
            (0.30, 100, "next-node"),
            (0.30, 200, "next-node"),
            (0.40, "last-branch", "next-node"),
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
        0  D DecisionNode          100             next-node
                                   200             next-node
                                   branch-4        next-node
        """
    )

    nodes = Nodes()
    nodes.decision(
        name="DecisionNode",
        branches=[
            (100, "next-node"),
            (200, "next-node"),
            ("branch-4", "next-node"),
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
