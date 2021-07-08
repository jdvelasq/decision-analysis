"""
Test suite for the SuperTree book 'Decision Analysis for the Professional'.

"""
from _pytest.pytester import LineMatcher
from smart_choice.decisiontree import DecisionTree
from smart_choice.examples import stbook, stbook_1


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
    matcher.fnmatch_lines(captured_text)


def test_fig_3_7_pag54(capsys):
    """Example creation from Fig. 5.1"""

    nodes = stbook()
    tree = DecisionTree(variables=nodes)
    tree.evaluate()
    tree.rollback()
    tree.display()

    _run_test("./tests/files/stbook_fig_3_7_pag54.txt", capsys)


def test_fig_3_8_pag55(capsys):
    """Probabilistic Sensitivity"""

    nodes = stbook()
    tree = DecisionTree(variables=nodes)
    tree.evaluate()
    tree.rollback()
    sensitivity = tree.probabilistic_sensitivity(varname="cost")
    print(sensitivity.head(21))
    print(sensitivity.tail(63).head(21))
    print(sensitivity.tail(42).head(21))
    print(sensitivity.tail(21))

    _run_test("./tests/files/stbook_fig_3_8_pag55.txt", capsys)


#
#
#
def test_fig_4_5_pag81(capsys):
    """Dependent outcomes"""

    nodes = stbook_1()
    tree = DecisionTree(variables=nodes, initial_variable="bid")

    tree.set_values(nodes=[3, 4, 5, 16, 17, 18, 29, 30, 31], values=[200, 400, 600] * 3)
    tree.set_values(nodes=[7, 8, 9, 20, 21, 22, 33, 34, 35], values=[400, 600, 800] * 3)
    tree.set_values(
        nodes=[11, 12, 13, 24, 25, 26, 37, 38, 39], values=[600, 800, 1000] * 3
    )

    tree.evaluate()
    tree.rollback()
    tree.display()

    _run_test("./tests/files/stbook_fig_4_5_pag81.txt", capsys)


def test_fig_5_11_pag112(capsys):
    """Dependent outcomes"""

    nodes = stbook()
    tree = DecisionTree(variables=nodes, initial_variable="bid")

    tree.evaluate()
    tree.rollback(utility_fn="exp", risk_tolerance=1000)
    tree.display(view="eu")

    _run_test("./tests/files/stbook_fig_5_11_pag112.txt", capsys)


def test_fig_5_13_pag114(capsys):
    """Expected utility"""

    nodes = stbook()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback(utility_fn="exp", risk_tolerance=1000)
    tree.display(view="ce")

    _run_test("./tests/files/stbook_fig_5_13_pag114.txt", capsys)
