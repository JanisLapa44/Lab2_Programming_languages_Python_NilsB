"""Reading CSV files into flight records and error messages."""

import csv
import os

from validator import to_record, validate_row



def parse_files(paths: list[str], airports: set[str]) -> tuple[list[dict], list[str]]:
    """Process the CSV files in the order given.

    Return (records, errors):
      records - valid flight records, in input order
      errors  - one message per invalid row, in input order, formatted as
                "<file name>:<line number>: <ERROR_CODE> | <free text>"
                (base file name only, no timestamp or level, no newline)

    Also performs the DUPLICATE_FLIGHT check across all the files.
    Does not write any files and does not log anything itself.
    """
    records = []
    errors = []
    seen = set()
    for path in paths:
        name = os.path.basename(path)
        with open(path, encoding="utf-8") as fh:
            # check error paths, first line is header, skip if # is first non whitespace character
            for n, line in enumerate(fh, 1):
                raw = line.rstrip("\r\n")
                if n == 1:
                    continue
                if not raw.strip():
                    continue
                if raw.lstrip().startswith("#"):
                    continue
                fields = next(csv.reader([raw]))
                code = validate_row(fields, airports)
                if code is None and (fields[0].strip(), fields[3].strip()) in seen:
                    code = "DUPLICATE_FLIGHT"
                if code is None:
                    seen.add((fields[0].strip(), fields[3].strip()))
                    records.append(to_record(fields))
                else:
                    errors.append(f"{name}:{n}: {code} | {raw}")
    return records, errors