"""
pepotron: CLI to open PEPs in your browser
"""
import argparse
import atexit
import logging

from pepotron import BASE_URL, __version__, _cache, pep

atexit.register(_cache.clear)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "search",
        nargs="?",
        help="PEP number, or Python version for its schedule, or words from title",
    )
    parser.add_argument(
        "-u", "--url", default=BASE_URL, help=f"Base URL for PEPs (default: {BASE_URL})"
    )
    parser.add_argument("-p", "--pr", type=int, help="Open preview for python/peps PR")
    parser.add_argument(
        "-n", "--dry-run", action="store_true", help="Don't open in browser"
    )
    parser.add_argument(
        "--clear-cache", action="store_true", help="Clear cache before running"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
        default=logging.WARNING,
        help="Verbose logging",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)
    if args.clear_cache:
        _cache.clear(clear_all=True)

    pep(search=args.search, base_url=args.url, pr=args.pr, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
