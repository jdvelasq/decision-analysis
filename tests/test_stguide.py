"""
Test suite for the SuperTree user guide simple bid example.

"""

from textwrap import dedent

from _pytest.pytester import LineMatcher

from dmak.decisiontree import DecisionTree
from dmak.examples import stguide_bid


def test_tree_creation(capsys):
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


def test_dependent_probabilities(capsys):
    """Example Fig. 7.2"""

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


def test_display_no_evaluated(capsys):
    """Example creatioin from Fig. 5.4"""

    expected_text = dedent(
        """
        |
        |
        \\---[D]
             | bid
             |   500.00
             +-------[C]
             |        | compbid
             |        | .350   400.00
             |        +------------[C]
             |        |             | cost
             |        |             | .250   200.00
             |        |             | .500   400.00
             |        |             \\ .250   600.00
             |        | compbid
             |        | .500   600.00
             |        +------------[C]
             |        |             | cost
             |        |             | .250   200.00
             |        |             | .500   400.00
             |        |             \\ .250   600.00
             |        | compbid
             |        | .150   800.00
             |        \\------------[C]
             |                      | cost
             |                      | .250   200.00
             |                      | .500   400.00
             |                      \\ .250   600.00
             | bid
             |   700.00
             \\-------[C]
                      | compbid
                      | .350   400.00
                      +------------[C]
                      |             | cost
                      |             | .250   200.00
                      |             | .500   400.00
                      |             \\ .250   600.00
                      | compbid
                      | .500   600.00
                      +------------[C]
                      |             | cost
                      |             | .250   200.00
                      |             | .500   400.00
                      |             \\ .250   600.00
                      | compbid
                      | .150   800.00
                      \\------------[C]
                                    | cost
                                    | .250   200.00
                                    | .500   400.00
                                    \\ .250   600.00
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


def test_evaluate(capsys):
    """Example creatioin from Fig. 5.4"""

    expected_text = dedent(
        """
        |
        |
        \\---[D]
             | bid
             |   500.00
             +-------[C]
             |        | compbid
             |        | .350   400.00
             |        +------------[C]
             |        |             | cost
             |        |             | .250   200.00     0.00
             |        |             | .500   400.00     0.00
             |        |             \\ .250   600.00     0.00
             |        | compbid
             |        | .500   600.00
             |        +------------[C]
             |        |             | cost
             |        |             | .250   200.00   300.00
             |        |             | .500   400.00   100.00
             |        |             \\ .250   600.00  -100.00
             |        | compbid
             |        | .150   800.00
             |        \\------------[C]
             |                      | cost
             |                      | .250   200.00   300.00
             |                      | .500   400.00   100.00
             |                      \\ .250   600.00  -100.00
             | bid
             |   700.00
             \\-------[C]
                      | compbid
                      | .350   400.00
                      +------------[C]
                      |             | cost
                      |             | .250   200.00     0.00
                      |             | .500   400.00     0.00
                      |             \\ .250   600.00     0.00
                      | compbid
                      | .500   600.00
                      +------------[C]
                      |             | cost
                      |             | .250   200.00     0.00
                      |             | .500   400.00     0.00
                      |             \\ .250   600.00     0.00
                      | compbid
                      | .150   800.00
                      \\------------[C]
                                    | cost
                                    | .250   200.00   500.00
                                    | .500   400.00   300.00
                                    \\ .250   600.00   100.00
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
