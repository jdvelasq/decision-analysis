"""
PrecisionTree Oil Example

"""


from _pytest.pytester import LineMatcher
from smart_choice.examples import oil_tree_example


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


#
# ---------------------------------------------------------------------------------------
#
def test_pag32(capsys):
    """Typical risk profile"""
    tree = oil_tree_example()
    tree.evaluate()
    tree.rollback()
    tree.risk_profile(idx=0, cumulative=False, single=False)

    _run_test("./tests/oilexample_pag32.txt", capsys)


def test_pag33(capsys):
    """Typical risk profile"""
    tree = oil_tree_example()
    tree.evaluate()
    tree.rollback()
    tree.display(policy_suggestion=True)

    _run_test("./tests/oilexample_pag33.txt", capsys)


def test_pag34a(capsys):
    """Sensitivity"""
    tree = oil_tree_example()
    print(
        tree.value_sensitivity(
            name="oil_found", branch="large-well", values=(2500, 5000)
        )
    )
    _run_test("./tests/oilexample_pag34a.txt", capsys)


def test_pag34b(capsys):
    """Sensitivity"""
    tree = oil_tree_example()
    print(
        tree.value_sensitivity(
            name="drill_decision", branch="drill", values=(-750, -450)
        )
    )
    _run_test("./tests/oilexample_pag34b.txt", capsys)


def test_pag43(capsys):
    """Basic oil tree example"""

    tree = oil_tree_example()
    tree.evaluate()
    tree.rollback()
    tree.display()

    _run_test("./tests/oilexample_pag43.txt", capsys)


def test_pag56(capsys):
    """Basic oil tree example"""

    tree = oil_tree_example()
    tree.evaluate()
    tree.rollback()
    tree.display(max_deep=3)

    _run_test("./tests/oilexample_pag56.txt", capsys)
