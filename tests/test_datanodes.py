"""
DataNodes creation tests.

"""
from smart_choice.examples import (
    stguide,
    stguide_dependent_outcomes,
    stguide_dependent_probabilities,
    oil_tree_example,
)

from tests.capsys import check_capsys


def test_stguide_fig_5_4a(capsys):
    """Table of variables"""

    nodes = stguide()
    print(nodes)
    check_capsys("./tests/files/stguide_fig_5_4a.txt", capsys)


def test_stguide_fig_7_3a(capsys):
    """Change probabilities"""

    nodes = stguide_dependent_probabilities()
    print(nodes)
    check_capsys("./tests/files/stguide_fig_7_3a.txt", capsys)


def test_stguide_fig_7_6a(capsys):
    """Dependent outcomes"""

    nodes = stguide_dependent_outcomes()
    print(nodes)
    check_capsys("./tests/files/stguide_fig_7_6a.txt", capsys)


def test_oilexample_pag_43a(capsys):
    """Table of variables"""

    nodes = oil_tree_example()
    print(nodes)
    check_capsys("./tests/files/oilexample_pag_43a.txt", capsys)
