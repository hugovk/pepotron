"""
CLI to open PEPs in your browser
"""

from __future__ import annotations

import logging
from itertools import pairwise
from typing import Any

from . import _cache, _version

__version__ = _version.__version__

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
    "3.14": 745,
    "3.15": 790,
    "3.16": 826,
}


logger = logging.getLogger(__name__)


def _get_peps(json_url: str = BASE_URL + JSON_PATH) -> _cache.PepData:
    cache_file = _cache.filename(json_url)
    logger.info("Cache file: %s", cache_file)

    data = _cache.load(cache_file)
    if not data:
        # No cache, or couldn't load cache
        import urllib3

        resp = urllib3.request("GET", json_url, headers={"User-Agent": USER_AGENT})

        # Raise if we made a bad request
        # (4XX client error or 5XX server error response)
        logger.info("HTTP status code: %s", resp.status)
        if resp.status != 200:
            msg = f"Unable to download {json_url}: status {resp.status}"
            raise RuntimeError(msg)

        data = resp.json()

        _cache.save(cache_file, data)

    logger.info("")
    return data


def _get_published_peps() -> set[int]:
    peps = _get_peps()
    numbers = {int(number) for number in peps}
    return numbers


def _next_available_pep(ignore: list[str] | None = None) -> int:
    published = _get_published_peps()
    proposed = _get_pr_peps(ignore=ignore)
    combined = published | proposed
    numbers = sorted(combined)

    start = 828
    next_pep = -1
    for x, y in pairwise(numbers):
        if x < start:
            continue
        if x + 1 != y:
            next_pep = x + 1
            break

    return next_pep


def _get_github_prs() -> list[Any]:
    from ghapi.all import GhApi

    api = GhApi(owner="python", repo="peps", authenticate=False)
    return api.pulls.list(per_page=100)


def _get_pr_peps(ignore: list[str] | None = None) -> set[int]:
    import re

    pr_url_regex = re.compile(r"/pull/(\d+)")
    ignored_prs = set()
    for value in ignore or []:
        if value.isdigit():
            ignored_prs.add(int(value))
        elif match := re.search(pr_url_regex, value):
            ignored_prs.add(int(match[1]))

    pr_title_regex = re.compile(r"^PEP (\d+): .*")

    numbers = set()
    for pr in _get_github_prs():
        if pr.number in ignored_prs:
            continue
        if match := re.search(pr_title_regex, pr.title):
            number = match[1]
            numbers.add(int(number))

    return numbers


def word_search(search: str | None) -> int:
    from rapidfuzz import process

    peps = _get_peps()

    # Dict of title->number
    titles = {details["title"]: number for number, details in peps.items()}

    result = process.extract(search, titles.keys())
    print("Score   Result")
    for title, score, _ in result:
        print(f"{round(score):<8}PEP {titles[title]}: {title}")
    print()

    # Find PEP number of top match
    return int(titles[result[0][0]])


def pep_url(
    search: str | None,
    base_url: str = BASE_URL,
    pr: int | None = None,
    ignore: list[str] | None = None,
) -> str:
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

    if search.lower() == "next":
        from yaspin import yaspin

        with yaspin(color="yellow"):
            return f"Next available PEP: {_next_available_pep(ignore=ignore)}"

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
    search: str,
    base_url: str = BASE_URL,
    pr: int | None = None,
    dry_run: bool = False,
    ignore: list[str] | None = None,
) -> str:
    """Open this PEP in the browser"""
    url = pep_url(search, base_url, pr, ignore=ignore)
    if not dry_run and "Next available PEP: " not in url:
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
