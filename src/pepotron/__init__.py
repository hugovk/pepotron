#!/usr/bin/env python3
"""
CLI to open PEPs in your browser
"""
from __future__ import annotations

import webbrowser

try:
    # Python 3.8+
    import importlib.metadata as importlib_metadata
except ImportError:
    # Python 3.7 and lower
    import importlib_metadata  # type: ignore

__version__ = importlib_metadata.version(__name__)

VERSION_TO_PEP = {
    "1.6": 160,
    "2.0": 200,
    "2.1": 226,
    "2.2": 251,
    "2.3": 283,
    "2.4": 320,
    "2.5": 356,
    "2.6": 361,
    "2.7": 373,
    "3.0": 361,
    "3.1": 375,
    "3.2": 392,
    "3.3": 398,
    "3.4": 429,
    "3.5": 478,
    "3.6": 494,
    "3.7": 537,
    "3.8": 569,
    "3.9": 596,
    "3.10": 619,
    "3.11": 664,
}


def url(search: str, base_url: str | None = None, pr: int | None = None) -> str:
    """Get PEP URL"""
    try:
        number = int(search)
    except ValueError:
        number = VERSION_TO_PEP[search]

    if pr:
        base_url = f"https://pep-previews--{pr}.org.readthedocs.build"

    return base_url.rstrip("/") + f"/pep-{number:04}" + "/"


def pep(search: str, base_url: str | None = None, pr: int | None = None) -> None:
    """Open this PEP in the browser"""
    pep_url = url(search, base_url, pr)
    print(pep_url)
    webbrowser.open(pep_url, new=2)  # 2 = open in a new tab, if possible
