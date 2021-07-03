"""
PrecisionTree Oil Example

"""
from textwrap import dedent

from _pytest.pytester import LineMatcher
from dmak.decisiontree import DecisionTree
from dmak.examples import oilexample


def test_pag43(capsys):
    """Basic oil tree example"""

    expected_text = dedent(
        r"""

        """
    )

    nodes = oilexample()
    tree = DecisionTree(variables=nodes, initial_variable="test_decision")
    # tree.evaluate()
    # tree.rollback(utility_fn="exp", risk_tolerance=1000)
    tree.display()

    #
    # Test
    #
    captured_text = capsys.readouterr().out.splitlines()
    captured_text = [text.rstrip() for text in captured_text]
    matcher = LineMatcher(expected_text.splitlines()[1:])
    matcher.fnmatch_lines(captured_text, consecutive=True)
