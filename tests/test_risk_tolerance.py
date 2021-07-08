from smart_choice.decisiontree import DecisionTree
from smart_choice.examples import stguide

from tests.capsys import check_capsys


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
