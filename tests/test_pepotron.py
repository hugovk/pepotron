"""
Unit tests
"""
from __future__ import annotations

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
        ("release", "https://peps.python.org/topic/release/"),
        ("typing", "https://peps.python.org/topic/typing/"),
        ("topics", "https://peps.python.org/topic/"),
        ("topic", "https://peps.python.org/topic/"),
    ],
)
def test_url(search: str, expected_url: str) -> None:
    # Act
    pep_url = pepotron.pep_url(search)
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
    pep_url = pepotron.pep_url(search, base_url)
    # Assert
    assert pep_url == expected_url


@pytest.mark.parametrize(
    "search, expected_url",
    [
        ("594", "https://pep-previews--2440.org.readthedocs.build/pep-0594/"),
        (None, "https://pep-previews--2440.org.readthedocs.build"),
    ],
)
def test_url_pr(search: str | None, expected_url: str) -> None:
    # Arrange
    pr = 2440
    # Act
    pep_url = pepotron.pep_url(search, pr=pr)
    # Assert
    assert pep_url == expected_url


def test_pep() -> None:
    url = pepotron.open_pep("8", dry_run=True)
    assert url == "https://peps.python.org/pep-0008/"


def test_open_bpo() -> None:
    url = pepotron.open_bpo(38374, dry_run=True)
    assert url == "https://bugs.python.org/issue?@action=redirect&bpo=38374"
