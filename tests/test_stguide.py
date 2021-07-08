"""
Test suite for the SuperTree user guide simple bid example.

"""

from textwrap import dedent

from _pytest.pytester import LineMatcher

from smart_choice.decisiontree import DecisionTree
from smart_choice.examples import (
    stguide,
    stguide_dependent_probabilities,
    stguide_dependent_outcomes,
)


def _get_matcher(filename):
    with open(filename, "r") as file:
        expected_text = file.readlines()
    expected_text = [line.replace("\n", "") for line in expected_text]
    matcher = LineMatcher(expected_text)
    return matcher


def _get_captured_text(capsys):
    captured_text = capsys.readouterr().out.splitlines()
    # captured_text = captured_text[1:]
    captured_text = [text.rstrip() for text in captured_text]
    return captured_text


def _run_test(filename, capsys):
    matcher = _get_matcher(filename)
    captured_text = _get_captured_text(capsys)
    matcher.fnmatch_lines(captured_text, consecutive=True)


def test_fig_5_8a(capsys):
    """Fig. 5.8 (a) --- Plot distribution"""

    nodes = stguide()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback()
    tree.risk_profile(idx=0, cumulative=False, single=True)

    _run_test("./tests/stguide_fig_5_8a.txt", capsys)


def test_fig_5_8b(capsys):
    """Fig. 5.8 (b) --- Plot distribution"""

    nodes = stguide()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback()
    tree.risk_profile(idx=0, cumulative=True, single=True)

    _run_test("./tests/stguide_fig_5_8b.txt", capsys)


def test_fig_5_8c(capsys):
    """Fig. 5.8 (c) --- Plot distribution"""

    nodes = stguide()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback()
    tree.risk_profile(idx=0, cumulative=False, single=False)

    _run_test("./tests/stguide_fig_5_8b.txt", capsys)


def test_fig_5_10(capsys):
    """Fig. 5.10 --- Cumulative plot distribution"""

    nodes = stguide()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback()
    tree.risk_profile(idx=0, cumulative=True, single=False)

    _run_test("./tests/stguide_fig_5_10.txt", capsys)


def test_fig_7_3a(capsys):
    """Change probabilities"""

    nodes = stguide_dependent_probabilities()
    print(nodes)
    _run_test("./tests/stguide_fig_7_3a.txt", capsys)


def test_fig_7_3b(capsys):
    """Change probabilities"""

    nodes = stguide_dependent_probabilities()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    print(tree)

    _run_test("./tests/stguide_fig_7_3b.txt", capsys)


def test_fig_7_6a(capsys):
    """Dependent outcomes"""

    nodes = stguide_dependent_outcomes()
    print(nodes)
    _run_test("./tests/stguide_fig_7_6a.txt", capsys)


def test_fig_7_6b(capsys):
    """Dependent outcomes"""

    nodes = stguide_dependent_outcomes()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    print(tree)

    _run_test("./tests/stguide_fig_7_6b.txt", capsys)


def test_fig_7_14(capsys):
    """Node reordering: add new nodes to the tree data"""
    nodes = stguide()
    tree = DecisionTree(variables=nodes, initial_variable="compbid-1")
    tree.evaluate()
    tree.rollback()
    tree.display()
    _run_test("./tests/stguide_fig_7_14.txt", capsys)


def test_fig_7_15(capsys):
    """Fig. 7.15 --- Plot distribution"""

    expected_text = dedent(
        r"""
                  Label  Value  Cumulative Probability
        0  800;EV=300.0    100                    0.25
        1  800;EV=300.0    300                    0.75
        2  800;EV=300.0    500                    1.00
        """
    )

    nodes = stguide()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback()
    tree.risk_profile(idx=23, cumulative=True, single=True)

    #
    # Test
    #
    captured_text = capsys.readouterr().out.splitlines()
    captured_text = [text.rstrip() for text in captured_text]
    matcher = LineMatcher(expected_text.splitlines()[1:])
    matcher.fnmatch_lines(captured_text, consecutive=True)


def test_fig_7_17(capsys):
    """Fig. 7.17 --- Probabilistic Sensitivity"""

    expected_text = dedent(
        r"""
           Branch  Probability  Value
        0     500         0.00  -65.0
        1     500         0.05  -52.0
        2     500         0.10  -39.0
        3     500         0.15  -26.0
        4     500         0.20  -13.0
        5     500         0.25    0.0
        6     500         0.30   13.0
        7     500         0.35   26.0
        8     500         0.40   39.0
        9     500         0.45   52.0
        10    500         0.50   65.0
        11    500         0.55   78.0
        12    500         0.60   91.0
        13    500         0.65  104.0
        14    500         0.70  117.0
        15    500         0.75  130.0
        16    500         0.80  143.0
        17    500         0.85  156.0
        18    500         0.90  169.0
        19    500         0.95  182.0
        20    500         1.00  195.0
        0     700         0.00   15.0
        1     700         0.05   18.0
        2     700         0.10   21.0
        3     700         0.15   24.0
        4     700         0.20   27.0
        5     700         0.25   30.0
        6     700         0.30   33.0
        7     700         0.35   36.0
        8     700         0.40   39.0
        9     700         0.45   42.0
        10    700         0.50   45.0
        11    700         0.55   48.0
        12    700         0.60   51.0
        13    700         0.65   54.0
        14    700         0.70   57.0
        15    700         0.75   60.0
        16    700         0.80   63.0
        17    700         0.85   66.0
        18    700         0.90   69.0
        19    700         0.95   72.0
        20    700         1.00   75.0
        """
    )

    nodes = stguide()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback()
    tree.probabilistic_sensitivity(varname="cost")

    #
    # Test
    #
    captured_text = capsys.readouterr().out.splitlines()
    captured_text = [text.rstrip() for text in captured_text]
    matcher = LineMatcher(expected_text.splitlines()[1:])
    matcher.fnmatch_lines(captured_text, consecutive=True)


def test_fig_7_19(capsys):
    """Fig. 7.19 --- Risk Tolerance"""

    expected_text = dedent(
        r"""
                  500        700 Risk Tolerance
        0   65.000000  45.000000       Infinity
        1   55.205969  36.620035            750
        2   46.192925  30.328977            375
        3   37.932689  25.563104            250
        4   30.369424  21.903377            187
        5   23.435045  19.048741            150
        6   17.059969  16.785671            125
        7   11.179425  14.962826            107
        8    5.736366  13.472262             94
        9    0.682183  12.236194             83
        10  -4.023832  11.197883             75
        """
    )

    nodes = stguide()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback()
    tree.risk_sensitivity(utility_fn="exp", risk_tolerance=75)

    #
    # Test
    #
    captured_text = capsys.readouterr().out.splitlines()
    captured_text = [text.rstrip() for text in captured_text]
    matcher = LineMatcher(expected_text.splitlines()[1:])
    matcher.fnmatch_lines(captured_text, consecutive=True)
