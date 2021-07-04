"""
Test suite for the SuperTree user guide simple bid example.

"""

from textwrap import dedent

from _pytest.pytester import LineMatcher
from dmak.decisiontree import DecisionTree
from dmak.examples import stguide


def test_fig_5_1(capsys):
    """Example creation from Fig. 5.1"""

    expected_text = dedent(
        r"""
        |
        |
        \---[D] #0
             | bid
             |   500.00
             +------[C] #1
             |       | compbid
             |       | .3500   400.00
             |       +------------[C] #2
             |       |             | cost
             |       |             | .2500   200.00
             |       |             | .5000   400.00
             |       |             \ .2500   600.00
             |       | compbid
             |       | .5000   600.00
             |       +------------[C] #6
             |       |             | cost
             |       |             | .2500   200.00
             |       |             | .5000   400.00
             |       |             \ .2500   600.00
             |       | compbid
             |       | .1500   800.00
             |       \------------[C] #10
             |                     | cost
             |                     | .2500   200.00
             |                     | .5000   400.00
             |                     \ .2500   600.00
             | bid
             |   700.00
             \------[C] #14
                     | compbid
                     | .3500   400.00
                     +------------[C] #15
                     |             | cost
                     |             | .2500   200.00
                     |             | .5000   400.00
                     |             \ .2500   600.00
                     | compbid
                     | .5000   600.00
                     +------------[C] #19
                     |             | cost
                     |             | .2500   200.00
                     |             | .5000   400.00
                     |             \ .2500   600.00
                     | compbid
                     | .1500   800.00
                     \------------[C] #23
                                   | cost
                                   | .2500   200.00
                                   | .5000   400.00
                                   \ .2500   600.00

        """
    )

    nodes = stguide()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.display()

    #
    # Test
    #
    captured_text = capsys.readouterr().out.splitlines()
    captured_text = [text.rstrip() for text in captured_text]
    matcher = LineMatcher(expected_text.splitlines()[1:])
    matcher.fnmatch_lines(captured_text, consecutive=True)


def test_fit_5_4(capsys):
    """Example creatioin from Fig. 5.4"""

    expected_text = dedent(
        """
        STRUCTURE    NAMES    OUTCOMES     PROBABILIES
        ------------------------------------------------------
        0D1 14       bid      500 700
        1C2 6 10     compbid  400 600 800  .3500 .5000 .1500
        2C3 4 5      cost     200 400 600  .2500 .5000 .2500
        3T           profit
        4T           profit
        5T           profit
        6C7 8 9      cost     200 400 600  .2500 .5000 .2500
        7T           profit
        8T           profit
        9T           profit
        10C11 12 13  cost     200 400 600  .2500 .5000 .2500
        11T          profit
        12T          profit
        13T          profit
        14C15 19 23  compbid  400 600 800  .3500 .5000 .1500
        15C16 17 18  cost     200 400 600  .2500 .5000 .2500
        16T          profit
        17T          profit
        18T          profit
        19C20 21 22  cost     200 400 600  .2500 .5000 .2500
        20T          profit
        21T          profit
        22T          profit
        23C24 25 26  cost     200 400 600  .2500 .5000 .2500
        24T          profit
        25T          profit
        26T          profit
        """
    )

    nodes = stguide()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    print(tree)

    #
    # Test
    #
    captured_text = capsys.readouterr().out.splitlines()
    captured_text = captured_text[1:]
    captured_text = [text.rstrip() for text in captured_text]
    matcher = LineMatcher(expected_text.splitlines()[1:])
    matcher.fnmatch_lines(captured_text, consecutive=True)


def test_fig_5_6a(capsys):
    """Fig. 5.6 (a) --- Evaluation of terminal nodes"""

    expected_text = dedent(
        r"""
        |
        |
        \---[D] #0
             | bid
             |   500.00
             +------[C] #1
             |       | compbid
             |       | .3500   400.00
             |       +------------[C] #2
             |       |             | cost
             |       |             | .2500   200.00 :     0.00
             |       |             | .5000   400.00 :     0.00
             |       |             \ .2500   600.00 :     0.00
             |       | compbid
             |       | .5000   600.00
             |       +------------[C] #6
             |       |             | cost
             |       |             | .2500   200.00 :   300.00
             |       |             | .5000   400.00 :   100.00
             |       |             \ .2500   600.00 :  -100.00
             |       | compbid
             |       | .1500   800.00
             |       \------------[C] #10
             |                     | cost
             |                     | .2500   200.00 :   300.00
             |                     | .5000   400.00 :   100.00
             |                     \ .2500   600.00 :  -100.00
             | bid
             |   700.00
             \------[C] #14
                     | compbid
                     | .3500   400.00
                     +------------[C] #15
                     |             | cost
                     |             | .2500   200.00 :     0.00
                     |             | .5000   400.00 :     0.00
                     |             \ .2500   600.00 :     0.00
                     | compbid
                     | .5000   600.00
                     +------------[C] #19
                     |             | cost
                     |             | .2500   200.00 :     0.00
                     |             | .5000   400.00 :     0.00
                     |             \ .2500   600.00 :     0.00
                     | compbid
                     | .1500   800.00
                     \------------[C] #23
                                   | cost
                                   | .2500   200.00 :   500.00
                                   | .5000   400.00 :   300.00
                                   \ .2500   600.00 :   100.00

        """
    )

    nodes = stguide()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.display()

    #
    # Test
    #
    captured_text = capsys.readouterr().out.splitlines()
    captured_text = [text.rstrip() for text in captured_text]
    matcher = LineMatcher(expected_text.splitlines()[1:])
    matcher.fnmatch_lines(captured_text, consecutive=True)


def test_fig_5_6b(capsys):
    """Fig. 5.6 (b) --- Expected Values"""

    expected_text = dedent(
        r"""
        |
        |    65.00
        \------[D] #0
                | bid
                >   500.00    65.00
                +---------------[C] #1
                |                | compbid
                |                | .3500   400.00     0.00
                |                +---------------------[C] #2
                |                |                      | cost
                |                |                      | .2500   200.00 :     0.00 .0875
                |                |                      | .5000   400.00 :     0.00 .1750
                |                |                      \ .2500   600.00 :     0.00 .0875
                |                | compbid
                |                | .5000   600.00   100.00
                |                +---------------------[C] #6
                |                |                      | cost
                |                |                      | .2500   200.00 :   300.00 .1250
                |                |                      | .5000   400.00 :   100.00 .2500
                |                |                      \ .2500   600.00 :  -100.00 .1250
                |                | compbid
                |                | .1500   800.00   100.00
                |                \---------------------[C] #10
                |                                       | cost
                |                                       | .2500   200.00 :   300.00 .0375
                |                                       | .5000   400.00 :   100.00 .0750
                |                                       \ .2500   600.00 :  -100.00 .0375
                | bid
                |   700.00    45.00
                \---------------[C] #14
                                 | compbid
                                 | .3500   400.00     0.00
                                 +---------------------[C] #15
                                 |                      | cost
                                 |                      | .2500   200.00 :     0.00 .0000
                                 |                      | .5000   400.00 :     0.00 .0000
                                 |                      \ .2500   600.00 :     0.00 .0000
                                 | compbid
                                 | .5000   600.00     0.00
                                 +---------------------[C] #19
                                 |                      | cost
                                 |                      | .2500   200.00 :     0.00 .0000
                                 |                      | .5000   400.00 :     0.00 .0000
                                 |                      \ .2500   600.00 :     0.00 .0000
                                 | compbid
                                 | .1500   800.00   300.00
                                 \---------------------[C] #23
                                                        | cost
                                                        | .2500   200.00 :   500.00 .0000
                                                        | .5000   400.00 :   300.00 .0000
                                                        \ .2500   600.00 :   100.00 .0000
        
        """
    )

    nodes = stguide()
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


def test_fig_5_8a(capsys):
    """Fig. 5.8 (a) --- Plot distribution"""

    expected_text = dedent(
        r"""
             Label  Value  Probability
        0  EV=65.0   -100       0.1625
        1  EV=65.0      0       0.3500
        2  EV=65.0    100       0.3250
        3  EV=65.0    300       0.1625
        """
    )

    nodes = stguide()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback()
    tree.risk_profile(idx=0, cumulative=False, single=True)

    #
    # Test
    #
    captured_text = capsys.readouterr().out.splitlines()
    captured_text = [text.rstrip() for text in captured_text]
    matcher = LineMatcher(expected_text.splitlines()[1:])
    matcher.fnmatch_lines(captured_text, consecutive=True)


def test_fig_5_8b(capsys):
    """Fig. 5.8 (b) --- Plot distribution"""

    expected_text = dedent(
        r"""
             Label  Value  Cumulative Probability
        0  EV=65.0   -100                  0.1625
        1  EV=65.0      0                  0.5125
        2  EV=65.0    100                  0.8375
        3  EV=65.0    300                  1.0000
        """
    )

    nodes = stguide()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback()
    tree.risk_profile(idx=0, cumulative=True, single=True)

    #
    # Test
    #
    captured_text = capsys.readouterr().out.splitlines()
    captured_text = [text.rstrip() for text in captured_text]
    matcher = LineMatcher(expected_text.splitlines()[1:])
    matcher.fnmatch_lines(captured_text, consecutive=True)


def test_fig_5_8c(capsys):
    """Fig. 5.8 (c) --- Plot distribution"""

    expected_text = dedent(
        r"""
                 Label  Value  Probability
        0  500;EV=65.0   -100       0.1625
        1  500;EV=65.0      0       0.3500
        2  500;EV=65.0    100       0.3250
        3  500;EV=65.0    300       0.1625
        0  700;EV=45.0      0       0.8500
        1  700;EV=45.0    100       0.0375
        2  700;EV=45.0    300       0.0750
        3  700;EV=45.0    500       0.0375
        """
    )

    nodes = stguide()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback()
    tree.risk_profile(idx=0, cumulative=False, single=False)

    #
    # Test
    #
    captured_text = capsys.readouterr().out.splitlines()
    captured_text = [text.rstrip() for text in captured_text]
    matcher = LineMatcher(expected_text.splitlines()[1:])
    matcher.fnmatch_lines(captured_text, consecutive=True)


def test_fig_5_10(capsys):
    """Fig. 5.10 --- Cumulative plot distribution"""

    expected_text = dedent(
        r"""
                 Label  Value  Cumulative Probability
        0  500;EV=65.0   -100                  0.1625
        1  500;EV=65.0      0                  0.5125
        2  500;EV=65.0    100                  0.8375
        3  500;EV=65.0    300                  1.0000
        0  700;EV=45.0      0                  0.8500
        1  700;EV=45.0    100                  0.8875
        2  700;EV=45.0    300                  0.9625
        3  700;EV=45.0    500                  1.0000
        """
    )

    nodes = stguide()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback()
    tree.risk_profile(idx=0, cumulative=True, single=False)

    #
    # Test
    #
    captured_text = capsys.readouterr().out.splitlines()
    captured_text = [text.rstrip() for text in captured_text]
    matcher = LineMatcher(expected_text.splitlines()[1:])
    matcher.fnmatch_lines(captured_text, consecutive=True)


def test_fig_7_2(capsys):
    """Dependent probabilities"""

    expected_text = dedent(
        """
        STRUCTURE    NAMES    OUTCOMES     PROBABILIES
        ------------------------------------------------------
        0D1 14       bid      500 700
        1C2 6 10     compbid  400 600 800  .3500 .5000 .1500
        2C3 4 5      cost     200 400 600  .4000 .4000 .2000
        3T           profit
        4T           profit
        5T           profit
        6C7 8 9      cost     200 400 600  .2500 .5000 .2500
        7T           profit
        8T           profit
        9T           profit
        10C11 12 13  cost     200 400 600  .1000 .4500 .4500
        11T          profit
        12T          profit
        13T          profit
        14C15 19 23  compbid  400 600 800  .3500 .5000 .1500
        15C16 17 18  cost     200 400 600  .4000 .4000 .2000
        16T          profit
        17T          profit
        18T          profit
        19C20 21 22  cost     200 400 600  .2500 .5000 .2500
        20T          profit
        21T          profit
        22T          profit
        23C24 25 26  cost     200 400 600  .1000 .4500 .4500
        24T          profit
        25T          profit
        26T          profit
        """
    )

    nodes = stguide()
    tree = DecisionTree(variables=nodes, initial_variable="bid")

    ## Probabilities for COST depends on COMPBID
    tree.set_dependent_probabilities(
        variable="cost",
        depends_on="compbid",
        probabilities={
            400: [0.4, 0.4, 0.2],
            600: [0.25, 0.50, 0.25],
            800: [0.1, 0.45, 0.45],
        },
    )

    print(tree)

    #
    # Test
    #
    captured_text = capsys.readouterr().out.splitlines()
    captured_text = captured_text[1:]
    captured_text = [text.rstrip() for text in captured_text]
    matcher = LineMatcher(expected_text.splitlines()[1:])
    matcher.fnmatch_lines(captured_text, consecutive=True)


def test_fig_7_6(capsys):
    """Dependent outcomes"""

    expected_text = dedent(
        """
        STRUCTURE    NAMES    OUTCOMES     PROBABILIES
        ------------------------------------------------------
        0D1 14       bid      500 700
        1C2 6 10     compbid  400 600 800  .3500 .5000 .1500
        2C3 4 5      cost     170 350 550  .2500 .5000 .2500
        3T           profit
        4T           profit
        5T           profit
        6C7 8 9      cost     200 400 600  .2500 .5000 .2500
        7T           profit
        8T           profit
        9T           profit
        10C11 12 13  cost     280 450 650  .2500 .5000 .2500
        11T          profit
        12T          profit
        13T          profit
        14C15 19 23  compbid  400 600 800  .3500 .5000 .1500
        15C16 17 18  cost     190 380 570  .2500 .5000 .2500
        16T          profit
        17T          profit
        18T          profit
        19C20 21 22  cost     220 420 610  .2500 .5000 .2500
        20T          profit
        21T          profit
        22T          profit
        23C24 25 26  cost     300 480 680  .2500 .5000 .2500
        24T          profit
        25T          profit
        26T          profit
        """
    )

    nodes = stguide()
    tree = DecisionTree(variables=nodes, initial_variable="bid")

    ## Probabilities for COST depends on COMPBID, BID
    tree.set_dependent_outcomes(
        variable="cost",
        depends_on=("compbid", "bid"),
        outcomes={
            (400, 500): [170, 350, 550],
            (400, 700): [190, 380, 570],
            (600, 500): [200, 400, 600],
            (600, 700): [220, 420, 610],
            (800, 500): [280, 450, 650],
            (800, 700): [300, 480, 680],
        },
    )
    print(tree)

    #
    # Test
    #
    captured_text = capsys.readouterr().out.splitlines()
    captured_text = captured_text[1:]
    captured_text = [text.rstrip() for text in captured_text]
    matcher = LineMatcher(expected_text.splitlines()[1:])
    matcher.fnmatch_lines(captured_text, consecutive=True)


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
