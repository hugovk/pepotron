#!/usr/bin/env python3
"""
CLI to open PEPs in your browser
"""
import argparse

import pepotron


class Formatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawDescriptionHelpFormatter,
):
    pass


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=Formatter)
    parser.add_argument("search", help="PEP number, or Python version for its schedule")
    parser.add_argument(
        "-u",
        "--url",
        default="https://peps.python.org",
        help="Base URL for PEPs",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {pepotron.__version__}"
    )
    args = parser.parse_args()
    pepotron.pep(search=args.search, base_url=args.url)


if __name__ == "__main__":
    main()
