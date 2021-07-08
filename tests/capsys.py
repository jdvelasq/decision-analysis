"""Routines for checking capsys"""

from _pytest.pytester import LineMatcher


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


def check_capsys(filename, capsys):
    """Checks system output"""
    matcher = _get_matcher(filename)
    captured_text = _get_captured_text(capsys)
    matcher.fnmatch_lines(captured_text, consecutive=True)
