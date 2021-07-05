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
        \------[D] #0
                | bid
                |   300.00  -100.00
                +---------------[C] #1
                |                | compbid
                |                | .3500   400.00  -100.00
                |                +---------------------[C] #2
                |                |                      | cost
                |                |                      | .2500   200.00 :   100.00 .0000
                |                |                      | .5000   400.00 :  -100.00 .0000
                |                |                      \ .2500   600.00 :  -300.00 .0000
                |                | compbid
                |                | .5000   600.00  -100.00
                |                +---------------------[C] #6
                |                |                      | cost
                |                |                      | .2500   200.00 :   100.00 .0000
                |                |                      | .5000   400.00 :  -100.00 .0000
                |                |                      \ .2500   600.00 :  -300.00 .0000
                |                | compbid
                |                | .1500   800.00  -100.00
                |                \---------------------[C] #10
                |                                       | cost
                |                                       | .2500   200.00 :   100.00 .0000
                |                                       | .5000   400.00 :  -100.00 .0000
                |                                       \ .2500   600.00 :  -300.00 .0000
                | bid
                >   500.00    65.00
                +---------------[C] #14
                |                | compbid
                |                | .3500   400.00     0.00
                |                +---------------------[C] #15
                |                |                      | cost
                |                |                      | .2500   200.00 :     0.00 .0875
                |                |                      | .5000   400.00 :     0.00 .1750
                |                |                      \ .2500   600.00 :     0.00 .0875
                |                | compbid
                |                | .5000   600.00   100.00
                |                +---------------------[C] #19
                |                |                      | cost
                |                |                      | .2500   200.00 :   300.00 .1250
                |                |                      | .5000   400.00 :   100.00 .2500
                |                |                      \ .2500   600.00 :  -100.00 .1250
                |                | compbid
                |                | .1500   800.00   100.00
                |                \---------------------[C] #23
                |                                       | cost
                |                                       | .2500   200.00 :   300.00 .0375
                |                                       | .5000   400.00 :   100.00 .0750
                |                                       \ .2500   600.00 :  -100.00 .0375
                | bid
                |   700.00    45.00
                +---------------[C] #27
                |                | compbid
                |                | .3500   400.00     0.00
                |                +---------------------[C] #28
                |                |                      | cost
                |                |                      | .2500   200.00 :     0.00 .0000
                |                |                      | .5000   400.00 :     0.00 .0000
                |                |                      \ .2500   600.00 :     0.00 .0000
                |                | compbid
                |                | .5000   600.00     0.00
                |                +---------------------[C] #32
                |                |                      | cost
                |                |                      | .2500   200.00 :     0.00 .0000
                |                |                      | .5000   400.00 :     0.00 .0000
                |                |                      \ .2500   600.00 :     0.00 .0000
                |                | compbid
                |                | .1500   800.00   300.00
                |                \---------------------[C] #36
                |                                       | cost
                |                                       | .2500   200.00 :   500.00 .0000
                |                                       | .5000   400.00 :   300.00 .0000
                |                                       \ .2500   600.00 :   100.00 .0000
                \ no-bid         0.00 :     0.00 .0000
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


def test_fig_3_8_pag55(capsys):
    """Probabilistic Sensitivity"""

    expected_text = dedent(
        r"""
           Branch  Probability  Value
        0     300         0.00 -300.0
        1     300         0.05 -280.0
        2     300         0.10 -260.0
        3     300         0.15 -240.0
        4     300         0.20 -220.0
        ..    ...          ...    ...
        16      0         0.80    0.0
        17      0         0.85    0.0
        18      0         0.90    0.0
        19      0         0.95    0.0
        20      0         1.00    0.0
        
        [84 rows x 3 columns]
        """
    )

    nodes = stbook()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback()
    print(tree.probabilistic_sensitivity(varname="cost"))

    #
    # Test
    #
    captured_text = capsys.readouterr().out.splitlines()
    captured_text = [text.rstrip() for text in captured_text]
    matcher = LineMatcher(expected_text.splitlines()[1:])
    matcher.fnmatch_lines(captured_text, consecutive=True)


def test_fig_5_13_pag114(capsys):
    """Expected utility"""

    expected_text = dedent(
        r"""
        |
        |    57.58
        \------[D] #0
                | bid
                |   300.00  -109.98
                +---------------[C] #1
                |                | compbid
                |                | .3500   400.00  -109.98
                |                +---------------------[C] #2
                |                |                      | cost
                |                |                      | .2500   200.00 :   100.00 .0000
                |                |                      | .5000   400.00 :  -100.00 .0000
                |                |                      \ .2500   600.00 :  -300.00 .0000
                |                | compbid
                |                | .5000   600.00  -109.98
                |                +---------------------[C] #6
                |                |                      | cost
                |                |                      | .2500   200.00 :   100.00 .0000
                |                |                      | .5000   400.00 :  -100.00 .0000
                |                |                      \ .2500   600.00 :  -300.00 .0000
                |                | compbid
                |                | .1500   800.00  -109.98
                |                \---------------------[C] #10
                |                                       | cost
                |                                       | .2500   200.00 :   100.00 .0000
                |                                       | .5000   400.00 :  -100.00 .0000
                |                                       \ .2500   600.00 :  -300.00 .0000
                | bid
                >   500.00    57.58
                +---------------[C] #14
                |                | compbid
                |                | .3500   400.00    -0.00
                |                +---------------------[C] #15
                |                |                      | cost
                |                |                      | .2500   200.00 :    -0.00 .0875
                |                |                      | .5000   400.00 :    -0.00 .1750
                |                |                      \ .2500   600.00 :    -0.00 .0875
                |                | compbid
                |                | .5000   600.00    90.02
                |                +---------------------[C] #19
                |                |                      | cost
                |                |                      | .2500   200.00 :   300.00 .1250
                |                |                      | .5000   400.00 :   100.00 .2500
                |                |                      \ .2500   600.00 :  -100.00 .1250
                |                | compbid
                |                | .1500   800.00    90.02
                |                \---------------------[C] #23
                |                                       | cost
                |                                       | .2500   200.00 :   300.00 .0375
                |                                       | .5000   400.00 :   100.00 .0750
                |                                       \ .2500   600.00 :  -100.00 .0375
                | bid
                |   700.00    38.49
                +---------------[C] #27
                |                | compbid
                |                | .3500   400.00    -0.00
                |                +---------------------[C] #28
                |                |                      | cost
                |                |                      | .2500   200.00 :    -0.00 .0000
                |                |                      | .5000   400.00 :    -0.00 .0000
                |                |                      \ .2500   600.00 :    -0.00 .0000
                |                | compbid
                |                | .5000   600.00    -0.00
                |                +---------------------[C] #32
                |                |                      | cost
                |                |                      | .2500   200.00 :    -0.00 .0000
                |                |                      | .5000   400.00 :    -0.00 .0000
                |                |                      \ .2500   600.00 :    -0.00 .0000
                |                | compbid
                |                | .1500   800.00   290.02
                |                \---------------------[C] #36
                |                                       | cost
                |                                       | .2500   200.00 :   500.00 .0000
                |                                       | .5000   400.00 :   300.00 .0000
                |                                       \ .2500   600.00 :   100.00 .0000
                \ no-bid         0.00 :    -0.00 .0000s
        """
    )

    nodes = stbook()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback(utility_fn="exp", risk_tolerance=1000)
    tree.display(view="ce")

    #
    # Test
    #
    captured_text = capsys.readouterr().out.splitlines()
    captured_text = [text.rstrip() for text in captured_text]
    matcher = LineMatcher(expected_text.splitlines()[1:])
    matcher.fnmatch_lines(captured_text, consecutive=True)
