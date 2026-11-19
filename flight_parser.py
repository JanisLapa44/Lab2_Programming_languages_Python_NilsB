"""Flight Schedule Parser and Query Tool - command-line entry point.

Run from the project folder, for example:
    python flight_parser.py -i data/db.csv -a data/airports.txt
"""
import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

from csv_loader import parse_files
from query import run_queries
from validator import load_airports

STUDENT_ID = "251RDC087"
FIRST_NAME = "Nils"
LAST_NAME = "Briska"


def main(argv: list[str] | None = None) -> int:
    """Run the whole program and return the exit code (0, 1 or 2).

    argv is the argument list without the program name.
    None means use sys.argv[1:] (argparse does this for you).
    Do not call sys.exit() inside main(); return the code instead.
    """
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("-i")
    source.add_argument("-d")
    source.add_argument("-j")

    parser.add_argument("-a")
    parser.add_argument("-o")
    parser.add_argument("-q")
    parser.add_argument("-r", default=".")

    try:
        args = parser.parse_args(argv)
        if (args.i or args.d) and not args.a:
            parser.error("CSV input requires an airport list (-a)")
        if args.j and args.o:
            parser.error("-o cannot be used with -j")
    except SystemExit as exc:
        return exc.code

    try:
        if args.j:
            with open(args.j, encoding="utf-8") as file:
                db = json.load(file)

            if not isinstance(db, list) or not all(isinstance(f, dict) for f in db):
                raise ValueError("database must be a list of flight objects")
        else:
            if args.i:
                paths = [args.i]
            else:
                paths = sorted(
                    str(path) for path in Path(args.d).iterdir()
                    if path.is_file() and path.suffix == ".csv"
                )
                if not paths:
                    raise ValueError("no .csv files in folder")

            airports = load_airports(args.a)
            db, errors = parse_files(paths, airports)
            output = Path(args.o or "db.json")
            with output.open("w", encoding="utf-8") as file:
                json.dump(db, file, indent=2, ensure_ascii=False)

            logger = logging.getLogger("flight_parser")
            handler = logging.FileHandler(
                output.with_name("errors.log"), mode="w", encoding="utf-8"
            )
            handler.setFormatter(logging.Formatter(
                "%(asctime)s %(levelname)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            ))
            logger.addHandler(handler)
            try:
                for message in errors:
                    logger.warning(message)
            finally:
                logger.removeHandler(handler)
                handler.close()

        if args.q:
            with open(args.q, encoding="utf-8") as file:
                queries = json.load(file)

            if not isinstance(queries, dict) and not (
                isinstance(queries, list) and all(isinstance(q, dict) for q in queries)
            ):
                raise ValueError("query file must contain an object or a list of objects")

            responses = run_queries(db, queries)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"response_{STUDENT_ID}_{FIRST_NAME}_{LAST_NAME}_{timestamp}.json"

            with (Path(args.r) / filename).open("w", encoding="utf-8") as file:
                json.dump(responses, file, indent=2, ensure_ascii=False)

        return 0

    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
