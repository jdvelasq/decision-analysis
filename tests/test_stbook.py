"""
Test suite for the SuperTree book 'Decision Analysis for the Professional'.

"""
from textwrap import dedent

from _pytest.pytester import LineMatcher
from smart_choice.decisiontree import DecisionTree
from smart_choice.examples import stbook


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


def test_fig_3_7_pag54(capsys):
    """Example creation from Fig. 5.1"""

    nodes = stbook()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback()
    tree.display()

    _run_test("./tests/stbook_fig_3_7_pag54.txt", capsys)


def test_fig_3_8_pag55(capsys):
    """Probabilistic Sensitivity"""

    nodes = stbook()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback()
    sensitivity = tree.probabilistic_sensitivity(varname="cost")
    print(sensitivity.head(21))
    print(sensitivity.tail(63).head(21))
    print(sensitivity.tail(42).head(21))
    print(sensitivity.tail(21))

    _run_test("./tests/stbook_fig_3_8_pag55.txt", capsys)


#
#
#
def test_fig_4_5_pag81(capsys):
    """Dependent outcomes"""

    nodes = stbook()
    tree = DecisionTree(variables=nodes, initial_variable="bid")

    # changes the order of original nodes in the tree
    bid_ = {"compbid": "cost"}
    compbid_ = {"cost": "profit"}
    cost_ = {"profit": "compbid"}

    tree.change_successor(name="bid", new_successors=bid_)
    tree.change_successor(name="compbid", new_successors=compbid_)
    tree.change_successor(name="cost", new_successors=cost_)
    tree.rebuild()

    tree.set_dependent_outcomes(
        variable="compbid",
        depends_on="cost",
        outcomes={
            "low": [200, 400, 600],
            "medium": [400, 600, 800],
            "high": [600, 800, 1000],
        },
    )

    tree.evaluate()
    tree.rollback()
    tree.display()

    _run_test("./tests/stbook_fig_4_5_pag81.txt", capsys)


def test_fig_5_13_pag114(capsys):
    """Expected utility"""

    nodes = stbook()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback(utility_fn="exp", risk_tolerance=1000)
    tree.display(view="ce")

    _run_test("./tests/stbook_fig_5_13_pag114.txt", capsys)
