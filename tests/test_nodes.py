""""
Test suite for variables
=========================================================================================


"""
from textwrap import dedent

from _pytest.pytester import LineMatcher
from dmak.nodes import Nodes


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
        0  C ChanceNode      100                  .333 100.00 next-node
                             branch-1             .333 200.00 next-node
                             a very very long...  .333 300.00 next-node
        """
    )

    nodes = Nodes()
    nodes.chance(
        name="ChanceNode",
        branches=[
            (0.30, 100, "next-node"),
            ("branch-1", 0.30, 200, "next-node"),
            ("a very very long name", 0.30, 300, "next-node"),
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
        0  D DecisionNode... 100                   100.00 next-node
                             branch-1              200.00 next-node
                             a long long very...   400.00 next-node
        """
    )

    nodes = Nodes()
    nodes.decision(
        name="DecisionNode",
        branches=[
            (100, "next-node"),
            ("branch-1", 200, "next-node"),
            ("a long long very long name", 400, "next-node"),
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
