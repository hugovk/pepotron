"""
Cache functions
"""
from __future__ import annotations

import datetime as dt
import json
import logging
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from platformdirs import user_cache_dir

if TYPE_CHECKING:
    if sys.version_info >= (3, 10):
        from typing import TypeAlias
    else:
        from typing_extensions import TypeAlias

PepData: TypeAlias = "dict[str, dict[str, str]]"

CACHE_DIR = Path(user_cache_dir("pepotron"))


def filename(url: str) -> Path:
    """yyyy-mm-dd-url-slug.json"""
    from slugify import slugify

    today = dt.datetime.utcnow().strftime("%Y-%m-%d")
    slug = slugify(url)
    return CACHE_DIR / f"{today}-{slug}.json"


def load(cache_file: Path) -> PepData:
    """Load data from cache_file"""
    if not cache_file.exists():
        return {}

    logging.info("Cache file exists")
    with cache_file.open("r") as f:
        try:
            data: PepData = json.load(f)
        except json.decoder.JSONDecodeError:
            return {}

    return data


def save(cache_file: Path, data: PepData) -> None:
    """Save data to cache_file"""
    try:
        if not CACHE_DIR.exists():
            CACHE_DIR.mkdir(parents=True)

        with cache_file.open("w") as f:
            json.dump(data, f)

    except OSError:
        pass


def clear(clear_all: bool = False) -> None:
    """Delete all or old cache files"""
    cache_files = CACHE_DIR.glob("**/*.json")
    today = dt.datetime.utcnow().strftime("%Y-%m-%d")
    for cache_file in cache_files:
        if clear_all or not cache_file.name.startswith(today):
            cache_file.unlink()
