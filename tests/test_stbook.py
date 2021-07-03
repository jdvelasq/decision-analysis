"""
Test suite for the SuperTree book 'Decision Analysis for the Professional'.

"""
from textwrap import dedent

from _pytest.pytester import LineMatcher
from dmak.decisiontree import DecisionTree
from dmak.examples import stbook


def test_fig_3_7_pag54(capsys):
    """Example creation from Fig. 5.1"""

    expected_text = dedent(
        r"""
        |
        |    65.00
        \------[D]
                | bid
                |   300.00  -100.00
                +---------------[C]
                |                | compbid
                |                | .350   400.00  -100.00
                |                +--------------------[C]
                |                |                     | cost
                |                |                     | .250   200.00 :   100.00 .000
                |                |                     | .500   400.00 :  -100.00 .000
                |                |                     \ .250   600.00 :  -300.00 .000
                |                | compbid
                |                | .500   600.00  -100.00
                |                +--------------------[C]
                |                |                     | cost
                |                |                     | .250   200.00 :   100.00 .000
                |                |                     | .500   400.00 :  -100.00 .000
                |                |                     \ .250   600.00 :  -300.00 .000
                |                | compbid
                |                | .150   800.00  -100.00
                |                \--------------------[C]
                |                                      | cost
                |                                      | .250   200.00 :   100.00 .000
                |                                      | .500   400.00 :  -100.00 .000
                |                                      \ .250   600.00 :  -300.00 .000
                | bid
                >   500.00    65.00
                +---------------[C]
                |                | compbid
                |                | .350   400.00     0.00
                |                +--------------------[C]
                |                |                     | cost
                |                |                     | .250   200.00 :     0.00 .087
                |                |                     | .500   400.00 :     0.00 .175
                |                |                     \ .250   600.00 :     0.00 .087
                |                | compbid
                |                | .500   600.00   100.00
                |                +--------------------[C]
                |                |                     | cost
                |                |                     | .250   200.00 :   300.00 .125
                |                |                     | .500   400.00 :   100.00 .250
                |                |                     \ .250   600.00 :  -100.00 .125
                |                | compbid
                |                | .150   800.00   100.00
                |                \--------------------[C]
                |                                      | cost
                |                                      | .250   200.00 :   300.00 .037
                |                                      | .500   400.00 :   100.00 .075
                |                                      \ .250   600.00 :  -100.00 .037
                | bid
                |   700.00    45.00
                +---------------[C]
                |                | compbid
                |                | .350   400.00     0.00
                |                +--------------------[C]
                |                |                     | cost
                |                |                     | .250   200.00 :     0.00 .000
                |                |                     | .500   400.00 :     0.00 .000
                |                |                     \ .250   600.00 :     0.00 .000
                |                | compbid
                |                | .500   600.00     0.00
                |                +--------------------[C]
                |                |                     | cost
                |                |                     | .250   200.00 :     0.00 .000
                |                |                     | .500   400.00 :     0.00 .000
                |                |                     \ .250   600.00 :     0.00 .000
                |                | compbid
                |                | .150   800.00   300.00
                |                \--------------------[C]
                |                                      | cost
                |                                      | .250   200.00 :   500.00 .000
                |                                      | .500   400.00 :   300.00 .000
                |                                      \ .250   600.00 :   100.00 .000
                \ no-bid         0.00 :     0.00 .000
        """
    )

    nodes = stbook()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback()
    tree.display()

    #
    # Test
    #
    captured_text = capsys.readouterr().out.splitlines()
    captured_text = [text.rstrip() for text in captured_text]
    matcher = LineMatcher(expected_text.splitlines()[1:])
    matcher.fnmatch_lines(captured_text, consecutive=True)
