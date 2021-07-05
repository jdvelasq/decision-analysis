"""
PrecisionTree Oil Example

"""
from textwrap import dedent

from _pytest.pytester import LineMatcher

from dmak.examples import oil_tree_example


def test_pag43(capsys):
    """Basic oil tree example"""

    expected_text = dedent(
        r"""
        |
        |   544.92
        \------[D] #0
                | test_decision
                > test         -55.00   544.92
                +--------------------------[C] #1
                |                           | test_results
                |                           | ind_dry    .3800     0.00   -55.00
                |                           +--------------------------------[D] #2
                |                           |                                 | drill_decision
                |                           |                                 | drill       -600.00  -239.31
                |                           |                                 +--------------------------[C] #3
                |                           |                                 |                           | oil_found
                |                           |                                 |                           | dry        .7895     0.00 :  -655.00 .0000
                |                           |                                 |                           | small      .1579  1500.00 :   845.00 .0000
                |                           |                                 |                           \ large      .0526  3400.00 :  2745.00 .0000
                |                           |                                 > dont-drill     0.00 :   -55.00 1.000
                |                           | test_results
                |                           | ind_small  .3900     0.00   560.24
                |                           +--------------------------------[D] #8
                |                           |                                 | drill_decision
                |                           |                                 > drill       -600.00   560.24
                |                           |                                 +--------------------------[C] #9
                |                           |                                 |                           | oil_found
                |                           |                                 |                           | dry        .3846     0.00 :  -655.00 .3846
                |                           |                                 |                           | small      .4615  1500.00 :   845.00 .4615
                |                           |                                 |                           \ large      .1538  3400.00 :  2745.00 .1538
                |                           |                                 \ dont-drill     0.00 :   -55.00 .0000
                |                           | test_results
                |                           | ind_large  .2300     0.00  1510.13
                |                           \--------------------------------[D] #14
                |                                                             | drill_decision
                |                                                             > drill       -600.00  1510.13
                |                                                             +--------------------------[C] #15
                |                                                             |                           | oil_found
                |                                                             |                           | dry        .2174     0.00 :  -655.00 .2174
                |                                                             |                           | small      .2609  1500.00 :   845.00 .2609
                |                                                             |                           \ large      .5217  3400.00 :  2745.00 .5217
                |                                                             \ dont-drill     0.00 :   -55.00 .0000
                | test_decision
                | dont-test      0.00   530.00
                \--------------------------[D] #20
                                            | drill_decision
                                            | drill       -600.00   530.00
                                            +--------------------------[C] #21
                                            |                           | oil_found
                                            |                           | dry        .5000     0.00 :  -600.00 .0000
                                            |                           | small      .3000  1500.00 :   900.00 .0000
                                            |                           \ large      .2000  3400.00 :  2800.00 .0000
                                            \ dont-drill     0.00 :     0.00 .0000
        """
    )

    tree = oil_tree_example()
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


def test_pag56(capsys):
    """Basic oil tree example"""

    expected_text = dedent(
        r"""
        |
        |   544.92
        \------[D] #0
                | test_decision
                > test         -55.00   544.92
                +--------------------------[C] #1
                |                           | test_results
                |                           | ind_dry    .3800     0.00   -55.00
                |                           +--------------------------------[D] #2
                |                           |                                 | drill_decision
                |                           |                                 | drill       -600.00  -239.31
                |                           |                                 +--------------------------[C] #3
                |                           |                                 > dont-drill     0.00 :   -55.00 1.000
                |                           | test_results
                |                           | ind_small  .3900     0.00   560.24
                |                           +--------------------------------[D] #8
                |                           |                                 | drill_decision
                |                           |                                 > drill       -600.00   560.24
                |                           |                                 +--------------------------[C] #9
                |                           |                                 \ dont-drill     0.00 :   -55.00 .0000
                |                           | test_results
                |                           | ind_large  .2300     0.00  1510.13
                |                           \--------------------------------[D] #14
                |                                                             | drill_decision
                |                                                             > drill       -600.00  1510.13
                |                                                             +--------------------------[C] #15
                |                                                             \ dont-drill     0.00 :   -55.00 .0000
                | test_decision
                | dont-test      0.00   530.00
                \--------------------------[D] #20
                                            | drill_decision
                                            | drill       -600.00   530.00
                                            +--------------------------[C] #21
                                            |                           | oil_found
                                            |                           | dry        .5000     0.00 :  -600.00 .0000
                                            |                           | small      .3000  1500.00 :   900.00 .0000
                                            |                           \ large      .2000  3400.00 :  2800.00 .0000
                                            \ dont-drill     0.00 :     0.00 .0000

        """
    )

    tree = oil_tree_example()
    tree.evaluate()
    tree.rollback()
    tree.display(max_deep=3)

    #
    # Test
    #
    captured_text = capsys.readouterr().out.splitlines()
    captured_text = [text.rstrip() for text in captured_text]
    matcher = LineMatcher(expected_text.splitlines()[1:])
    matcher.fnmatch_lines(captured_text, consecutive=True)
