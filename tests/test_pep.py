"""
Unit tests
"""
import pytest

import pepotron


@pytest.mark.parametrize(
    "search, base_url, expected_url",
    [
        (
            "8",
            "https://peps.python.org",
            "https://peps.python.org/pep-0008/",
        ),
        (
            "12",
            "https://peps.python.org/",
            "https://peps.python.org/pep-0012/",
        ),
        (
            "2.7",
            "https://peps.python.org/",
            "https://peps.python.org/pep-0373/",
        ),
        (
            "3.11",
            "https://hugovk.github.io/peps",
            "https://hugovk.github.io/peps/pep-0664/",
        ),
    ],
)
def test_url(search: str, base_url: str, expected_url: str) -> None:
    # Act
    pep_url = pepotron.url(search, base_url)
    # Assert
    assert pep_url == expected_url


def test_url_pr() -> None:
    # Arrange
    search = "594"
    pr = 2440
    # Act
    pep_url = pepotron.url(search, pr=pr)
    # Assert
    assert pep_url == "https://pep-previews--2440.org.readthedocs.build/pep-0594/"
