"""
Test suite for the SuperTree user guide simple bid example.

"""

from textwrap import dedent

from _pytest.pytester import LineMatcher

from dmak.decisiontree import DecisionTree
from dmak.examples import stguide_bid


def test_fig_5_1(capsys):
    """Example creation from Fig. 5.1"""

    expected_text = dedent(
        r"""
        |
        |
        \---[D]
             | bid
             |   500.00
             +------[C]
             |       | compbid
             |       | .350   400.00
             |       +-----------[C]
             |       |            | cost
             |       |            | .250   200.00
             |       |            | .500   400.00
             |       |            \ .250   600.00
             |       | compbid
             |       | .500   600.00
             |       +-----------[C]
             |       |            | cost
             |       |            | .250   200.00
             |       |            | .500   400.00
             |       |            \ .250   600.00
             |       | compbid
             |       | .150   800.00
             |       \-----------[C]
             |                    | cost
             |                    | .250   200.00
             |                    | .500   400.00
             |                    \ .250   600.00
             | bid
             |   700.00
             \------[C]
                     | compbid
                     | .350   400.00
                     +-----------[C]
                     |            | cost
                     |            | .250   200.00
                     |            | .500   400.00
                     |            \ .250   600.00
                     | compbid
                     | .500   600.00
                     +-----------[C]
                     |            | cost
                     |            | .250   200.00
                     |            | .500   400.00
                     |            \ .250   600.00
                     | compbid
                     | .150   800.00
                     \-----------[C]
                                  | cost
                                  | .250   200.00
                                  | .500   400.00
                                  \ .250   600.00


        """
    )

    nodes = stguide_bid()
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
        ---------------------------------------------------
        0D1 14       bid      500 700
        1C2 6 10     compbid  400 600 800  .350 .500 .150
        2C3 4 5      cost     200 400 600  .250 .500 .250
        3T           profit
        4T           profit
        5T           profit
        6C7 8 9      cost     200 400 600  .250 .500 .250
        7T           profit
        8T           profit
        9T           profit
        10C11 12 13  cost     200 400 600  .250 .500 .250
        11T          profit
        12T          profit
        13T          profit
        14C15 19 23  compbid  400 600 800  .350 .500 .150
        15C16 17 18  cost     200 400 600  .250 .500 .250
        16T          profit
        17T          profit
        18T          profit
        19C20 21 22  cost     200 400 600  .250 .500 .250
        20T          profit
        21T          profit
        22T          profit
        23C24 25 26  cost     200 400 600  .250 .500 .250
        24T          profit
        25T          profit
        26T          profit
        """
    )

    nodes = stguide_bid()
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
        \---[D]
             | bid
             |   500.00
             +------[C]
             |       | compbid
             |       | .350   400.00
             |       +-----------[C]
             |       |            | cost
             |       |            | .250   200.00 :     0.00
             |       |            | .500   400.00 :     0.00
             |       |            \ .250   600.00 :     0.00
             |       | compbid
             |       | .500   600.00
             |       +-----------[C]
             |       |            | cost
             |       |            | .250   200.00 :   300.00
             |       |            | .500   400.00 :   100.00
             |       |            \ .250   600.00 :  -100.00
             |       | compbid
             |       | .150   800.00
             |       \-----------[C]
             |                    | cost
             |                    | .250   200.00 :   300.00
             |                    | .500   400.00 :   100.00
             |                    \ .250   600.00 :  -100.00
             | bid
             |   700.00
             \------[C]
                     | compbid
                     | .350   400.00
                     +-----------[C]
                     |            | cost
                     |            | .250   200.00 :     0.00
                     |            | .500   400.00 :     0.00
                     |            \ .250   600.00 :     0.00
                     | compbid
                     | .500   600.00
                     +-----------[C]
                     |            | cost
                     |            | .250   200.00 :     0.00
                     |            | .500   400.00 :     0.00
                     |            \ .250   600.00 :     0.00
                     | compbid
                     | .150   800.00
                     \-----------[C]
                                  | cost
                                  | .250   200.00 :   500.00
                                  | .500   400.00 :   300.00
                                  \ .250   600.00 :   100.00
        """
    )

    nodes = stguide_bid()
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
        \------[D]
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
                \---------------[C]
                                 | compbid
                                 | .350   400.00     0.00
                                 +--------------------[C]
                                 |                     | cost
                                 |                     | .250   200.00 :     0.00 .000
                                 |                     | .500   400.00 :     0.00 .000
                                 |                     \ .250   600.00 :     0.00 .000
                                 | compbid
                                 | .500   600.00     0.00
                                 +--------------------[C]
                                 |                     | cost
                                 |                     | .250   200.00 :     0.00 .000
                                 |                     | .500   400.00 :     0.00 .000
                                 |                     \ .250   600.00 :     0.00 .000
                                 | compbid
                                 | .150   800.00   300.00
                                 \--------------------[C]
                                                       | cost
                                                       | .250   200.00 :   500.00 .000
                                                       | .500   400.00 :   300.00 .000
                                                       \ .250   600.00 :   100.00 .000






        """
    )

    nodes = stguide_bid()
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

    nodes = stguide_bid()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback()
    tree.risk_profile_table(idx=0, cumulative=False, single=True)

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

    nodes = stguide_bid()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback()
    tree.risk_profile_table(idx=0, cumulative=True, single=True)

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

    nodes = stguide_bid()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback()
    tree.risk_profile_table(idx=0, cumulative=False, single=False)

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

    nodes = stguide_bid()
    tree = DecisionTree(variables=nodes, initial_variable="bid")
    tree.evaluate()
    tree.rollback()
    tree.risk_profile_table(idx=0, cumulative=True, single=False)

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
        ---------------------------------------------------
        0D1 14       bid      500 700
        1C2 6 10     compbid  400 600 800  .350 .500 .150
        2C3 4 5      cost     200 400 600  .400 .400 .200
        3T           profit
        4T           profit
        5T           profit
        6C7 8 9      cost     200 400 600  .250 .500 .250
        7T           profit
        8T           profit
        9T           profit
        10C11 12 13  cost     200 400 600  .100 .450 .450
        11T          profit
        12T          profit
        13T          profit
        14C15 19 23  compbid  400 600 800  .350 .500 .150
        15C16 17 18  cost     200 400 600  .400 .400 .200
        16T          profit
        17T          profit
        18T          profit
        19C20 21 22  cost     200 400 600  .250 .500 .250
        20T          profit
        21T          profit
        22T          profit
        23C24 25 26  cost     200 400 600  .100 .450 .450
        24T          profit
        25T          profit
        26T          profit
        """
    )

    nodes = stguide_bid()
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


def test_dependent_outcomes(capsys):
    """Example Fig. 7.2"""

    expected_text = dedent(
        """
        STRUCTURE    NAMES    OUTCOMES     PROBABILIES
        ---------------------------------------------------
        0D1 14       bid      500 700
        1C2 6 10     compbid  400 600 800  .350 .500 .150
        2C3 4 5      cost     170 350 550  .250 .500 .250
        3T           profit
        4T           profit
        5T           profit
        6C7 8 9      cost     200 400 600  .250 .500 .250
        7T           profit
        8T           profit
        9T           profit
        10C11 12 13  cost     280 450 650  .250 .500 .250
        11T          profit
        12T          profit
        13T          profit
        14C15 19 23  compbid  400 600 800  .350 .500 .150
        15C16 17 18  cost     190 380 570  .250 .500 .250
        16T          profit
        17T          profit
        18T          profit
        19C20 21 22  cost     220 420 610  .250 .500 .250
        20T          profit
        21T          profit
        22T          profit
        23C24 25 26  cost     300 480 680  .250 .500 .250
        24T          profit
        25T          profit
        26T          profit
        """
    )

    nodes = stguide_bid()
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
