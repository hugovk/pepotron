"""
Unit tests
"""

from __future__ import annotations

from typing import NamedTuple

import pytest

import pepotron


class Pull(NamedTuple):
    number: int
    title: str


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


def test_next(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    prs = [
        Pull(number=1, title="PEP 716: Seven One Six"),
        Pull(number=2, title="PEP 717: Seven One Seven"),
    ]
    monkeypatch.setattr(pepotron, "_get_github_prs", lambda: prs)

    # Act
    next_pep = pepotron.pep_url("next")

    # Assert
    assert next_pep.startswith("Next available PEP: ")
    assert next_pep.split()[-1].isdigit()


def test_next_ignore(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    prs = [
        Pull(number=100, title="PEP 829: Eight Two Nine"),
        Pull(number=101, title="PEP 832: Eight Three Two"),
    ]
    monkeypatch.setattr(pepotron, "_get_github_prs", lambda: prs)
    monkeypatch.setattr(
        pepotron, "_get_published_peps", lambda: set(range(1, 829)) | {830}
    )

    # Act
    without_ignore = pepotron.pep_url("next")
    with_ignore = pepotron.pep_url(
        "next", ignore=["https://github.com/python/peps/pull/100"]
    )

    with_ignore_int = pepotron.pep_url("next", ignore=["100"])

    # Assert
    # Without ignore, 829 and 830 are taken, so next is 831
    assert without_ignore == "Next available PEP: 831"
    # With ignore, PR 100 (PEP 829) is ignored, so 829 is available
    assert with_ignore == "Next available PEP: 829"
    # Also works with just a PR number
    assert with_ignore_int == "Next available PEP: 829"


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


def test__get_peps_ok() -> None:
    # Arrange
    pepotron._cache.clear(clear_all=True)
    # Act
    data = pepotron._get_peps()
    # Assert
    assert isinstance(data, dict)
    assert len(data) > 0


def test__get_peps_error() -> None:
    with pytest.raises(RuntimeError):
        pepotron._get_peps("https://httpbin.org/status/404")


def test_pep() -> None:
    url = pepotron.open_pep("8", dry_run=True)
    assert url == "https://peps.python.org/pep-0008/"


def test_open_bpo() -> None:
    url = pepotron.open_bpo(38374, dry_run=True)
    assert url == "https://bugs.python.org/issue?@action=redirect&bpo=38374"
