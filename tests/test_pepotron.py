"""
Unit tests
"""
import pytest

import pepotron


@pytest.mark.parametrize(
    "search, expected_url",
    [
        ("8", "https://peps.python.org/pep-0008/"),
        ("12", "https://peps.python.org/pep-0012/"),
        ("2.7", "https://peps.python.org/pep-0373/"),
        (None, "https://peps.python.org"),
        ("dead batteries", "https://peps.python.org/pep-0594/"),
    ],
)
def test_url(search: str, expected_url: str) -> None:
    # Act
    pep_url = pepotron.url(search)
    # Assert
    assert pep_url == expected_url


@pytest.mark.parametrize(
    "search, base_url, expected_url",
    [
        (
            "8",
            "https://hugovk.github.io/peps",
            "https://hugovk.github.io/peps/pep-0008/",
        ),
        (
            "3.11",
            "https://hugovk.github.io/peps",
            "https://hugovk.github.io/peps/pep-0664/",
        ),
        (
            None,
            "https://hugovk.github.io/peps",
            "https://hugovk.github.io/peps",
        ),
        (
            "dead batteries",
            "https://hugovk.github.io/peps",
            "https://hugovk.github.io/peps/pep-0594/",
        ),
    ],
)
def test_url_base_url(search: str, base_url: str, expected_url: str) -> None:
    # Act
    pep_url = pepotron.url(search, base_url)
    # Assert
    assert pep_url == expected_url


@pytest.mark.parametrize(
    "search, expected_url",
    [
        ("594", "https://pep-previews--2440.org.readthedocs.build/pep-0594/"),
        (None, "https://pep-previews--2440.org.readthedocs.build"),
    ],
)
def test_url_pr(search, expected_url) -> None:
    # Arrange
    pr = 2440
    # Act
    pep_url = pepotron.url(search, pr=pr)
    # Assert
    assert pep_url == expected_url


def test_pep() -> None:
    pepotron.pep("8", dry_run=True)
