"""
CLI to open PEPs in your browser
"""
from __future__ import annotations

import importlib.metadata
import logging
from pathlib import Path

from pepotron import _cache

__version__ = importlib.metadata.version(__name__)

BASE_URL = "https://peps.python.org"
JSON_PATH = "/api/peps.json"
USER_AGENT = f"pepotron/{__version__}"

TOPICS = ("governance", "packaging", "release", "typing")
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
    "3.12": 693,
    "3.13": 719,
}


def _download_peps_json(json_url: str = BASE_URL + JSON_PATH) -> Path:
    cache_file = _cache.filename(json_url)
    logging.info(f"Cache file: {cache_file}")

    data = _cache.load(cache_file)
    if data == {}:
        # No cache, or couldn't load cache
        import urllib3

        resp = urllib3.request("GET", json_url, headers={"User-Agent": USER_AGENT})

        # Raise if we made a bad request
        # (4XX client error or 5XX server error response)
        logging.info(f"HTTP status code: {resp.status}")
        if resp.status != 200:
            msg = f"Unable to download {json_url}: status {resp.status}"
            raise RuntimeError(msg)

        data = resp.json()

        _cache.save(cache_file, data)

    logging.info("")
    return cache_file


def word_search(search: str | None) -> int:
    import json

    peps_file = _download_peps_json()

    from rapidfuzz import process

    with open(peps_file) as f:
        peps = json.load(f)

    # Dict of title->number
    titles = {details["title"]: number for number, details in peps.items()}

    result = process.extract(search, titles.keys())
    print("Score   Result")
    for title, score, _ in result:
        print(f"{round(score):<8}PEP {titles[title]}: {title}")
    print()

    # Find PEP number of top match
    number: int = next(
        number for number, details in peps.items() if details["title"] == result[0][0]
    )

    return number


def pep_url(search: str | None, base_url: str = BASE_URL, pr: int | None = None) -> str:
    """Get PEP URL"""
    if pr:
        base_url = f"https://pep-previews--{pr}.org.readthedocs.build"

    result = base_url.rstrip("/")

    if not search:
        return result

    if search.lower() in ("topic", "topics"):
        return result + "/topic/"

    if search.lower() in TOPICS:
        return result + f"/topic/{search}/"

    try:
        # pep 8
        number = int(search)
    except ValueError:
        try:
            # pep 3.11
            number = VERSION_TO_PEP[search]
        except KeyError:
            # pep "dead batteries"
            number = word_search(search)

    return result + f"/pep-{number:0>4}/"


def open_pep(
    search: str, base_url: str = BASE_URL, pr: int | None = None, dry_run: bool = False
) -> str:
    """Open this PEP in the browser"""
    url = pep_url(search, base_url, pr)
    if not dry_run:
        import webbrowser

        webbrowser.open_new_tab(url)
    print(url)
    return url


def open_bpo(number: int, dry_run: bool = False) -> str:
    """Open this BPO in the browser"""
    url = f"https://bugs.python.org/issue?@action=redirect&bpo={number}"
    if not dry_run:
        import webbrowser

        webbrowser.open_new_tab(url)
    print(url)
    return url
